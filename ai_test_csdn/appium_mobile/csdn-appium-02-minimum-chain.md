# Appium 最小可执行链路：连设备 → 找元素 → 操作 → 断言

> 环境终于搭好了。你是不是现在特别想打开一个 App 然后对着屏幕戳戳戳？这一章就是干这个的——给你一条从连接设备到断言成功的最短路径。而且你会发现，跟 Selenium 写得几乎一模一样。

---

## Appium 的四步骨架：跟 Selenium 一样吗？

把 Appium 的操作拆开，跟 Selenium 的最小可执行链路对比一下：

```
Selenium：  启动浏览器 → 打开页面 → 定位元素 → 操作 → 断言 → 关闭
Appium：    连接设备  → 启动 App  → 定位元素 → 操作 → 断言 → 关闭
```

区别就两个：
1. Selenium 是 `webdriver.Chrome()` 本地起浏览器，Appium 是 `webdriver.Remote()` 连到一个 Appium Server。
2. Selenium 是 `driver.get("https://...")` 打开网页，Appium 是配一堆 `options` 告诉 Server 你要打开哪个 App。

这两步搞定之后——`find_element`、`send_keys`、`click`、`WebDriverWait`、`assert`——**写法和 Selenium 一模一样。** 正因为这样，如果你是从 Selenium 系列过来的，这篇你的学习成本大约是百分之二十。

---

## 第一步：启动 Appium Server

跑任何 Appium 脚本之前，要先把 Server 跑起来。开一个新终端：

```bash
appium
```

留这个窗口别关。看到这行绿字说明 Server 就绪了：

```
[Appium] Appium REST http interface listener started on http://0.0.0.0:4723
```

Appium Server 监听在 `4723` 端口，你的 Python 代码通过这个端口跟它通信。

**一个容易被忽略的点：** Appium Server 启动时加载了你之前安装的所有驱动。如果你的 `appium` 启动日志里有一行报错说某个驱动加载失败——虽然你测的是 Android，但失败的 iOS 驱动日志也会让你心慌。不用管，只要 `uiautomator2` 驱动加载成功就行。

---

## 第二步：确保模拟器/真机连上了

```bash
adb devices
```

确保输出里至少有一个设备：

```
List of devices attached
emulator-5554   device
```

如果显示 `offline`，设备连接断了。如果显示 `unauthorized`，手机上没点允许——解锁屏幕重新插拔。

如果 `adb devices` 看不到任何设备：模拟器没开就去开，真机没插就去插。别跳过这步直接跑脚本——Appium 会报 `device not found` 而且报错信息非常不友好。

---

## 第三步：配置 Appium Options——2026 年唯一正确的写法

Appium 3 不再接受旧格式的 `desired_capabilities` 字典。现在必须用 `Options` 对象。Android 端长这样：

```python
from appium.options.android import UiAutomator2Options

options = UiAutomator2Options()
options.platform_name = "Android"
options.automation_name = "UiAutomator2"
options.device_name = "emulator-5554"           # adb devices 看到的设备名
options.app_package = "com.android.settings"    # App 包名
options.app_activity = ".Settings"              # 启动页面 Activity
```

### 每个字段是干什么的

- **`platform_name`**：固定 `"Android"` 或 `"iOS"`。没什么好说的。
- **`automation_name`**：你用的是什么底层引擎。Android 用 `"UiAutomator2"`，iOS 用 `"XCUITest"`。这决定了 Appium Server 调用哪个驱动。
- **`device_name`**：设备标识。模拟器一般叫 `emulator-5554`。真机是设备序列号（`adb devices` 显示的）。
- **`app_package`**：你要打开哪个 App。相当于 Android 里的包名，比如微信是 `com.tencent.mm`，设置是 `com.android.settings`。
- **`app_activity`**：启动哪个页面。`.` 开头是省略包名的简写。`.Settings` 等于 `com.android.settings.Settings`。

### 怎么查一个 App 的包名和 Activity

最简单的办法是用 adb 查当前正在运行的 App：

```bash
# 先在手机上打开目标 App，然后敲这个
adb shell dumpsys window | findstr mCurrentFocus
```

输出大概长这样：

```
mCurrentFocus=Window{... com.android.settings/com.android.settings.Settings}
```

`com.android.settings` 就是包名，`com.android.settings.Settings` 就是 Activity 的全路径。你可以简写成 `app_package="com.android.settings"` + `app_activity=".Settings"`。

另一个办法是直接拿到目标 App 的 APK 文件，用 `aapt` 工具提取包名和启动 Activity。但那属于进阶玩法，入门用 adb 足够了。

---

## 第四步：连接——`webdriver.Remote()`

```python
from appium import webdriver

driver = webdriver.Remote("http://localhost:4723", options=options)
```

这行干了三件事：
1. Python 客户端发了一个 HTTP POST 到 `http://localhost:4723/session`
2. 请求里带着你配好的 options（平台、设备名、包名、Activity）
3. Appium Server 收到后，根据 `automation_name` 调 UiAutomator2 驱动，驱动通过 adb 在手机上启动 Settings App

如果一切正常，你会看到模拟器/真机上 Settings App 打开了。而且 `driver` 这个对象就是你的「手机遥控器」。

### 连接失败最常见的原因

`Connection refused` 或者 `could not connect to server`——Appium Server 没启动。回第一步启动它。

`A new session could not be created`——检查这三样：
- 设备有没有连上（`adb devices`）
- 包名对不对（在目标 App 开启的情况下跑 `adb shell dumpsys window | findstr mCurrentFocus` 确认）
- UiAutomator2 驱动装没装（`appium driver list` 确认）

---

## 第五步：定位元素——App 和 Web 的差异

元素定位在 App 里比 Web 复杂，因为 App 的元素属性和 HTML 不完全一样。Appium 给 App 端也提供了好几种定位方式：

| 定位方式 | 写法 | 什么时候用 |
|------|------|-----------|
| **Accessibility ID** | `AppiumBy.ACCESSIBILITY_ID, "登录"` | 最推荐，最稳定 |
| **ID** | `AppiumBy.ID, "com.example:id/btn"` | 带包名前缀的完整 ID |
| **XPath** | `AppiumBy.XPATH, "//button[@text='登录']"` | WebView 中或别无选择时 |
| **Class Name** | `AppiumBy.CLASS_NAME, "android.widget.Button"` | 同类元素批量操作 |
| **UI Automator Selector** | `AppiumBy.ANDROID_UIAUTOMATOR, '...'` | Android 专项高级定位 |

### `AppiumBy` vs `By`

你如果在 Selenium 系列里用的是 `By.ID`，在 Appium 里要用 `AppiumBy.ID`。

```python
# 这是 Selenium
from selenium.webdriver.common.by import By
driver.find_element(By.ID, "kw")

# 这是 Appium
from appium.webdriver.common.appiumby import AppiumBy
driver.find_element(AppiumBy.ID, "com.android.settings:id/search_action_bar")
```

不导入 `AppiumBy` 直接用 `By` 也不会报错，但它走的是 Selenium 的 Web 逻辑而不是 Appium 的移动端逻辑，某些定位方式会失效。直接用 `AppiumBy` 别偷懒。

### 用系统 Settings App 练手

系统 Settings App 每个 Android 手机都有，先拿它练。用 Appium Inspector（`http://localhost:4723/inspector`）连上之后能看到 Settings 的页面元素树。

Settings 首页通常有个搜索按钮，它的 ID 大概是 `com.android.settings:id/search_action_bar`。

```python
# 找到搜索按钮，点击
search_btn = driver.find_element(
    AppiumBy.ID, "com.android.settings:id/search_action_bar"
)
search_btn.click()
```

不同手机品牌的 Settings App 界面不一样——三星、小米、华为、原生 Android 的 Settings 界面和元素 ID 都不同。用模拟器的原生 Android 做练习最省心。

---

## 第六步：操作元素——跟 Web 一样又不太一样

### 输入文字

```python
element = driver.find_element(AppiumBy.ID, "android:id/search_src_text")
element.send_keys("WiFi")
```

用法跟 Selenium 一样。但有一个区别：App 里的输入法可能会弹出来挡住元素。Appium 默认会处理输入法的显示和隐藏，但个别定制系统（特别是小米 MIUI、华为 EMUI）的输入法行为可能不一致。如果 `send_keys` 出问题，换个输入法——模拟器默认的一般没问题。

### 点击

```python
element.click()
```

appium 的 `click()` 跟 selenium 一样简单。但 App 界面小、元素间距近，偶尔会因为坐标计算偏差点到隔壁元素。解决方案是用显示等待确认元素可点击后再点（第 4 章会展开）。

### App 独有的：屏幕滑动

Appium 里滑动不是操作元素，是操作屏幕。简单滑动：

```python
# 从屏幕中间往上滑（类似向上翻页）
size = driver.get_window_size()
start_x = size['width'] // 2
start_y = int(size['height'] * 0.8)
end_y = int(size['height'] * 0.2)

driver.swipe(start_x, start_y, start_x, end_y, duration=800)
```

`swipe` 五个参数：起点 x、起点 y、终点 x、终点 y、滑动时间（毫秒）。x 不变、y 从 80% 滑到 20%，就是向上翻。

**2026 年注意：** `swipe()` 在 Appium 3 里仍然可用但官方更推荐 W3C Actions API 来写复杂手势。`swipe()` 适合简单滚动，复杂的手势（长按拖拽、双指缩放）留到第 3 章专门讲。

---

## 第七步：断言

跟 Selenium 一模一样，没有任何区别。

```python
# 断言元素可见
element = driver.find_element(AppiumBy.ID, "com.android.settings:id/search_action_bar")
assert element.is_displayed(), "搜索按钮应该可见但没有"

# 断言文字内容
search_input = driver.find_element(AppiumBy.ID, "android:id/search_src_text")
assert search_input.text == "WiFi", f"输入内容不对，期望 WiFi 实际 {search_input.text}"
```

`.text` 在 App 里返回的是元素的显示文字（相当于元素的 `text` 属性）。`.is_displayed()` 用法和 Selenium 完全一致。

---

## 完整链路实战：Settings App 搜索 WiFi

把以上六步串起来，用系统 Settings App 做一个完整的搜索流程：

```python
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === 第一步：配置 ===
options = UiAutomator2Options()
options.platform_name = "Android"
options.automation_name = "UiAutomator2"
options.device_name = "emulator-5554"
options.app_package = "com.android.settings"
options.app_activity = ".Settings"

# === 第二步：连接 ===
driver = webdriver.Remote("http://localhost:4723", options=options)
driver.implicitly_wait(10)

# === 第三步：定位搜索按钮并点击 ===
# 注意：这个 ID 是原生 Android 的，不同品牌手机可能不同
search_btn = driver.find_element(
    AppiumBy.ID, "com.android.settings:id/search_action_bar"
)
search_btn.click()

# === 第四步：输入搜索词 ===
search_input = driver.find_element(
    AppiumBy.ID, "android:id/search_src_text"
)
search_input.send_keys("WiFi")

# === 第五步：等待搜索结果出现 ===
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (AppiumBy.ID, "com.android.settings:id/search_results")
    )
)

# === 第六步：断言 ===
# 页面标题变成了搜索模式，标题应该是 "Settings" 或者带 "WiFi"
page_title = driver.find_element(
    AppiumBy.CLASS_NAME, "android.widget.TextView"
)
# 至少有结果显示
search_results = driver.find_elements(
    AppiumBy.ID, "com.android.settings:id/search_results"
)
assert len(search_results) > 0, "搜索结果为空"

print("✅ Settings 搜索 WiFi 流程测试通过")

# === 第七步：关闭 ===
driver.quit()
```

### 这个脚本在不同手机上能跑通吗？

**不一定。** 原因下面的对比说清楚。

### Selenium vs Appium 代码对比

把 Selenium 百度搜索和 Appium Settings 搜索放一起看：

```python
# Selenium 百度搜索
driver = webdriver.Chrome()
driver.get("https://www.baidu.com")
driver.find_element(By.ID, "kw").send_keys("Selenium")
driver.find_element(By.ID, "su").click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located(...))
assert "Selenium" in driver.title
```

```python
# Appium Settings 搜索
options = UiAutomator2Options()
options.platform_name = "Android"
options.app_package = "com.android.settings"
options.app_activity = ".Settings"
driver = webdriver.Remote("http://localhost:4723", options=options)
driver.find_element(AppiumBy.ID, "...").click()
driver.find_element(AppiumBy.ID, "...").send_keys("WiFi")
WebDriverWait(driver, 10).until(EC.presence_of_element_located(...))
assert len(results) > 0
```

**99% 相似。** 唯一区别就是启动方式和导入的 By 类不同。这就是 Appium 最大的优势——如果你会 Selenium，你已经会了 80% 的 Appium。

---

## 不推荐的方案：两种新手常见错误

### ❌ 用 `time.sleep()` 等 App 启动

```python
driver = webdriver.Remote("http://localhost:4723", options=options)
time.sleep(5)  # 等 App 启动
```

`webdriver.Remote()` 返回的时候 App 的启动 Activity 已经完成了渲染。不需要再等 5 秒。Appium Server 在创建 Session 阶段会自己等 App 启动。

唯一需要等的是 App 启动后还有二次加载的情况——比如开屏广告、权限弹窗。这些等的策略在第 4 章讲。

### ❌ 看到 App 里有 WebView 就用 Web 的 By 定位

混合应用（App 里嵌套网页）里面的元素要用 WebView 的定位方式，但你必须先切换到 WebView 的 Context。没切换就直接定位，App 端永远找不到 Web 里的元素。这个在第 5 章展开。

---

## 接下来

你现在已经能连上 App、打开页面、找元素、操作、断言了。但如果你试过在 Settings App 之外的其他 App 里找元素，你应该已经体会到了——**元素定位在 App 里比 Web 痛苦**。ID 又长又丑，很多元素根本没 ID，XPath 写起来比 Web 恶心得多。

下一章就干这个——把 App 端的各种定位方式拆碎了揉开了讲。哪个最稳、哪个最坑、哪个在 2026 年已经不推荐用了。

---

> 下一篇：《Appium 元素定位深度讲解：Accessibility ID、ID、XPath、UIAutomator Selector，每种定位方式的使用场景和坑》

#Appium #App自动化 #Python测试 #元素定位 #软件测试

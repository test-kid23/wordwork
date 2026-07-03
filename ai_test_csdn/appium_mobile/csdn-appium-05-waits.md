# Appium 等待与同步：App 自动化比 Web 多了哪些「等」

> Web 端的等待是页面加载完就行。App 端的等待复杂得多——App 启动要等、页面切换要等、网络请求要等、键盘弹起收起要等、Toast 一闪而过你的断言要刚好截住它。这一篇把 App 端所有需要「等」的场景逐个拆了。

---

## App 端等待跟 Web 端的核心区别

Web 端的等待几乎只跟 DOM 加载有关——等元素出现、等元素可见、等元素消失。

App 端多了四个等：

1. **等 App 启动。** App 从点击图标到首屏可见，比浏览器打开 URL 慢且不稳定。
2. **等页面切换动画。** App 的页面过渡比 Web 的页面跳转慢，而且有些动画没法被 Appium 直接感知。
3. **等网络请求。** App 里的列表数据、图片、内容几乎全是异步加载的，你滑到哪加载到哪。
4. **等系统级 UI。** 键盘弹出、Toast 消息、权限弹窗——这些不在你的 App 元素树里。

---

## 一、隐式等待——用法跟 Selenium 完全一致

```python
driver = webdriver.Remote("http://localhost:4723", options=options)
driver.implicitly_wait(10)
```

生效逻辑跟 Selenium 一模一样：`find_element` 时如果元素不在元素树中，反复尝试，最多等 10 秒。

**一个 App 特有的建议：** 把隐式等待设成 10-15 秒，比 Web 端大一点。因为 App 首次启动、冷启动数据加载通常比 Web 慢。而且隐式等待找到了立刻返回，不浪费太多时间。

---

## 二、显式等待——WebDriverWait 也可以用

Appium 底层的 WebDriver 协议跟 Selenium 同源——所以 `WebDriverWait` 和 `expected_conditions` 可以直接用。

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

element = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((AppiumBy.ID, "com.example:id/main_list"))
)
```

跟 Selenium 一样的是：
- `presence_of_element_located` ——元素在元素树里
- `visibility_of_element_located` ——元素在元素树里且可见
- `element_to_be_clickable` ——元素可见且能点
- `invisibility_of_element_located` ——元素消失

**跟 Selenium 不一样的是：** 即使元素 `is_displayed()` 返回 `True`，它在 App 端可能因为页面过渡动画还在播放而导致 `click()` 失效。Appium 的点击走的是坐标事件——动画中的元素坐标可能还在变。

这时候多等半秒比什么都靠谱：

```python
import time

btn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((AppiumBy.ID, "com.example:id/btn"))
)
time.sleep(0.5)  # 唯一合法用途：等动画尘埃落定
btn.click()
```

0.5 秒的 `time.sleep` 在动画场景下不叫「硬等」——叫「给动画一个结束的机会」。因为 Appium 的 EC 条件检测不到原生动画是否结束。

---

## 三、App 端独有的四种等待场景

### 场景一：等 App 启动完成

`webdriver.Remote(...)` 在 Appium 3 里默认会等到 App 启动并可以接收操作时才返回。但如果你用的是 `appActivity` 启动了一个有启动页/广告页的 App——启动页切换耗时长，你的 `find_element` 可能还在启动页上找首页的元素。

**做法：等首页的某个特征元素出现。**

```python
driver = webdriver.Remote("http://localhost:4723", options=options)

# 等首页的某个标志性元素出现——说明启动完成
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((AppiumBy.ID, "com.example.app:id/main_tab"))
)
# 超时给 30 秒——冷启动真的可能这么慢
```

如果超时了还没等到，检查：
- 启动 Activity 配置错了？`appActivity` 没写对导致 App 开的是别的页面
- App 启动时弹出了权限请求弹窗？弹窗挡住了首页，用 `driver.tap()` 先点掉权限弹窗

---

### 场景二：等页面切换完成

App 的页面之间切换有动画（滑动进入、淡入淡出）。如果在动画过程中找元素——Appium 可能找到的是切换前的旧页面元素，也可能元素树还没更新。

```python
# 点击跳转按钮
driver.find_element(AppiumBy.ID, "com.example:id/settings_btn").click()

# 等新页面的特征元素出现——说明切换完成
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((AppiumBy.ID, "com.example:id/settings_title"))
)
```

规律：**每次页面跳转/切 Tab 之后，等新页面上的某个独一无二的元素出现。** 这个元素最好是标题栏文字或页面专有的按钮——每个页面总有至少一个独一无二的 UI 元素。

---

### 场景三：等网络数据加载

列表数据、详情信息、搜索结果——App 的数据渲染几乎全是异步的。你的脚本可能跑太快，列表还没加载完就去数有几条数据了。

```python
# 搜索
search_input = driver.find_element(AppiumBy.ID, "com.example:id/search_bar")
search_input.send_keys("耳机")

# 等一下列表加载——用自定义条件
WebDriverWait(driver, 10).until(
    lambda d: len(d.find_elements(AppiumBy.ID, "com.example:id/product_item")) >= 3
)
# 等到至少有 3 条结果

# 或者等 loading 指示器消失
WebDriverWait(driver, 10).until(
    EC.invisibility_of_element_located((AppiumBy.ID, "com.example:id/loading_spinner"))
)
```

**两种策略选一个：**
- 等 loading 动画消失（`invisibility_of_element_located`）——适合 App 明确有 loading 动画
- 等数据数量达到预期（`lambda` 自定义条件）——适合没有 loading 动画或者 loading 动画不稳定

没有 loading 动画是大多数 App 的常态。这种情况下用 `lambda` 自定义条件。

---

### 场景四：等 Toast 消息——Appium 最难等的那个

Toast 是 Android 的小浮层提示——「保存成功」「网络错误」「请输入手机号」。它出现 2 秒后自动消失。

```python
# ❌ 这样等不到——Toast 出现的速度太快，还没等你的断言执行完它就消失了
driver.find_element(AppiumBy.ID, "save_btn").click()
toast = driver.find_element(AppiumBy.XPATH, "//*[contains(@text, '保存成功')]")
assert toast.is_displayed()

# ✅ 正确做法：用显式等待等 Toast 出现
from selenium.webdriver.support import expected_conditions as EC

driver.find_element(AppiumBy.ID, "save_btn").click()

toast = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((
        AppiumBy.XPATH, "//*[contains(@text, '保存成功')]"
    ))
)
assert toast is not None
```

Toast 的 XPath 用 `contains(@text, '...')` 而不是精确匹配——因为 Android 的 Toast 文本前后可能会被系统加空格或换行。

**如果 Toast 实在是抓不到：**

有些 App 用了自定义 Toast 组件而非系统 Toast。自定义 Toast 在元素树里可能不存在——这是 Appium 的已知痛点。

换一种验证思路——不验证 Toast 本身，验证 Toast 提示之后的状态变化：

```python
driver.find_element(AppiumBy.ID, "save_btn").click()

# 不验证「保存成功」Toast——验证表单关闭或者数据出现在列表里
WebDriverWait(driver, 5).until(
    EC.invisibility_of_element_located((AppiumBy.ID, "edit_form"))
)
# 表单消失了，说明保存成功了
```

---

## 四、键盘相关的等待

键盘弹出和收起也是异步的——动画需要时间。

```python
element = driver.find_element(AppiumBy.ID, "input_field")
element.click()

# 键盘弹起需要时间——等一下再找「输入框下面的按钮」
time.sleep(0.5)  # 这个 sleep 是防键盘弹起动画的
driver.hide_keyboard()

# 键盘收起也需要时间
time.sleep(0.3)
```

键盘弹起和收起——这是我觉得 `time.sleep` 可以被容忍的极少数场景之一。0.3-0.5 秒的固定等待比写复杂的条件判断更省心。

---

## 五、App 启动和 Activity 切换的等待规则

### 冷启动 vs 热启动

```python
# 冷启动——App 首次启动或被杀进程后启动
driver = webdriver.Remote("http://localhost:4723", options=options)
# Remote() 返回时 App 已经启动了，但启动页可能还没跳过
# 给首页特征元素 30 秒的超时

# 热启动——App 在后台切回来
driver.background_app(5)
# background_app 返回时 App 已经回到前台，几乎不需要额外等
# 但有些 App 切回来会刷新数据——等 loading 消失
WebDriverWait(driver, 5).until(
    EC.invisibility_of_element_located((AppiumBy.ID, "com.example:id/refresh_progress"))
)
```

### Activity 跳转

```python
# 从当前 App 跳到另一个 App 的某个页面
driver.start_activity("com.android.settings", ".WifiSettings")

# 等目标页面元素出现
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((AppiumBy.ID, "com.android.settings:id/switch_bar"))
)
```

---

## 六、一个完整的等待实战

打开 App → 登录 → 等首页加载 → 搜索商品 → 等搜索结果 → 点击第一个 → 等详情页加载 → 验证。

```python
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = UiAutomator2Options()
options.platform_name = "Android"
options.automation_name = "UiAutomator2"
options.device_name = "emulator-5554"
options.app_package = "com.shop.app"
options.app_activity = ".MainActivity"
driver = webdriver.Remote("http://localhost:4723", options=options)
driver.implicitly_wait(8)

# === 等 App 启动完成（首页标志性元素出现） ===
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((AppiumBy.ID, "com.shop.app:id/home_tab"))
)

# === 登录 ===
driver.find_element(AppiumBy.ID, "com.shop.app:id/mine_tab").click()
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((AppiumBy.ID, "com.shop.app:id/username_input"))
)
driver.find_element(AppiumBy.ID, "com.shop.app:id/username_input").send_keys("test_user")
driver.find_element(AppiumBy.ID, "com.shop.app:id/password_input").send_keys("pass123")

login_btn = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((AppiumBy.XPATH, "//android.widget.Button[@text='登录']"))
)
login_btn.click()

# === 等登录成功回到首页 ===
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((AppiumBy.ID, "com.shop.app:id/home_tab"))
)

# === 搜索商品 ===
driver.find_element(AppiumBy.ID, "com.shop.app:id/search_bar").click()
driver.find_element(AppiumBy.ID, "com.shop.app:id/search_input").send_keys("耳机")

search_btn = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((
        AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("搜索")'
    ))
)
search_btn.click()

# === 等搜索结果加载（至少有 1 条结果） ===
WebDriverWait(driver, 10).until(
    lambda d: len(d.find_elements(AppiumBy.ID, "com.shop.app:id/product_item")) >= 1
)

# === 点第一个商品 ===
products = driver.find_elements(AppiumBy.ID, "com.shop.app:id/product_item")
products[0].click()

# === 等详情页加载（价格元素出现） ===
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((AppiumBy.ID, "com.shop.app:id/product_price"))
)

# === 验证价格不为空 ===
price = driver.find_element(AppiumBy.ID, "com.shop.app:id/product_price").text
assert price != "", "商品价格不应为空"
print(f"✅ 商品价格：{price}")

driver.quit()
```

这个脚本里每一处等待都有明确目的：
- 30 秒等启动——冷启动慢
- 元素出现等页面切换——每次切换都等
- `element_to_be_clickable` 等按钮——点之前确保就绪
- `lambda` 等数据——异步加载没有明确结束信号

---

## ❌ 等待相关的三个错误习惯

### 1. 每次找元素前都 sleep(3)

```python
time.sleep(3)
element1 = driver.find_element(...)
time.sleep(3)
element2 = driver.find_element(...)
```

这不如用 `implicitly_wait(10)` ——一次设置全局生效。

### 2. 只用隐式等待，不用显式等待

隐式等待等不了「元素可点击」「元素消失」「数据加载完成」。App 端的异步操作比例比 Web 高得多——不用显式等待等于裸奔。

### 3. Toast 断言不等待

```python
driver.find_element(...).click()
toast = driver.find_element(...)  # Toast 已经消失了！
```

Toast 的存活时间极短（通常 2 秒），必须在点击后**立刻**用显式等待拦截。

---

## 写在最后

如果说元素定位占了你写脚本 80% 的时间，那等待策略占了你调试脚本 80% 的时间。「时好时坏」的用例，十有八九是等待没加对。

这一章是 Appium 教程里分水岭的一章。之前的章节，你学会了「能做什么」。这一章之后，你学会了「怎么做才稳」。下一篇讲混合应用与 WebView——App 里嵌 H5 页面的全流程处理，那才是真正的移动端自动化硬骨头。

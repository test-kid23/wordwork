# Appium 基础操作与手势：写出「像人在操作手机」的脚本

> 前两章你学会了环境搭建和元素定位。现在元素找到了，接下来你对它能做什么？Web 端只有 click 和 send_keys，App 端不一样——tap、长按、滑动、拖拽、双指缩放……这些才是移动端自动化的精华。

---

## App 操作全景：比你想象的多

```
Web  (Selenium)：click | send_keys | clear | submit
App  (Appium)：  tap | send_keys | swipe | long_press | drag | pinch/zoom | 键盘控制
```

App 端操作分两大类：
- **元素操作**：对已经找到的元素执行（click、send_keys、clear）
- **屏幕操作**：操作的是屏幕坐标区域（tap、swipe、pinch）——你有没有找到元素不重要，你可以在屏幕任意位置执行动作

屏幕操作是 Appium 的独门绝技。你写 Selenium 的时候不会想「在屏幕坐标 500,800 点击」，但在 Appium 里你经常会这么干——因为有些控件在元素树里根本不存在，只能靠坐标。

---

## 一、元素操作——跟 Web 差不多但有几个坑

### click()——最基础也最容易炸

```python
element = driver.find_element(AppiumBy.ID, "com.example:id/btn")
element.click()
```

App 端的 `click()` 跟 Web 端同一个方法名，背后的机制不一样。Appium 的 click 在 Android 上是通过 UiAutomator2 往屏幕坐标发一个 tap 事件——它先算出元素的中心坐标，然后 `tap(x_center, y_center)`。

两个 App 端独有的坑：

**坑一：元素坐标计算偏移。** 全屏/沉浸式 App 里，状态栏和导航栏高度影响了坐标系。Appium 有时会算错——你以为在点「确认」，实际击点了上方 50px 的「返回」。遇到这种情况把 App 退出全屏模式再测。

**坑二：元素重叠。** App 界面小、弹出层多——Toast 提示、键盘、下拉菜单都可能挡住目标元素。Appium 遇到被遮挡的元素会报 `ElementClickInterceptedException`。解决办法是等待遮挡层先消失（下一章展开讲）。

---

### send_keys()——App 端输入有多坑

```python
element = driver.find_element(AppiumBy.ID, "com.example:id/input")
element.send_keys("hello world")
```

这行看上去跟 Selenium 一模一样。但如果你在中文 App 里输英文、或者在英文系统里输中文——各种奇怪问题就来了。

**常见问题：**

1. **输入法弹窗挡住输入框。** Appium 3 默认在 `send_keys` 前收起键盘、输完后再收起。但国产 ROM（MIUI、ColorOS）有时候不受控，键盘收起来了但下面的输入框还在键盘区域上面——导致下一次 `find_element` 失效。解法：`driver.hide_keyboard()` 手动收键盘。

2. **中文输入。** `send_keys("中文")` 在某些 App 里只会输入拼音字母不会触发输入法。这不是 Appium 的 bug——`send_keys` 走的是底层的 `setText` API，它不经过输入法引擎。如果 App 的业务逻辑跟输入法绑定（比如输入框字数限制通过输入法事件触发），`send_keys` 可能绕过那个校验。

3. **安全键盘。** 银行 App 和支付页面的自定义安全键盘不是标准控件，元素树里看不到它。碰上这种页面，自动化只能放弃这部分或者用截图 OCR 辅助。

**建议：** 测试数据用英文和数字。把中文输入留到必须的业务场景（比如测试拼音搜索建议）里专门处理。

---

### clear()——先清再输

```python
element.clear()
element.send_keys("新内容")
```

跟 Selenium 一样，输入前先清空。`clear()` 在 App 端也是用底层 `setText("")` 实现，不走删除键逐字删。

---

## 二、屏幕操作——Appium 的真正杀手锏

以下所有屏幕操作都需要先拿到屏幕尺寸：

```python
size = driver.get_window_size()
width = size['width']
height = size['height']
```

---

### tap()——点击屏幕任意位置

```python
from appium.webdriver.common.appiumby import AppiumBy

# 方式一：点元素（首选——因为稳定）
element = driver.find_element(AppiumBy.ID, "com.example:id/btn")
element.click()  # 等价于 tap 元素中心

# 方式二：点坐标（万不得已才用——换设备就偏）
driver.tap([(500, 800)], duration=100)
```

`tap()` 的 `duration` 参数是指触控持续时间，单位毫秒。`duration=100` 就是轻点一下，跟手指快速点一下一样。

**什么时候必须用坐标 tap？**

- 元素在元素树里不存在（Canvas 绘制的图形、游戏引擎渲染的界面）
- 系统级弹窗（权限请求弹窗——部分 ROM 上这类弹窗不在 App 元素树里）
- 你只是想点屏幕空白处收起某个弹出层

**坐标 tap 的保命技巧：用百分比，不用绝对像素。**

```python
# ❌ 绝对坐标——换设备就废
driver.tap([(540, 960)])

# ✅ 百分比——通用
size = driver.get_window_size()
x = int(size['width'] * 0.5)   # 屏幕正中间
y = int(size['height'] * 0.3)  # 上方 30% 位置
driver.tap([(x, y)])
```

---

### swipe()——四方向滑动

```python
# 从 (x1, y1) 滑到 (x2, y2)，duration 毫秒
driver.swipe(x1, y1, x2, y2, duration=500)
```

用封装函数把四个方向固定下来：

```python
def swipe_up(driver, duration=500):
    size = driver.get_window_size()
    x = size['width'] // 2
    start_y = int(size['height'] * 0.8)
    end_y = int(size['height'] * 0.2)
    driver.swipe(x, start_y, x, end_y, duration)

def swipe_down(driver, duration=500):
    size = driver.get_window_size()
    x = size['width'] // 2
    start_y = int(size['height'] * 0.2)
    end_y = int(size['height'] * 0.8)
    driver.swipe(x, start_y, x, end_y, duration)

def swipe_left(driver, duration=500):
    size = driver.get_window_size()
    y = size['height'] // 2
    start_x = int(size['width'] * 0.8)
    end_x = int(size['width'] * 0.2)
    driver.swipe(start_x, y, end_x, y, duration)

def swipe_right(driver, duration=500):
    size = driver.get_window_size()
    y = size['height'] // 2
    start_x = int(size['width'] * 0.2)
    end_x = int(size['width'] * 0.8)
    driver.swipe(start_x, y, end_x, y, duration)
```

四个方向说穿了就是改变起点和终点的坐标比例。横向滑改变 x、y 不变；纵向滑改变 y、x 不变。

**duration 的讲究：**

- `duration=200`：快速滑动（翻页、切 Tab），像手指快速划过
- `duration=800~1000`：慢速滑动（像慢慢拖动查看内容），给 App 时间加载新内容

有些列表是懒加载的——你快速滑到底部，底部的内容还没加载出来。用 `duration=1000` 慢滑，给 App 一点时间渲染。

---

### scroll——滑动到某个元素可见

`swipe()` 是你自己算坐标滑动。`scroll()` 是告诉 Appium「把那个元素滑到屏幕里」：

```python
# Appium 3 推荐写法：用 UiAutomator 的 scrollIntoView
element = driver.find_element(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiScrollable(new UiSelector().scrollable(true))'
    '.scrollIntoView(new UiSelector().text("目标文字"))'
)
element.click()
```

这行干了什么：在可滚动的列表里，把文字是「目标文字」的元素滑动到屏幕可见区域。滑到了再点。

**`scroll()` 跟 `swipe()` 的区别：** `swipe()` 是「往某个方向滑动固定距离」，`scroll()` 是「把指定元素找出来放在屏幕上」。如果元素就在当前屏幕上，`scroll()` 不执行任何滑动。`swipe()` 不管你元素在哪都执行滑动。

---

### long_press()——长按

```python
from appium.webdriver.common.touch_action import TouchAction

element = driver.find_element(AppiumBy.ID, "com.example:id/item")

TouchAction(driver).long_press(element, duration=2000).release().perform()
# 在目标元素上长按 2 秒
```

长按最常见的场景：删除操作（长按图标出现删除菜单）、多选模式（长按进入编辑状态）、文本选择（长按出选中和复制菜单）。

不用 `TouchAction` 的替代写法（Appium 3 推荐 W3C Actions API）：

```python
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction

actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
actions.pointer_action.move_to(element)
actions.pointer_action.pointer_down()
actions.pointer_action.pause(2.0)  # 按住 2 秒
actions.pointer_action.pointer_up()
actions.perform()
```

实话实说——W3C 写法是官方推荐的方向，但 `TouchAction` 长了几年没被移除，用起来简单得多。入门阶段用 `TouchAction` 完全行。等 Appium 哪天真的不兼容了再迁到 W3C。

---

### 拖拽：drag_and_drop()

```python
from appium.webdriver.common.touch_action import TouchAction

source = driver.find_element(AppiumBy.ID, "com.example:id/drag_handle")
target = driver.find_element(AppiumBy.ID, "com.example:id/drop_zone")

TouchAction(driver) \
    .long_press(source, duration=1000) \
    .move_to(target) \
    .release() \
    .perform()
```

拖拽本质是「长按 + 移动 + 松开」。常见场景：拖拽排序（任务列表、相册排列）、滑块验证码、地图拖拽。

---

### 双指缩放：pinch / zoom

```python
# 缩小（双指向中间捏）
driver.pinch(element=None, percent=200, steps=50)
# percent=200 → 缩小到原来的 200%（相当于两指间距缩小了 50%）
# steps=50 → 分 50 步动画执行，步数越多动画越平滑

# 放大（双指向外扩）——没有 zoom() 方法，用 pinch 的 percent<100
driver.pinch(element=None, percent=50, steps=50)
# percent=50 → 缩小到 50% 相当于放大两倍。反向思维，别搞混
```

如果传入 `element`，双指操作的中心点在该元素上。不传则用屏幕中心。

我坦白说——双指缩放在自动化里用到的是极少数场景（地图 App 测试、图片浏览测试）。大多数 App 测试到你这里就够用了。

---

## 三、键盘控制——App 自动化绕不开的头痛环节

```python
# 收起键盘（如果当前有键盘在屏幕上）
driver.hide_keyboard()

# 发送 Android 按键事件（仅 Android）
driver.press_keycode(66)   # 66 = ENTER 键
driver.press_keycode(4)    # 4 = BACK 返回键
driver.press_keycode(3)    # 3 = HOME 键
driver.press_keycode(26)   # 26 = POWER 电源键
driver.press_keycode(24)   # 24 = VOLUME_UP 音量+
```

常用 keycode 速查：
| keycode | 含义 |
|---------|------|
| 3 | HOME |
| 4 | BACK |
| 24 | 音量+ |
| 25 | 音量- |
| 26 | 电源键 |
| 66 | ENTER |
| 67 | DELETE（退格删除） |
| 84 | 搜索键 |

```python
# 隐藏键盘的另一种方式：按返回键
driver.press_keycode(4)  # 按 BACK 通常也能收起键盘
```

`hide_keyboard()` 也不是万能的。某些定制 ROM 里键盘收不起来或者收起后页面没有恢复原位。这时候用 `press_keycode(4)` 暴力按返回键通常能救急。

---

## 四、App 状态控制

```python
# 把 App 切到后台（模拟用户按 Home 键出去）
driver.background_app(5)  # 切到后台 5 秒再回来

# 关闭当前 App
driver.terminate_app("com.example.app")

# 重新启动 App
driver.activate_app("com.example.app")

# 安装 App（APK 路径需要是设备上的路径或 URL）
driver.install_app("/sdcard/app-debug.apk")

# 卸载 App
driver.remove_app("com.example.app")

# 获取当前 App 的包名和 Activity
print(driver.current_package)
print(driver.current_activity)

# 启动另一个 App 的 Activity
driver.start_activity("com.android.settings", ".Settings")
```

`background_app()` 特别好用——测试 App 从后台切回前台的状态恢复逻辑。很多 App 的 bug 就在这里：切到后台过一会再回来，登录状态丢了、页面白屏了、数据不刷新了。

---

## 五、一个综合实战：电商 App 商品筛选

完整场景：打开 App → 搜索「耳机」→ 长按第一个商品进入多选模式 → 滑动列表找到目标商品 → 点击 → 加购物车 → 验证。

```python
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction

# === 连接 ===
options = UiAutomator2Options()
options.platform_name = "Android"
options.automation_name = "UiAutomator2"
options.device_name = "emulator-5554"
options.app_package = "com.shop.app"
options.app_activity = ".MainActivity"
driver = webdriver.Remote("http://localhost:4723", options=options)

# === 搜索 ===
driver.find_element(AppiumBy.ID, "com.shop.app:id/search_bar").click()
driver.find_element(AppiumBy.ID, "com.shop.app:id/search_input").send_keys("耳机")
driver.find_element(
    AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("搜索")'
).click()

# === 长按第一个商品，假设弹出多选菜单 ===
first_item = driver.find_elements(AppiumBy.ID, "com.shop.app:id/product_card")[0]
TouchAction(driver).long_press(first_item, duration=1500).release().perform()

# === 滑动列表到底部 ===
size = driver.get_window_size()
driver.swipe(
    size['width'] // 2,        # 屏幕中间 x
    int(size['height'] * 0.8), # 底部 80%
    size['width'] // 2,
    int(size['height'] * 0.3), # 滑到 30%（向上翻）
    duration=1000               # 慢滑——等懒加载
)

# === 用 scroll 找目标商品 ===
target = driver.find_element(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiScrollable(new UiSelector().scrollable(true))'
    '.scrollIntoView(new UiSelector().text("降噪耳机 Pro"))'
)
target.click()

# === 加购物车 ===
add_btn = driver.find_element(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().text("加入购物车")'
)
add_btn.click()

# === 验证：看 toast 或者购物车角标 ===
# 切到后台再回来（验证状态保持）
driver.background_app(2)

cart_badge = driver.find_element(AppiumBy.ID, "com.shop.app:id/cart_badge")
assert cart_badge.text == "1", f"购物车数量应为 1，实际为 {cart_badge.text}"

print("✅ 商品筛选 + 加购链路完成")
driver.quit()
```

脚本里用了：`click`、`send_keys`、`long_press`、`swipe`、`scroll`、`background_app`、`find_elements` 取第一个、UiAutomator Selector 按文字。动作类型覆盖了 App 自动化最常见的场景。

---

## ❌ 两种别学的「手势写法」

### 1. ActionChains（Selenium 遗留）

```python
# ❌ 别在 Appium 里这么用
from selenium.webdriver.common.action_chains import ActionChains
ActionChains(driver).move_to_element(element).click().perform()
```

`ActionChains` 是给 Web 端设计的（鼠标操作）。App 端没有鼠标，用 `TouchAction` 或 W3C Actions API。

### 2. execute_script("mobile: swipe") 旧式脚本

```python
# ❌ Appium 1.x 时代的老写法
driver.execute_script("mobile: swipe", {"direction": "up"})
```

Appium 2 之后官方不建议用 `execute_script` 调 `mobile:` 命令，很多命令已经被移除或改名。直接用 `driver.swipe()` ——简洁且不被未来的版本干掉。

---

## 写在最后

Appium 的手势操作比 Selenium 丰富得多。你仔细想想——你用手机时 90% 的动作就是本篇覆盖的这些：点、滑、长按、输入。剩下的捏合缩放、多指手势、摇一摇——要么很少用到，要么平台差异大到根本不值得花篇幅讲。

掌握了这些，你就能写出「看起来像人在操作手机」的脚本。下一篇讲 App 端的等待与同步——Web 端有显式等待隐式等待，App 端多了一层：App 启动要等、页面切换要等、网络请求要等、Toast 弹窗要等。那才是 App 自动化稳定性真正的分水岭。

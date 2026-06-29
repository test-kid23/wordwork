# Selenium 等待机制：让你的脚本比页面慢一步

> 你定位写对了，操作写对了，断言写对了——但脚本还是挂了。看一眼报错：`NoSuchElementException`。再看一眼页面：元素明明在。问题出在哪？你的脚本跑得比页面渲染快。

---

## 一句话讲清楚等待的本质

自动化脚本运行速度是毫秒级的。浏览器渲染页面是秒级的。

你点了搜索按钮，浏览器在请求后端、渲染结果、加载图片——这个过程可能 0.5 秒，可能 3 秒。你的脚本不管你，点了搜索之后下一毫秒就去 `find_element` 找结果列表。结果列表还没渲染出来——挂了。

**等待机制的本质：让你的脚本「等一等」，等到页面准备好再往下走。**

---

## 三种等待：谁来等、等多久、等到什么

Selenium 提供三种等待方式。名字像，但用法完全不同。

| 等待类型 | 作用范围 | 等多久 | 一句话 |
|----------|---------|--------|--------|
| `time.sleep()` | 固定时间 | 硬编码秒数 | ❌ 不是 Selenium 的等待，写死了等多久 |
| 隐式等待 `implicitly_wait` | 全局（整个 driver 生命周期） | 设置一个最大值，找到了立刻走 | 找元素时如果元素还没出现，最多等 N 秒 |
| 显式等待 `WebDriverWait` | 单次、指定条件 | 设置一个最大值 + 一个具体条件 | 等到「某个条件成立」或者超时 |

---

## 一、`time.sleep()`——为什么它是不及格的等待

```python
import time

driver.find_element(By.ID, "search-btn").click()
time.sleep(3)  # 硬等 3 秒
driver.find_element(By.ID, "result-list")
```

**三个致命问题：**

1. **浪费时间。** 如果页面 0.5 秒就渲染完了，剩下 2.5 秒在发呆。一个测试套件 100 条用例，每条发呆 2.5 秒 = 4 分钟干等。

2. **不够长。** CI/CD 环境比本地慢，你那 3 秒在 CI 上可能不够——又挂了。

3. **没有条件判断。** `time.sleep()` 只知道「过了 3 秒」，不知道「页面有没有渲染完」。你只能在 3 秒和 5 秒之间猜，永远猜不准。

**唯一的「合法」使用场景：** 调试时临时插一行 `time.sleep(2)` 看页面状态，确认问题不是等待引起的。确认之后立刻删掉换成显式等待。

---

## 二、隐式等待——全场兜底

```python
driver = webdriver.Chrome()
driver.implicitly_wait(10)  # 全局生效
```

生效逻辑：之后每一次 `find_element` / `find_elements`，如果元素在 DOM 中不存在，Selenium 会反复尝试查找，最多等 10 秒。10 秒内找到了就立刻返回，不再等。

第 1 章就让你加了这行。但有个关键问题第 1 章刻意没展开——**隐式等待只管「元素存不存在于 DOM」，不管元素能不能点、能不能看、有没有文字。**

```python
# 隐式等待能解决：
driver.find_element(By.ID, "btn")  # 等 btn 出现在 DOM 里

# 隐式等待解决不了：
btn = driver.find_element(By.ID, "btn")
btn.click()  # 元素在 DOM 里，但被另一个弹窗挡住了——隐式等待不管这个
```

所以实际项目里隐式等待只当兜底，不当代替品。主力是显式等待。

---

## 三、显式等待——这才是你要主用的

### 基础语法

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "result-list"))
)
```

三个组成部分：
- **`driver`** ——在哪个浏览器窗口等
- **`10`** ——最多等 10 秒（跟隐式等待一样，找到了立刻停止）
- **`EC.xxx`** ——等到什么条件成立

---

### 最常用的 6 个 Expected Conditions

```python
from selenium.webdriver.support import expected_conditions as EC

# 1. presence_of_element_located —— 元素出现在 DOM（最常用）
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "login-form"))
)
# 注意：元素在 DOM 但 display:none 也算通过。只保证 DOM 里有。

# 2. visibility_of_element_located —— 元素在 DOM 里且可见（更严格）
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "error-msg"))
)
# 要 DOM 有、而且 display 不是 none、而且宽高大于 0。

# 3. element_to_be_clickable —— 元素可见且可被点击（最严格）
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "submit-btn"))
)
# click 之前用这个。确保按钮既可见又不被挡住。

# 4. text_to_be_present_in_element —— 元素的文字变成了某个值
WebDriverWait(driver, 10).until(
    EC.text_to_be_present_in_element((By.ID, "status"), "保存成功")
)
# 等那个 span 的文字变成「保存成功」。适用于异步更新结果的场景。

# 5. alert_is_present —— 弹窗出现了
WebDriverWait(driver, 5).until(EC.alert_is_present())
alert = driver.switch_to.alert
alert.accept()

# 6. invisibility_of_element_located —— 元素消失了
WebDriverWait(driver, 10).until(
    EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loading-spinner"))
)
# 等 loading 转圈消失。很适合等 Ajax 请求完成。
```

---

### presence vs visibility vs clickable 怎么选

```html
<div id="modal" style="display:none">
  <button id="confirm-btn">确认</button>
</div>
```

| 条件 | id="modal" | id="confirm-btn" | 什么时候用 |
|------|-----------|------------------|-----------|
| `presence` | ✅ 在 DOM | ✅ 在 DOM | 你只需要读元素文本，不操作它 |
| `visibility` | ❌ display:none | ❌ 父级不可见 | 你要操作或验证它但不需要点 |
| `clickable` | ❌ display:none | ❌ 父级不可见 | 你要点它 |

三者严格程度递增。**日常操作元素用 `visibility`，点按钮用 `clickable`，只读文本用 `presence` 也行。**

---

### 显式等待支持自定义条件

EC 包不是万能的。有的场景你需要自己写条件：

```python
# 等页面标题变成指定值
WebDriverWait(driver, 10).until(
    lambda d: d.title == "订单列表 - 管理后台"
)

# 等某个列表里至少有 5 条数据
WebDriverWait(driver, 10).until(
    lambda d: len(d.find_elements(By.CSS_SELECTOR, ".order-row")) >= 5
)

# 等某个元素的属性值变化
WebDriverWait(driver, 10).until(
    lambda d: d.find_element(By.ID, "progress").get_attribute("value") == "100"
)
```

`lambda d: ...` 里的 `d` 就是 `driver`。只要这行代码返回 `True`（或非空非零值），等待结束。

自定义条件给你完全的自由——你可以等任何你能用代码描述的状态。

---

## 四、隐式等待 + 显式等待能混用吗

**能，但有个坑。**

```python
driver.implicitly_wait(10)

# 这么写没问题——隐式等 10 秒 + 显式等 10 秒，两者独立
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "btn"))
)
```

看起来正常工作。但 Selenium 官方不推荐混用——因为两者的等待逻辑在某些边界情况下会互相干扰，导致实际等待时间变成隐式时间乘以显式时间。

**我的建议：**

```python
driver = webdriver.Chrome()
driver.implicitly_wait(5)   # 小值兜底（5 秒足够了）

# 需要精确等的地方上显式等待
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "submit-btn"))
).click()
```

隐式等待值设小一点（3-5 秒），当「页面瞬间渲染完」的最低保障。真正需要等的场景一律用显式等待。这样混用基本不会出问题。

---

## 五、每次 click / submit 之后都要等——一套习惯

给你一个可以直接套用的模式：

```python
# === 搜索并等结果 ===
driver.find_element(By.CSS_SELECTOR, "[placeholder='搜索']").send_keys("Python" + Keys.ENTER)

# 点击能触发页面变化的动作之后——加等待
results = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".search-result"))
)
assert len(results) > 0, "搜索结果不应为空"

# === 打开弹窗 ===
driver.find_element(By.ID, "open-modal-btn").click()

modal = WebDriverWait(driver, 5).until(
    EC.visibility_of_element_located((By.ID, "modal"))
)
assert modal.is_displayed()

# === 关闭弹窗 ===
driver.find_element(By.CSS_SELECTOR, "[aria-label='关闭']").click()

WebDriverWait(driver, 5).until(
    EC.invisibility_of_element_located((By.ID, "modal"))
)
```

三个动作后等待的规律：
- **页面跳转后** → `presence_of_element_located`（新页面某个特征元素出现）
- **点击触发弹窗/下拉后** → `visibility_of_element_located`（那个弹窗可见）
- **关闭弹窗/提交表单后** → `invisibility_of_element_located`（弹窗消失 / loading 消失）
- **点击之前** → `element_to_be_clickable`（确保能点）

---

## 六、一个完整的等待策略实战

登录后台 → 创建订单 → 等订单列表刷新 → 验证新订单出现。

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(3)  # 兜底
driver.get("https://admin.example.com/login")

# 等登录表单可见再操作
username = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, "username"))
)
password = driver.find_element(By.NAME, "password")
login_btn = driver.find_element(By.XPATH, "//button[text()='登录']")

username.send_keys("admin")
password.send_keys("pass123")
login_btn.click()

# 等登录完成——页面跳转后 dashboard 出现
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".dashboard"))
)

# 点创建订单按钮
create_btn = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "创建订单"))
)
create_btn.click()

# 等表单弹窗出现，填数据
order_form = WebDriverWait(driver, 5).until(
    EC.visibility_of_element_located((By.ID, "order-form"))
)
driver.find_element(By.NAME, "product").send_keys("测试商品")
driver.find_element(By.NAME, "amount").send_keys("1")

# 提交前确保提交按钮可点击
submit_btn = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, "//button[text()='提交']"))
)
submit_btn.click()

# 等弹窗消失 + 订单列表刷新
WebDriverWait(driver, 10).until(
    EC.invisibility_of_element_located((By.ID, "order-form"))
)
orders = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".order-row"))
)

# 断言新订单出现在列表里
order_texts = [o.text for o in orders]
assert any("测试商品" in t for t in order_texts), "❌ 新订单未出现在列表中"

print("✅ 订单创建流程通过")
driver.quit()
```

这条脚本里没有一行 `time.sleep()`。所有等待都是「等到某个条件成立才往下走」——跑得快的时候不浪费时间，跑得慢的时候不炸。

---

## ❌ 三个关于等待的错误认知

### 1. 「我加了 implicitly_wait 就够了」

不够。隐式等待只解决「元素还没出现在 DOM」的问题。元素在 DOM 但不可见、不可点击、文字还没更新——隐式等待全都管不了。

### 2. 「显式等待太啰嗦了，用 time.sleep 简单」

写 `time.sleep(3)` 确实比写三行 `WebDriverWait(...).until(...)` 快。但你的脚本跑一百遍，time.sleep 浪费的时间够你写完一千个显式等待。而且 CI 上的随机失败你每次都要花半小时排查——那才是真正的时间黑洞。

### 3. 「我每个操作都加一句 WebDriverWait」

过犹不及。同一个页面内连续操作几个已在 DOM 中的元素，不需要每次 `find_element` 前面都加显式等待。

```python
# ✅ 显式等待等「页面状态变化」（页面跳转、弹窗开关、数据刷新）
# ✅ 隐式等待兜底「普通元素加载」
# ❌ 不是每次 find_element 前面都需要 WebDriverWait
```

---

## 写在最后

等待机制不好，你的脚本就是「薛定谔的自动化」——在你本地能跑，在别人电脑上跑了三次过了两次。测试自动化的核心价值是**可信的重复执行**，而信任建立在稳定性上。稳定性的一半是定位策略，另一半就是等待。

你把等待策略搞对了，Selenium 的入门就结束了。下一篇讲浏览器操作与窗口管理——多窗口切换、Tab 管理、Cookie 操作、截图。那之后就是真枪实弹的实战系列了。

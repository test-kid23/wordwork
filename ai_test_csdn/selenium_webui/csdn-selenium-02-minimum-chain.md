# Selenium 最小可执行链路：启动 → 定位 → 操作 → 断言

> 上一章你打开了百度、打印了标题。但那不是自动化测试——那叫「用代码打开网页」。这一章，你要学会自动化测试最核心的四件事：找到元素、操作它、检查结果对不对、优雅地关掉浏览器。

---

## 先给你看一张完整的链路图

一个自动化用例，不管多复杂，拆到底就四个动作：

```
启动浏览器 → 打开页面 → [定位元素 → 操作元素] 循环 → 断言 → 关闭
```

这四个动作连起来，我管它叫「最小可执行链路」。这一篇用百度搜索一个完整例子帮你吃透这条链路。每个环节你后面会写几百上千遍的东西，这篇打好底。

---

## 第一步：启动浏览器

上一章你写了 `webdriver.Chrome()`，但实际项目里浏览器不是无脑启动就完事。有两个配置你迟早会用上。

### 窗口最大化

```python
from selenium import webdriver

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.baidu.com")
print(driver.title)
driver.quit()
```

就多了一行 `driver.maximize_window()`。为什么需要这个？因为有些页面元素在窗口缩小时会被隐藏（导航栏折叠成汉堡菜单），你定位元素时定位不到就会报错。**养成习惯，启动浏览器先最大化窗口。**

### 隐式等待——让你少写 100 个 time.sleep()

```python
driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)  # 这行加了之后，后面所有 find_element 都会自动等 10 秒
driver.get("https://www.baidu.com")
```

什么叫「自动等 10 秒」？

你打开百度，浏览器不会瞬间渲染完所有 DOM。如果页面还没加载完你就去 `find_element` 找输入框——元素还没出来，直接报 `NoSuchElementException`。

加了 `implicitly_wait(10)` 之后，Selenium 在找元素时如果元素还没出现，会反复去 DOM 里找，最多等 10 秒。10 秒内找到了就立刻往下走，不用傻等到 10 秒。

**这条东西能解决你 70% 的「用例时好时坏」问题。** 详细等待机制第 4 章会展开讲，现在你先记住：启动浏览器之后加一句 `driver.implicitly_wait(10)`。

---

## 第二步：打开页面

```python
driver.get("https://www.baidu.com")
```

没什么花头。`get()` 是 Selenium 里最朴实无华的方法。它做的事：在地址栏输入 URL、敲回车、等页面加载完成。后面的 `find_element` 之类默认是等 `get()` 返回了才执行。

有个小细节：`get()` 只等 HTML 文档加载完成（DOM ready），不等 JS 异步渲染完。如果你的页面是单页应用（Vue/React），页面结构在 `get()` 返回之后还在动态加载——这时候 `implicitly_wait` 就派上用场了。

---

## 第三步：定位元素——自动化最核心的技能

元素定位是整个 Selenium 的魂。你找不到元素，后面所有操作都白扯。

Selenium 4 提供了八种基础定位方式。你不用全背，但每种在哪用你得有概念。

### 八大定位方式速览

| 定位方式 | 写法 | 什么时候用 |
|------|------|-----------|
| **ID** | `By.ID, "kw"` | 元素有唯一 id，首选 |
| **Name** | `By.NAME, "username"` | 表单元素有 name 属性 |
| **Class Name** | `By.CLASS_NAME, "btn"` | class 唯一时可用，但很多页面 class 重用率高 |
| **Tag Name** | `By.TAG_NAME, "input"` | 很少用，页面上一堆 input |
| **Link Text** | `By.LINK_TEXT, "新闻"` | 精确匹配 a 标签的显示文字 |
| **Partial Link Text** | `By.PARTIAL_LINK_TEXT, "新闻"` | 模糊匹配 a 标签文字，比如「新闻中心」和「新闻频道」都能找到 |
| **CSS Selector** | `By.CSS_SELECTOR, "#kw"` | 最灵活，Web 首选 |
| **XPath** | `By.XPATH, "//input[@id='kw']"` | 功能最强，但比 CSS Selector 慢 |

**2026 年还多了两种推荐方式**（Selenium 4 加入）：

| 定位方式 | 写法 | 干什么的 |
|------|------|---------|
| **Role（ARIA）** | `By.ROLE, "button"` | 按无障碍语义角色定位，语义化最好 |
| **Test ID** | `By.TEST_ID, "submit-btn"` | 专门给自动化预留的属性 `data-testid` |

`By.ROLE` 和 `By.TEST_ID` 是新项目的最佳实践——不受 UI 改动影响。但老项目大概率没有 `data-testid`，ARIA 角色也不一定配全。所以基础的八种你还是得会。

### 百度搜索框：实操找元素

打开百度首页（https://www.baidu.com），按 F12 打开开发者工具。百度搜索框的 HTML 大概是这样的：

```html
<input id="kw" name="wd" class="s_ipt" value="" maxlength="255" autocomplete="off">
```

它有个 `id="kw"`。用 ID 定位最简单：

```python
search_box = driver.find_element(By.ID, "kw")
```

同理百度一下按钮：

```html
<input type="submit" id="su" value="百度一下" class="bg s_btn">
```

```python
search_btn = driver.find_element(By.ID, "su")
```

### 定位失败怎么办——先别急着怀疑代码

很多新手定位失败第一反应是「语法写错了」。其实大部分情况不是语法问题，是这四种情况：

1. **页面还没加载完你就去找了** → 加等待。这个第 4 章展开讲。
2. **元素在 iframe 里** → 你直接在主页面上找 iframe 里的元素永远找不到。下一章讲。
3. **ID 是动态生成的**。比如 `input_20260629_1432`——每次刷新都不一样。这种用 CSS Selector 或 XPath 模糊匹配。
4. **你在找的「id」实际上不是一个 HTML id属性，是别的什么** → 打开 F12 确认一下元素的真实属性。

---

## 第四步：操作元素——三个最常用的动作

找到元素之后，你能对它做的事大概有这些。但 90% 的操作用这三个就够了。

### 输入文字：send_keys()

```python
from selenium.webdriver.common.by import By

driver.find_element(By.ID, "kw").send_keys("Selenium 教程")
```

`send_keys` 不光能输文字，还能输键盘特殊键——回车、Tab、Ctrl+C 这些：

```python
from selenium.webdriver.common.keys import Keys

element.send_keys(Keys.ENTER)       # 回车
element.send_keys(Keys.TAB)         # Tab 切换焦点
element.send_keys(Keys.CONTROL, 'a')  # Ctrl+A 全选
element.send_keys(Keys.CONTROL, 'c')  # Ctrl+C 复制
```

### 点击：click()

```python
driver.find_element(By.ID, "su").click()
```

`click()` 是最常用的操作，但也是最容易出问题的一个。三种常见翻车场景：

1. **点击被其他元素挡住**。比如弹窗遮住了按钮，Selenium 会报 `ElementClickInterceptedException`。你得先关闭弹窗再点。
2. **按钮还没变成可点击状态**。比如提交按钮灰的，要等表单填写完整才亮。这时候你用 `click()` 会报错或者点完了没反应。
3. **按钮在页面底部，需要滚动才能看到**。Selenium 4 会自动滚动到元素可见位置再点。如果你的 Selenium 版本够新（4.x），不用手动写 `scroll_into_view`。

### 清除已有内容：clear()

```python
element = driver.find_element(By.ID, "kw")
element.clear()           # 先清空
element.send_keys("新内容")  # 再输入
```

`clear()` 是把 input 框里已有的内容删掉。你如果定位到一个已经填了东西的输入框，直接 `send_keys` 是在已有内容后面追加，不是覆盖。输入前先 `clear()` 能避免一堆诡异的断言失败。

---

## 第五步：断言——自动化测试的灵魂

没有断言的脚本不叫测试，叫演示。

```python
# 这就不是测试，这只是「跑了一遍」
driver.find_element(By.ID, "kw").send_keys("测试")
driver.find_element(By.ID, "su").click()
```

```python
# 这才是测试——你检查了结果对不对
driver.find_element(By.ID, "kw").send_keys("测试")
driver.find_element(By.ID, "su").click()

assert "测试" in driver.title   # 搜索结果页面标题里应该包含搜索词
```

### Selenium 里常用的三种断言

**1. 断言页面标题**

```python
assert "百度一下" in driver.title
```

最轻量级的断言。标题对了至少说明页面跳转成功了。

**2. 断言某个元素出现了**

```python
element = driver.find_element(By.CSS_SELECTOR, ".result")
assert element.is_displayed()
```

`is_displayed()` 检查元素是否在页面上可见。注意：元素存在于 DOM 但不一定可见（`display:none`）。`is_displayed()` 检查的是「用户在屏幕上能看到它吗」。

**3. 断言页面文本内容**

```python
assert "关键词" in driver.page_source
```

`driver.page_source` 是整个页面的 HTML 源码。这种断言比较暴力——只要能搜到这个词就算过。适合快速验证但对大页面性能不好。

### 一个要点：断言之前必须等

```python
# ❌ 这么写八成会挂
driver.find_element(By.ID, "su").click()
assert "百度一下" in driver.title

# ✅ 这么写才稳
driver.find_element(By.ID, "su").click()
# 等页面跳转完成——搜索结果页的某个元素出现了
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".result"))
)
assert "测试" in driver.title
```

不等的后果：你点了搜索，浏览器正在加载结果页，标题还没从「百度一下」变成「测试_百度搜索」——你的断言已经执行完了，挂了。**断言之前加一次显式等待，让你的脚本比页面慢一步。**

---

## 完整链路实战：百度搜索「Selenium 教程」

把前面讲的串成一条完整链路：

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === 第一步：启动 ===
driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)

# === 第二步：打开页面 ===
driver.get("https://www.baidu.com")

# === 第三步：操作元素 ===
# 输入搜索词
driver.find_element(By.ID, "kw").send_keys("Selenium 教程")
# 点击搜索按钮
driver.find_element(By.ID, "su").click()

# === 第四步：等结果出来 ===
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#content_left"))
)

# === 第五步：断言 ===
assert "Selenium 教程" in driver.title, f"标题不匹配，实际标题: {driver.title}"
print(f"✅ 测试通过，当前标题: {driver.title}")

# === 第六步：关闭 ===
driver.quit()
```

逐段说一下你可能不清楚的细节：

- **`By.CSS_SELECTOR, "#content_left"`**：百度搜索结果列表的容器 div，id 是 `content_left`。用 CSS 选择器 `#content_left` 定位（`#` 代表 id 选择器）。选择它作为等待目标是因为结果列表出现 = 搜索结果加载完毕。
- **`EC.presence_of_element_located`**：expected_conditions 预设的等待条件之一——「元素存在于 DOM 中」。只要元素进了 DOM 就算满足，不要求可见、不要求可点击。
- **`assert ... , f"报错信息"`**：逗号后面是断言失败时的提示信息。不加的话失败了你只知道「assert 挂了」，不知道当时实际标题是什么。带上错误信息，调试时间省一半。
- **百度首页 HTML 可能随版本变化**：百度偶尔改版，搜索框的 `id` 可能会变。如果 `By.ID, "kw"` 定位不到，打开 F12 确认一下元素当前的实际属性。这就是自动化测试的日常——页面改了，你的定位器跟着改。

---

## 你自己的第一个实战：拿这套模板去测任何网站

这套模板你已经可以拿去测任何网站了。找一个你手头在测的系统，按这个骨架填：

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)

# 打开你的系统
driver.get("你的系统URL")

# 找到需要操作的元素，操作它们
# ... 你的业务逻辑 ...

# 等关键结果出现
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.xxx, "xxx"))
)

# 断言
assert "期望的文本" in driver.page_source

driver.quit()
```

所有 Selenium 脚本都是这个骨架，只是中间填的业务逻辑不一样。你现在的问题是「知道骨架了但不知道具体怎么找元素」——接下来两章就是专治这个的。

---

## 不推荐的方案：两种常见的坏习惯

### ❌ 用 `time.sleep()` 当等待

```python
driver.find_element(By.ID, "su").click()
time.sleep(3)  # 硬等 3 秒
assert "xxx" in driver.title
```

为什么不该用：网络快的时候 0.5 秒就加载完了，你白等 2.5 秒。网络慢的时候 3 秒没加载完，脚本照挂。100 个用例下来你浪费了几分钟的生命。

唯一可以硬等的场景：**你真的在等一个外部系统响应，Selenium 的等待机制管不到。** 比如点了按钮后发了一个 HTTP 请求到外部服务，那个服务的响应时间你没法用 WebDriverWait 监控。这种情况才用 `time.sleep()`，但最多 5 秒。

### ❌ 只断言元素存在，不断言元素的内容

```python
element = driver.find_element(By.ID, "result")
assert element.is_displayed()  # 元素在，但内容对不对？
```

元素在页面上不代表内容是对的。比如登录失败也弹了个提示框，元素确实显示了——但内容是「密码错误」而不是「登录成功」。你的断言过了，Bug 漏了。

一个好的断言至少要验证关键内容。要么用 `element.text` 精确匹配，要么用 `driver.page_source` 模糊包含。

---

## 接下来

这一章你把自动化测试的四步骨架搭好了。但元素定位才开了一个头——百度搜索框有 id 是运气好。现实中你碰到的是「没有 id」「id 每次变」「class 和十个元素共用」「在嵌套 div 深处」这些情况。

下一篇开始拆解元素定位的各种花式写法——XPath、CSS Selector、还有 2026 年好用的 Relative Locator。**能稳定定位元素，你才算一个合格的自动化测试工程师。**

---

> 下一篇：《元素定位深度讲解（上）：ID/Name/Class/Tag，四大基础定位和为什么它们总是不够用》

#Selenium #Web自动化 #Python测试 #元素定位 #软件测试

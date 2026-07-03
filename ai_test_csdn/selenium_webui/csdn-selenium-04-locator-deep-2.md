# Selenium 元素定位深度讲解（下）：XPath 函数、动态 ID 与 iframe

> 上篇你学会了 CSS Selector 和 XPath 基础。但你发现没——那些例子的元素都很「干净」，有固定 ID、有固定文字。实战里 90% 的定位痛点不是基础语法问题，是这三大类：动态 ID、「点了没反应」（iframe 里）、不知道哪个写法最稳。这一篇，逐个拆。

---

## 一、XPath 函数：一条表达式能做的事比你想的多

### contains()——用得最多的一个

上篇介绍过 `contains(text(), 'xxx')`。但 `contains()` 不只用在文本上。

```python
# 属性包含
driver.find_element(By.XPATH, "//input[contains(@class, 'form')]")

# ID 包含
driver.find_element(By.XPATH, "//*[contains(@id, 'submit')]")

# 某个后代元素包含指定文本（找包含「优惠」二字的 div 卡片）
driver.find_element(By.XPATH, "//div[contains(., '优惠')]")
```

`contains(., '优惠')` 里的 `.` 代表当前节点的所有文本内容（包括嵌套子元素的文本）。跟 `contains(text(), '优惠')` 的区别：

```html
<div class="card">
  <span>限时</span>优惠
</div>
```

- `contains(text(), '优惠')` → ❌ 找不到。「优惠」不是 div 的直接文本节点，而在 span 旁边
- `contains(., '优惠')` → ✅ 找到。`.` 把 div 里所有后代文字拼起来再搜

**别死磕 `text()`。** 不确定文本位置的时候，用 `contains(., 'xxx')` 比 `text()` 容错率高。

---

### starts-with()——动态 ID 的救星

```html
<input id="input-abc123-def" />  <!-- abc123 每次刷新都变，但 input- 开头不变 -->
```

```python
driver.find_element(By.XPATH, "//input[starts-with(@id, 'input-')]")
```

这是处理动态 ID/class 最常用的组合——后面「动态 ID 策略」那节会展开讲。

---

### not()——排除某个条件

```python
# 所有 class 包含 btn 但不是 disabled 的按钮
driver.find_element(By.XPATH, "//button[contains(@class, 'btn') and not(@disabled)]")

# class 里有 card 但没有 expired 的 div
driver.find_element(By.XPATH, "//div[contains(@class, 'card') and not(contains(@class, 'expired'))]")
```

页面上一堆相似元素，你想排除掉那些灰的、禁用的、隐藏的——`not()` 是最简洁的写法。

---

### normalize-space()——干掉前后空格和换行

有些元素的文本换行了，或者前后被塞了空格：

```html
<button>
  确认
  提交
</button>
```

```python
# ❌ 精确匹配会失败——文本里有换行和空格
# driver.find_element(By.XPATH, "//button[text()='确认提交']")

# ✅ 用 normalize-space()
driver.find_element(By.XPATH, "//button[normalize-space()='确认提交']")
```

`normalize-space()` 三件事：去掉首位空格、把中间多个空格合并成一个、把换行替换成空格。你的 XPath 里只要有文本匹配，默认先试 `normalize-space()`。

---

### position() 和 last()——取第几个

```python
# 第 3 个 input
driver.find_element(By.XPATH, "(//input)[3]")

# 最后一个 div.card
driver.find_element(By.XPATH, "(//div[@class='card'])[last()]")

# 倒数第二个
driver.find_element(By.XPATH, "(//div[@class='card'])[last()-1]")

# 前 3 个中的最后一个（取第 3 个）
driver.find_element(By.XPATH, "(//div[@class='card'])[position()=3]")
```

注意：**括号不能省。**

```python
# ❌ 错误
driver.find_element(By.XPATH, "//input[3]")
# 含义：每个父元素下的第三个子元素（且必须是 input）

# ✅ 正确
driver.find_element(By.XPATH, "(//input)[3]")
# 含义：整个文档中全部 input 里的第三个
```

忘了加括号的后果不是报错——是定位到另一个元素，而你盯着屏幕半天发现「操作确实执行了，但是点歪了」。这种 bug 最难查。

---

### count()——统计元素个数

```python
# 统计页面上有多少个 class 为 card 的 div
cards = driver.find_elements(By.CLASS_NAME, "card")
print(f"一共有 {len(cards)} 张卡片")
```

XPath 自己的 `count()` 在 Selenium 里不那么实用——因为 Selenium 不直接返回 XPath 表达式计算结果。用 `find_elements` + `len()` 就够了。

---

### 函数组合实战：一个复杂场景

页面列表，每行一个商品卡，卡里有标题、价格、加入购物车按钮。你要点第一张卡里的「加入购物车」：

```html
<div class="product-list">
  <div class="product-card">
    <h3 class="title">蓝牙耳机 Pro</h3>
    <span class="price">¥299</span>
    <button>加入购物车</button>
  </div>
  <div class="product-card expired">
    <h3 class="title">数据线</h3>
    <span class="price">¥19</span>
    <button>加入购物车</button>
  </div>
</div>
```

需求：点第一张**没有过期**的商品卡里的「加入购物车」。

```python
# XPath 组合写法
driver.find_element(By.XPATH,
    "(//div[contains(@class, 'product-card') "
    "and not(contains(@class, 'expired'))])[1]"
    "//button[contains(text(), '加入购物车')]"
).click()
```

拆解：
1. `//div[contains(@class, 'product-card') and not(contains(@class, 'expired'))]` → 找到所有没过期的商品卡
2. `[1]` → 取第一张
3. `//button[...]` → 在里面找购物车按钮

一条 XPath 干了三步逻辑。

---

## 二、动态 ID：这是你最常撞的墙

### 问题长什么样

React、Vue、Angular 编译出来的 HTML，ID 和 class 很多是动态生成的：

```html
<!-- 每次刷新都不一样 -->
<div id="ember1234" class="css-1a2b3c4 container-xyz789">
<input id="input_20260629_143522" />
```

你不可能每次跑用例之前猜新的 ID。

### 策略一：用固定部分做模糊匹配

动态 ID 通常有固定规则——前缀固定，后缀随机：

```python
# id 以 ember 开头 → starts-with
driver.find_element(By.XPATH, "//*[starts-with(@id, 'ember')]")

# id 里包含 submit → contains
driver.find_element(By.XPATH, "//*[contains(@id, 'submit')]")

# CSS 也能做
driver.find_element(By.CSS_SELECTOR, "[id^='ember']")   # 以 ember 开头
driver.find_element(By.CSS_SELECTOR, "[id*='submit']")  # 包含 submit
driver.find_element(By.CSS_SELECTOR, "[id$='submit']")  # 以 submit 结尾
```

80% 的动态 ID 场景用这三行能搞定。

### 策略二：完全不用 ID——换其他属性定位

ID 不靠谱就换。按优先级来：

```python
# 1. data-testid（如果有）
driver.find_element(By.CSS_SELECTOR, "[data-testid='login-btn']")

# 2. name 属性
driver.find_element(By.NAME, "username")

# 3. aria-label（无障碍标签）
driver.find_element(By.CSS_SELECTOR, "[aria-label='搜索']")

# 4. placeholder
driver.find_element(By.CSS_SELECTOR, "[placeholder='请输入邮箱']")

# 5. class 里的固定部分
driver.find_element(By.CSS_SELECTOR, "[class*='btn-submit']")

# 6. 文字内容（终极兜底）
driver.find_element(By.XPATH, "//button[contains(text(), '登录')]")
```

优先级来自一条原则：**越跟视觉呈现无关的属性，越稳定。** data-testid 和 name 纯粹给开发/测试用的，aria-label 是给无障碍用的——这三种被产品改动的概率最低。placeholder 和文字内容是用户能看到的，产品可能会改——但改的频率比动态 ID 低多了。

### 策略三：按位置关系定位

既然元素自己的 ID 靠不住，就靠它身边的人：

```python
# 找到 label 文字是「手机号」的元素，后面那个 input 就是手机号输入框
driver.find_element(By.XPATH,
    "//label[contains(text(), '手机号')]/following-sibling::input"
)

# 或者从父元素往下找
driver.find_element(By.XPATH,
    "//div[contains(@class, 'form-item')][.//label[contains(text(), '手机号')]]//input"
)
```

这个思路：**找特征明显的「锚点元素」，再从锚点出发找目标。** label 的文字是产品定义的、不会变——拿它当锚点。

### 处理动态元素的万能口诀

```
先看有没有 data-testid → 没有看 name → 没有看 aria → 
没有就拿固定前缀/后缀模糊匹配 → 都没有就用旁边固定文字的兄弟/父子元素定位
```

---

## 三、iframe：你以为代码写对了，其实根本不在一个世界

### 问题不在语法，在「域」

iframe 是页面里嵌入的另一个独立 HTML 文档。你对主页面的 `driver.find_element` 操作——**找不到 iframe 里的元素。**

```html
<!-- 主页面 -->
<html>
<body>
  <h1>后台管理系统</h1>
  <iframe id="content-frame" src="/editor.html">
    <!-- 这里面是另一个完整的 HTML -->
    <textarea id="editor">...</textarea>
    <button id="save-btn">保存</button>
  </iframe>
</body>
</html>
```

```python
# ❌ 在主页面里直接找 iframe 里的按钮——永远找不到
driver.find_element(By.ID, "save-btn")  # NoSuchElementException
```

### 三步进入 iframe

```python
# 第一步：定位 iframe 元素
iframe = driver.find_element(By.ID, "content-frame")

# 第二步：切进去
driver.switch_to.frame(iframe)

# 第三步：现在你可以操作 iframe 里的 DOM 了
driver.find_element(By.ID, "save-btn").click()

# === 完事之后，切回主页面 ===
driver.switch_to.default_content()
```

`switch_to.frame()` 支持三种参数：

```python
# 1. 传 iframe 元素对象（推荐——你能确认你切对了）
iframe = driver.find_element(By.ID, "content-frame")
driver.switch_to.frame(iframe)

# 2. 传 iframe 的 name 或 id 属性值
driver.switch_to.frame("content-frame")

# 3. 传索引（第几个 iframe——换页面就变，不推荐）
driver.switch_to.frame(0)
```

### 嵌套 iframe

iframe 里还能再套 iframe：

```
主页面 → iframe A → iframe B → 目标按钮
```

```python
# 一层一层切
driver.switch_to.frame("frame-a")   # 主页面 → A
driver.switch_to.frame("frame-b")   # A → B
driver.find_element(By.ID, "target-btn").click()

# 跳回主页面（不是回到 A，是直接跳回最外层）
driver.switch_to.default_content()

# 回到上一层（回到 A）
driver.switch_to.parent_frame()
```

**切回主页面的关键词：** `default_content()` 是跳回最外层主页面。`parent_frame()` 是回到上一层 iframe。别搞混——我因为用错这个在嵌套 iframe 里调了一个下午。

### 你怎么知道目标元素在不在 iframe 里？

F12 打开开发者工具。在 Elements 里看——如果目标元素的 HTML 标签被一个 `<iframe>` 包裹着，它就在 iframe 里。或者更快的办法：用 `Ctrl+F` 搜索元素的 ID 或文字，搜不到说明它不在当前 DOM 层级——可能藏在 iframe 里。

### iframe 常见翻车场景

**场景一：页面加载了，但是 iframe 内容还没加载完。**

```python
# ❌ 切进去立马找元素——iframe 里的 DOM 可能还没渲染
driver.switch_to.frame("content-frame")
driver.find_element(By.ID, "save-btn")  # 可能 NoSuchElementException

# ✅ 切进去后先等
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver.switch_to.frame("content-frame")
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "save-btn"))
)
```

**场景二：操作完忘记切回主页面。**

```python
driver.switch_to.frame("content-frame")
driver.find_element(By.ID, "save-btn").click()
# 忘了切回来！！！

# 下一个操作在主页面找元素——找不到，报 NoSuchElementException
driver.find_element(By.LINK_TEXT, "退出登录").click()  # 挂了
```

**建议写法：操作完立刻切回来，养成肌肉记忆。**

```python
driver.switch_to.frame("content-frame")
driver.find_element(By.ID, "save-btn").click()
driver.switch_to.default_content()  # 立刻回主页面
```

---

## 四、DevTools：你的定位表达式对不对，先在这验证

很多人写完 XPath 直接往 Selenium 脚本里塞，跑一遍看报不报错。效率低而且对 CI 环境不友好（本地没问题、CI 上炸了）。

### 在 Chrome DevTools Console 里直接验证

打开目标页面，F12 → Console 标签页，输入：

```javascript
// 验证 CSS Selector
document.querySelector("#kw");

// 验证 XPath
$x("//input[@id='kw']");

// 验证多个匹配
$$(".product-card");           // CSS 返回所有
$x("//div[@class='product-card']");  // XPath 返回所有

// 看返回了几个
$x("//button[text()='登录']").length;
```

**`$x()` 是 Chrome 内置的 XPath 测试工具，但只在 Console 里可用。**

如果返回 `null` 或者空数组 `[]`——你的表达式写错了。如果返回了一个元素——点开看是不是你预期的那一个。如果返回了多个——你的表达式不够精确。

### 从 Elements 面板复制生成

在 Elements 面板右键某个元素 → Copy → Copy selector / Copy XPath / Copy JS path。但这三种自动生成的路径质量不一样：

- **Copy selector** → 一般是 `#xxx > div:nth-child(2) > span` 这种带了 `nth-child` 的路径。不太稳。
- **Copy XPath** → 通常是 `/html/body/div[1]/...` 绝对路径。废品。
- **Copy JS path** → `document.querySelector("#xxx")` 格式，有时可以直接用。

自动生成当起点，不要当终点。你拿到自动生成的路径后，自己简化到最少的层级和条件。

### 我平时怎么用 DevTools 验证定位

1. F12 → Console
2. `$x("//button[contains(text(), '登录')]")`
3. 看返回了几个元素。如果只有一个且属性跟预期一致 → OK
4. 如果返回了 5 个 → 加点条件 `$x("//form//button[contains(text(), '登录')]")` 缩小范围
5. 确定了就复制到脚本里

十秒钟的事，比你跑一次完整的 Selenium 脚本快一万倍。

---

## 五、一个完整的 iframe + 动态元素实战

假设一个后台系统的富文本编辑器页面。编辑器在 iframe 里，保存按钮的 ID 是动态的（`save-xxx`，xxx 随机）。

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)
driver.get("https://admin.example.com/editor")

# 第一步：切进编辑器 iframe
editor_frame = driver.find_element(By.ID, "editor-frame")
driver.switch_to.frame(editor_frame)

# 第二步：编辑文本（textarea 的 ID 也可能是动态的，用 class）
text_area = driver.find_element(By.CSS_SELECTOR, "[class*='editor-textarea']")
text_area.send_keys("这是自动生成的内容")

# 第三步：找保存按钮——ID 动态，但文字固定
save_btn = driver.find_element(
    By.XPATH, "//button[contains(., '保存') and not(@disabled)]"
)
save_btn.click()

# 第四步：切回主页面，验证保存成功（提示信息在主页面不在 iframe 里）
driver.switch_to.default_content()

toast = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".toast-success"))
)
assert "保存成功" in toast.text

driver.quit()
```

这个脚本里用了：iframe 切换、动态 class 模糊匹配、按文字 + `not()` 组合定位、操作完切换上下文、显式等待。把上篇和下篇的知识点全串起来了。

---

## 写在最后

元素定位学到这里，该会的你都会了。从 ID 开始，到 CSS Selector，到 XPath 基础和函数，到动态元素处理，到 iframe 跨域。剩下的不是学新知识，是**多做项目多踩坑**。

一个测试脚本的定位表达式好不好，只有一个标准：**产品改了十次界面，你这行 `find_element` 改了几次。** 改得越少，你当时的选择越对。

下一篇讲等待机制——你定位写对了，但页面没加载完脚本就跑了，结果一样挂。等待才是自动化稳定性的另一半。

---

> 如果你有实际项目里遇到过「怎么定位都不行」的元素，评论区贴 HTML 片段——我挑几个典型的下下一篇拆解。

# Selenium 元素定位深度讲解（上）：CSS Selector + XPath 彻底搞懂

> 上一章你在百度搜索框上用了 `By.ID`——因为百度输入框正好有 ID。但真实项目里，你要测的系统大概率不是百度。没有 ID、class 名是乱码、DOM 结构每版都变……这种页面才是你的日常。这一篇，我要把 CSS Selector 和 XPath 这两个定位利器彻底讲透。

---

## 先扯一句：为什么元素定位值得花两篇

你用 Selenium 做自动化，80% 的时间在干什么？

不是写操作、不是写断言——是**找元素**。

一个测试脚本最稳的部分是后面的逻辑，最脆弱的部分永远是那几个 `find_element` 的定位字符串。只要产品改一行 HTML，你的脚本就挂了。而你能做的、唯一能提升脚本稳定性的手段，就是把定位表达式写对。

这篇讲 CSS Selector（上篇的七成篇幅）和 XPath 的基础用法。下篇专门拆 XPath 高级玩法、动态元素处理和 iframe 跨域定位。

---

## CSS Selector：Web 端定位首选

实话实说——我写过的 Selenium 脚本里，CSS Selector 占了定位的 70% 以上。不是因为它功能最强，是它**在最常见场景下读起来最顺、性能最好、而且前端天然懂它**。

你写前端的同事可能不懂 XPath，但绝对懂 CSS Selector。你跟他要一个元素的定位：「帮我给那个按钮加个唯一的 class 呗，我用 CSS Selector 定位」。他能秒懂。你如果说「帮我给按钮加个唯一 XPath 路径」，他会愣一下。

### 基础语法：5 分钟从零到能用

如果你会写 CSS，CSS Selector 不用学。但测试人员不一定写过前端，下面用十行代码让你从零到能用。

```html
<!-- 假设这是你要定位的页面结构 -->
<div id="app">
  <form class="login-form">
    <input type="text" name="username" placeholder="请输入用户名" />
    <input type="password" name="password" />
    <button class="btn-primary" onclick="login()">登录</button>
    <a href="/forgot">忘记密码？</a>
  </form>
</div>
```

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

# === 最常用的 6 种 CSS Selector 写法 ===

# 1. 按 ID（最稳定）
driver.find_element(By.CSS_SELECTOR, "#app")

# 2. 按 class（注意 class 名前面的点）
driver.find_element(By.CSS_SELECTOR, ".login-form")
driver.find_element(By.CSS_SELECTOR, ".btn-primary")

# 3. 按标签名（不推荐——除非整个页面就这一个这种标签）
driver.find_element(By.CSS_SELECTOR, "form")

# 4. 按属性（中括号里写属性名和值）
driver.find_element(By.CSS_SELECTOR, "[name='username']")
driver.find_element(By.CSS_SELECTOR, "[placeholder='请输入用户名']")
driver.find_element(By.CSS_SELECTOR, "button[class='btn-primary']")

# 5. 组合：标签 + class
driver.find_element(By.CSS_SELECTOR, "input[name='password']")

# 6. 组合：标签 + class + 属性
driver.find_element(By.CSS_SELECTOR, "input[type='text'][name='username']")
```

就这些。没别的语法需要背。上面六种写法覆盖了你日常 90% 的定位需求。

---

### 父子/兄弟关系：元素间怎么跳

你需要的元素可能自己没什么特征——但它的爹或者兄弟有特征。这种场景下 CSS Selector 提供的组合符非常实用。

```html
<div class="order-card">
  <h3>订单 #12345</h3>
  <div class="detail">
    <span class="label">金额：</span>
    <span class="value">¥299.00</span>  <!-- 我要定位这个金额 -->
  </div>
</div>
```

**四种组合关系：**

```python
# 1. 后代选择器（空格）：所有后代，不管隔多少层
driver.find_element(By.CSS_SELECTOR, ".order-card .value")
# 含义：类名为 order-card 的元素里，找到一个类名为 value 的后代

# 2. 子代选择器（>）：只选直接儿子
driver.find_element(By.CSS_SELECTOR, ".order-card > .detail > .value")

# 3. 相邻兄弟（+）：紧跟在后面的那个
# 假设 label 后面紧跟着 value
driver.find_element(By.CSS_SELECTOR, ".label + .value")
# 含义：类名 label 后面紧邻的那个类名 value 的兄弟

# 4. 所有后续兄弟（~）：后面所有同级兄弟
driver.find_element(By.CSS_SELECTOR, ".label ~ span")
# 含义：label 后面所有的 span 兄弟
```

大多数情况下用空格（后代选择器）就够了。`>`（子代）当你确定 DOM 层级结构不会变、想写得更严格的时候用。

说实话，`+` 和 `~` 我实际项目里用得很少——但在动态表格、订单列表那种重复结构里偶尔会救你一命。

---

### 模糊匹配：class 名是乱码怎么办

前端框架（Vue/React/Angular）编译后的 class 经常长这样：

```html
<button class="css-1a2b3c4 btn-submit-xyz789">提交</button>
```

这个按钮你肯定不能用 `.css-1a2b3c4`——下次构建这串就变了。用属性模糊匹配：

```python
# ^= 开头匹配：以 "btn-submit" 开头
driver.find_element(By.CSS_SELECTOR, "[class^='btn-submit']")

# $= 结尾匹配：以 "submit" 结尾
driver.find_element(By.CSS_SELECTOR, "[class$='submit']")

# *= 包含匹配：class 里包含 "submit" 这个单词
driver.find_element(By.CSS_SELECTOR, "[class*='submit']")

# |= 单词前缀匹配：以 "btn-" 开头（完整单词或跟连字符）
driver.find_element(By.CSS_SELECTOR, "[class|='btn']")
```

这里有个坑：`*=` 是**包含**匹配，不是**完整单词**匹配。

```python
# 假设 class="btn-submit"，用 *= 搜 "btn" 能匹配到
# 假设 class="button"，用 *= 搜 "btn" 也能匹配到！
# button 里包含 "btn" 这三个字母
```

所以 `*=` 要尽量写得足够长、足够特殊，避免误匹配。

`|=` 是专门给 BEM 命名法（Block__Element--Modifier）设计的，类似 `btn--primary`、`btn--disabled`。如果你项目不用 BEM，这玩意用不上。

---

### 伪类选择器：选中第几个、最后一个

如果页面上有五个按钮，你要点第二个。怎么定位？

```html
<div class="button-group">
  <button>取消</button>
  <button>保存</button>      <!-- 我要这个 -->
  <button>删除</button>
</div>
```

CSS 伪类：

```python
# :nth-child(n)：父元素下的第 n 个子元素
driver.find_element(By.CSS_SELECTOR, ".button-group button:nth-child(2)")

# :first-child 和 :last-child
driver.find_element(By.CSS_SELECTOR, ".button-group button:first-child")
driver.find_element(By.CSS_SELECTOR, ".button-group button:last-child")

# :nth-of-type(n)：同类型的第 n 个
driver.find_element(By.CSS_SELECTOR, ".button-group button:nth-of-type(2)")
```

`nth-child` 和 `nth-of-type` 的区别别搞混：

- `:nth-child(2)` = 父元素的第二个子元素，而且这个子元素得是 button
- `:nth-of-type(2)` = 父元素下所有 button 里的第二个

```html
<div class="group">
  <span>标签</span>
  <button>保存</button>    <!-- nth-child(2) ← 能选到 -->
  <button>删除</button>    <!-- nth-of-type(2) ← 能选到 -->
</div>
```

这里 `span` 是第一个子元素，`button` 是第二个。所以 `button:nth-child(2)` 能选到「保存」；但 `button:nth-of-type(2)` 选的是所有 button 里的第二个，也就是「删除」。

我踩过这个坑——在一个表单里以为自己在定位第二个按钮，结果点到了一个隐藏的 span。**用 `nth-of-type`，别用 `nth-child`**，除非你知道自己在干什么。

---

### CSS Selector 的边界：它做不了的事

CSS Selector 不是万能的。有些场景它做不了：

1. **不能按文本内容定位。** CSS 只能匹配 HTML 结构，不能根据元素的文字内容定位元素。
   ```python
   # ❌ CSS 做不到——「文本是"登录"的按钮」
   # driver.find_element(By.CSS_SELECTOR, "button:contains('登录')")  # 不存在
   ```

2. **不能往上找父元素。** CSS 只能往下找（祖先找后代），不能反向。
   ```python
   # ❌ CSS 做不到——「找到那个包含了 span.label 的 div」
   # 从 child 定位 parent——CSS 做不到
   ```

3. **不能做复杂的逻辑条件。** 比如「找那个 class 是 btn 或者 role 是 button 的元素」。

这些场景——尤其是按文本内容定位——正是 XPath 的强项。

---

## XPath：CSS 做不到的事交给它

XPath 总被诟病「慢」。但这个「慢」你得正确理解。在现代浏览器上，CSS Selector 和 XPath 定位一个元素的速度差距**在毫秒级别**。一条测试用例跑下来，XPath 的「慢」根本感知不到。

你用 XPath 的唯一理由应该是：**CSS Selector 做不到这件事**。

### 绝对路径 vs 相对路径

```python
# 绝对路径——❌ 别用
driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/form/input[3]")
# 前端改一个 div 嵌套它就挂了。废品。

# 相对路径——✅ 这才是活的
driver.find_element(By.XPATH, "//input[@name='username']")
# // 表示「任意位置」，不依赖 DOM 层级深度
```

记死：写 XPath 永远从 `//` 开始。如果你写了个 `/html` 开头的 XPath，删掉重来。

### 按文本内容定位——XPath 最核心的优势

```python
# 找文字是"登录"的按钮
driver.find_element(By.XPATH, "//button[text()='登录']")

# 找包含"登录"文字的任意元素
driver.find_element(By.XPATH, "//*[contains(text(), '登录')]")

# 找 a 标签里带「忘记密码」的链接（无视前后的空白字符）
driver.find_element(By.XPATH, "//a[normalize-space(text())='忘记密码']")
```

`text()` 是精确匹配，`contains(text(), ...)` 是模糊包含。`normalize-space()` 处理了首尾空格、多行换行这类问题。

按文本定位在登录页面、表单页面、导航菜单里简直是神器——因为按钮和链接的文字是产品写死的，比 id 和 class 变动频率低太多。

---

### 按属性定位——比 CSS Selector 更灵活的写法

```python
# ID
driver.find_element(By.XPATH, "//input[@id='kw']")

# class
driver.find_element(By.XPATH, "//button[@class='btn-primary']")

# 任意自定义属性
driver.find_element(By.XPATH, "//div[@data-testid='submit-btn']")
driver.find_element(By.XPATH, "//span[@aria-label='关闭']")

# 属性包含
driver.find_element(By.XPATH, "//button[contains(@class, 'submit')]")

# 不只一个属性条件（同时满足）
driver.find_element(By.XPATH, "//input[@type='text' and @name='username']")

# 或者关系（满足其中之一）
driver.find_element(By.XPATH, "//button[@id='loginBtn' or @id='submitBtn']")
```

跟 CSS 的属性选择器（`[name='username']`）比，XPath 多了 `and` 和 `or` 逻辑。在判断条件复杂的时候不用嵌套多层 CSS 选择器——一条 XPath 表达式讲清。

---

### 父子兄弟关系——XPath 可以往上找

CSS Selector 不能做的事，XPath 全可以：

```python
# 往下找后代——跟 CSS 空格一样
driver.find_element(By.XPATH, "//div[@class='order-card']//span[@class='value']")

# 往下找直接儿子——跟 CSS > 一样
driver.find_element(By.XPATH, "//div[@class='order-card']/div/span")

# 往上找父元素——CSS 做不到！
driver.find_element(By.XPATH, "//span[text()='¥299.00']/..")
# /.. 表示父元素。找到金额 span，然后向上跳到它的父元素

# 往上找祖先
driver.find_element(By.XPATH, "//span[text()='¥299.00']/ancestor::div[@class='order-card']")
# ancestor:: 找到了金额 span 往上最近的类名为 order-card 的 div

# 找后面的兄弟
driver.find_element(By.XPATH, "//span[@class='label']/following-sibling::span")
# 找到 label 后面的 span 兄弟（金额）
```

`/..` 和 `ancestor::` 在实际项目中有多实用？

给你一个我遇到的真实场景：页面上有个表格，每一行的「操作」按钮长得都一样（class 都是 `.btn-detail`），但每一行的订单号不同。你要点 12345 这一行的「查看详情」按钮。

```html
<tr>
  <td class="order-no">12345</td>
  <td class="amount">¥299</td>
  <td><button class="btn-detail">查看详情</button></td>
</tr>
```

```python
# 先找到「12345」那行，然后往上跳到 tr，再从 tr 往下找 btn-detail
driver.find_element(By.XPATH,
    "//td[text()='12345']/parent::tr//button[@class='btn-detail']"
).click()
```

这行代码的逻辑：找到文字是「12345」的 td → 跳到它的父级 tr → 在这个 tr 范围内找详情按钮。**位置限定在正确的那一行**，不会错点到别的行的按钮。

这种场景你要是纯用 CSS Selector 就抓瞎了——CSS 没有向上找父元素的能力。

---

## CSS Selector vs XPath：什么时候用哪个

不是「选一个」，是**知道各在什么场景用**。

| 场景 | 用什么 | 原因 |
|------|--------|------|
| 元素有唯一 ID | CSS: `#kw` | 简单，性能最好 |
| 有唯一 class | CSS: `.btn-submit` | 直观 |
| class 是动态生成的 | XPath: `contains(@class, 'submit')` | XPath 的 `contains` 直接用 |
| 需要按文字内容定位 | XPath: `text()='登录'` | CSS 做不到 |
| 需要往父级定位（从子找父） | XPath: `/parent::` 或 `/..` | CSS 做不到 |
| 多个条件组合（and/or） | XPath: `[@a='x' and @b='y']` | 语法更直观 |
| 同一元素在 DOM 中出现多次，要区分第几个 | CSS: `:nth-of-type(n)` | 简单 |
| 前端已经配了 `data-testid` | 直接用 `By.TEST_ID` | 最稳 |
| 日常定位（没什么特殊需求） | CSS Selector | 读起来更短更顺 |

一个我内心的优先级：

```
data-testid > ID > Accessibility标签 > CSS Selector > XPath > 绝对路径
```

有 `data-testid` 用 `By.TEST_ID`。没有就看有没有 ID。没有 ID 用 CSS Selector。CSS 不行再上 XPath。

**绝对路径永远排最后——不，根本不该排进来。**

---

## ❌ 不推荐的定位方案

### 1. 绝对路径 XPath

```
/html/body/div[3]/table/tbody/tr[2]/td[4]/button
```

前端哪怕只在你按钮外面多包一层 div，字符串就全变。没有任何自动化脚本能在绝对路径上活过第二个版本。

### 2. 纯 class="s_ipt" 作为唯一定位条件

```python
# ❌ 百度页面还能用，你自己的项目先别这么写
driver.find_element(By.CLASS_NAME, "s_ipt")
```

一个页面上 `class="btn"` 的元素可能同时出现十几个。`CLASS_NAME` 只返回第一个匹配到的不保证每次同一个——时好时坏那种 bug 最难查。

### 3. 用数字做索引定位

```python
# ❌ (//input)[3]——今天第三个 input 是搜索框，明天第四个才是
driver.find_element(By.XPATH, "(//input)[3]")
```

一样的理由：数字索引在 UI 稍有变动时就会移位。

---

## 串一个实战例子

假设你要登录一个系统（登录页面是虚构的「Todo App」），用户名、密码、登录按钮都没有 ID：

```html
<div class="auth-card">
  <h2>欢迎回来</h2>
  <form class="auth-form">
    <div class="field">
      <label>邮箱</label>
      <input type="email" placeholder="请输入邮箱" />
    </div>
    <div class="field">
      <label>密码</label>
      <input type="password" placeholder="请输入密码" />
    </div>
    <button class="sc-dkPtRN jHdYwA">登录</button>
    <a href="/register">还没有账号？注册</a>
  </form>
</div>
```

三个元素的定位策略：

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get("https://example.com/login")

# 邮箱输入框：没有 id，没有 name，只有 placeholder
email_input = driver.find_element(By.CSS_SELECTOR, "[placeholder='请输入邮箱']")

# 密码输入框：同样的逻辑，用 type 属性区分
password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")

# 登录按钮：class 是动态生成的乱码（sc-dkPtRN jHdYwA），但文字是「登录」
login_btn = driver.find_element(By.XPATH, "//button[text()='登录']")

# 执行登录
email_input.send_keys("test@example.com")
password_input.send_keys("password123")
login_btn.click()

driver.quit()
```

三个元素用了三种策略：CSS 属性定位、CSS 类型定位、XPath 文本定位。不在一种方式上死磕。

---

## 本篇总结一句话

**能用简单属性就别上 CSS，能用 CSS 就别上 XPath，能用 XPath 就别写绝对路径。** 元素定位的好坏直接决定你的脚本能活几个迭代。

下一篇（下篇）我会覆盖：XPath 的函数玩法、动态 ID 的处理策略、iframe 内元素定位，以及 Inspect 工具的正确用法——那才是花时间最多的地方。

---

> 你读到这里如果有卡住的或有实际项目里遇到的定位场景不知道怎么处理，欢迎评论区直接丢 HTML 片段——我会挑几例在下篇里拆解你的定位怎么选。

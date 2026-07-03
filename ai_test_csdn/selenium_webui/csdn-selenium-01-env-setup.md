# Selenium 环境搭建：从零到跑通第一个脚本

> 2026 年的 Selenium，不需要 chromedriver，不需要配环境变量，三行命令就完事。但网上 90% 的教程还在教你手动下载驱动，这篇告诉你现在到底该怎么搞。

---

## 这篇要解决什么问题

你决定学 Selenium，打开搜索引擎敲了「selenium 教程」，点开前三个结果——每个都在教你：

1. 先去 Chrome 设置里看版本号
2. 再去 chromedriver 下载页找对应版本
3. 下载 .exe 放到某个目录
4. 配环境变量 PATH
5. 然后才开始 `pip install selenium`

**告诉你一个好消息：以上五步，在 2026 年已经全部不需要了。**

Selenium 从 4.6 版本开始内置了 Selenium Manager，驱动下载、版本匹配、环境配置自动全搞定。但搜索引擎的排名机制决定了老教程永远排在前面，所以你可能已经白折腾半天了。

这篇把现在正确的最短路径写清楚。只讲实战，不讲历史。

---

## 你需要准备什么

就三样东西，你电脑上大概率已经有了：

- **Python 3.8+**（建议 3.10 以上，3.8 也能跑但有些类型提示不支持）
- **pip**（装 Python 的时候自带的，命令行敲 `pip --version` 确认一下）
- **Chrome 浏览器**（Edge 或 Firefox 也行，后面会讲怎么切）

没了。不需要 JDK，不需要 Node.js，不需要 Android SDK。Web 自动化就这点好——环境轻。

如果你还没装 Python，去 python.org 下载最新版 3.12.x，安装的时候**勾上「Add Python to PATH」**。这一步不勾的话后面每一步都会报「pip 不是内部命令」。

---

## 装 Selenium：三种方式任选一个

### 方式一：直接装（最快）

```bash
pip install selenium
```

装完验证：

```bash
pip show selenium
```

输出大概长这样：

```
Name: selenium
Version: 4.45.0
Summary: Official Python bindings for Selenium WebDriver
```

看到版本号就说明装好了。

### 方式二：虚拟环境装（推荐正经做项目）

如果你只是写着玩，方式一就够了。如果你要做项目或者不想污染全局 Python 环境：

```bash
# 创建虚拟环境
python -m venv selenium_env

# 激活（Windows PowerShell）
selenium_env\Scripts\Activate.ps1

# 激活（Windows CMD）
selenium_env\Scripts\activate.bat

# 激活（Mac/Linux）
source selenium_env/bin/activate

# 装 Selenium
pip install selenium
```

以后每次写 Selenium 脚本前，先激活虚拟环境就行。

### 方式三：conda 环境（给已经在用 Anaconda 的人）

```bash
conda create -n selenium_env python=3.12
conda activate selenium_env
pip install selenium
```

选一种装完就行。我自己的习惯是方式二，虚拟环境干净，删了也不心疼。

---

## 跑第一个脚本：就 5 行

打开你的编辑器（VS Code / PyCharm / 记事本都行），新建一个 `test.py`：

```python
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.baidu.com")
print(driver.title)
driver.quit()
```

保存，终端里跑：

```bash
python test.py
```

你会看到：

1. 一个 Chrome 窗口自动弹出来
2. 地址栏跳转到百度首页
3. 终端打出「百度一下，你就知道」
4. Chrome 窗口自动关闭

如果你看到这四步，恭喜，环境已经配好了。**整个流程应该不超过两分钟。**

如果你看到了而不是这四步——跳到最后一大节「常见报错速查」，对着找。

---

## Selenium Manager 到底帮你干了什么

你可能好奇：以前不是要手动下载 chromedriver 吗？怎么现在 `pip install selenium` 就能跑了？

Selenium 4.6 开始内置了**Selenium Manager**，一个用 Rust 写的小工具。它的工作流程是这样：

```
你写 webdriver.Chrome()
    ↓
Selenium 检测你电脑上装了哪个版本的 Chrome
    ↓
Selenium Manager 自动从 Chrome 官方源下载匹配的 chromedriver
    ↓
chromedriver 启动，连上你的 Chrome 浏览器
    ↓
脚本开始跑
```

整个过程对你完全透明。你不用管 chromedriver 放在哪、版本对不对——Selenium Manager 全包了。

**第一次跑可能会慢几秒**，因为它要在后台下载驱动。从第二次开始就是秒启。

一个小细节：chromedriver 被 Selenium Manager 下载到了一个叫 `~/.cache/selenium/` 的目录里（Windows 在 `C:\Users\你的用户名\.cache\selenium\`）。你如果好奇它在哪，可以去这个目录看一眼。但你不需要手动管理它——Selenium Manager 会自动更新和清理。

---

## 换浏览器：Chrome / Edge / Firefox 三件套

你大概率用 Chrome，但项目里可能要求测 Edge 或 Firefox。换浏览器也很简单：

### Edge

```python
from selenium import webdriver

driver = webdriver.Edge()
driver.get("https://www.baidu.com")
print(driver.title)
driver.quit()
```

前提是你电脑上装了 Edge 浏览器。Selenium Manager 同样会自动下载 msedgedriver，不用手动搞。

### Firefox

```python
from selenium import webdriver

driver = webdriver.Firefox()
driver.get("https://www.baidu.com")
print(driver.title)
driver.quit()
```

需要装 Firefox 浏览器。Selenium Manager 会自动下载 geckodriver。

三种浏览器的代码区别仅仅是把 `Chrome()` 换成 `Edge()` 或 `Firefox()`，其他所有 API 一模一样。这也是 Selenium 跨浏览器的核心价值——写一套脚本，换一个类名就通吃。

---

## 第一个脚本拆开看

回到刚才那 5 行，每一行到底做了什么：

```python
from selenium import webdriver
```

从 Selenium 库里导入 `webdriver` 模块。`webdriver` 是 Selenium 的核心，所有操控浏览器的操作都在这个模块里。

```python
driver = webdriver.Chrome()
```

创建一个 Chrome 浏览器实例。`driver` 这个东西，你可以把它理解成「你的浏览器遥控器」。之后你对浏览器的所有操作，都是通过 `driver.` 调用的。

这行背后发生的事情：Selenium Manager 检测你的 Chrome 版本 → 下载匹配的 chromedriver → 启动 Chrome 浏览器 → 返回遥控器给你。

```python
driver.get("https://www.baidu.com")
```

让浏览器跳转到百度首页。`get()` 是 Selenium 里最常用的方法之一，相当于你在地址栏里输入 URL 敲回车。

```python
print(driver.title)
```

获取当前页面的标题并打印。`driver.title` 返回的是浏览器标签页上显示的那个标题文字。

```python
driver.quit()
```

关闭浏览器，释放内存。**这行非常重要**，忘写了的话每跑一次就多一个 Chrome 进程挂在后台，跑个十来次你电脑就卡了。

---

## 不推荐的方案：网上老教程里的三种写法

搜索引擎里排前面的 Selenium 教程，很多是 2019-2021 年写的。下面这三种写法你现在搜到的概率很大——**别学，原因如下**。

### ❌ 写法一：手动下载 chromedriver + 配 PATH

```python
# 老教程会教你这么写：
driver = webdriver.Chrome(executable_path="C:/chromedriver.exe")
```

为什么别学：`executable_path` 参数在 Selenium 4 里已经标记为 deprecated，官方不推荐用。而且手动管理驱动版本是个体力活——Chrome 一更新，驱动就得跟着换，忘了换就报错。用 Selenium Manager 自动管理不就完了。

### ❌ 写法二：用 webdriver-manager 包

```python
# 老教程会叫你装这个：
pip install webdriver-manager

from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```

为什么还在用这个：`webdriver-manager` 是 Selenium Manager 出现之前的过渡方案。当时 Selenium 自己不管理驱动，社区就做了这个第三方包来弥补。现在 Selenium 内置了 Selenium Manager，你不需要再依赖第三方包了。

但 `webdriver-manager` 也不是完全没用。个别企业的内网环境，Selenium Manager 自动下载驱动的 CDN 可能被墙，这时候 `webdriver-manager` 可以指定自定义镜像源。不过对大多数人来说，直接 `webdriver.Chrome()` 就够了。

### ❌ 写法三：用 `desired_capabilities` 字典

```python
# Python 老教程的经典写法：
caps = {
    "browserName": "chrome",
    "platformName": "Windows"
}
driver = webdriver.Remote(
    command_executor="http://localhost:4444",
    desired_capabilities=caps
)
```

为什么别学：`desired_capabilities` 已经是 deprecated 状态很久了。现在的正确写法是用 `Options` 对象设置参数，下一篇会讲。

**一句话：如果你搜到的 Selenium 教程在教你下载 chromedriver 或者用 `webdriver-manager`——那篇教程基本是 2023 年之前的。方法能跑，但不是现在的最佳实践。**

---

## 常见报错速查

环境搭建阶段，你大概率会碰到下面这几个报错，我都列出来，对着找就行。

### 报错一：`'pip' 不是内部或外部命令`

**原因：** Python 没装，或者装的时候没勾「Add Python to PATH」。

**解决：** 重新运行 Python 安装程序，点「Modify」，勾上「Add Python to environment variables」。或者手动把 Python 安装目录加到系统 PATH 里。

### 报错二：`ModuleNotFoundError: No module named 'selenium'`

**原因：** selenium 没装，或者你在虚拟环境外跑了脚本。

**解决：** `pip install selenium`，然后确认你的终端当前环境是不是装了的那个。

### 报错三：`SessionNotCreatedException: Could not start a new session`

最常见的环境报错，原因可能有好几种：

**情况 A——Chrome 版本太旧。** Selenium Manager 找不到匹配的驱动。

解决：打开 Chrome → 右上角三个点 → 帮助 → 关于 Google Chrome，让它自动更新到最新版。

**情况 B——Selenium Manager 下载驱动被墙/代理拦了。**

解决：关掉 VPN/代理试试。如果是公司内网必须走代理，配一下系统代理环境变量：
```bash
set HTTP_PROXY=http://你的代理地址:端口
set HTTPS_PROXY=http://你的代理地址:端口
```

**情况 C——你电脑上有多个 Chrome 版本。**

解决：极少数情况。有些测试机同时装了 Chrome Stable 和 Chrome Beta，Selenium Manager 可能搞混。卸载其中一个就行。

### 报错四：Chrome 窗口闪了一下就没了，终端也没打印东西

**原因：** 脚本报错了但你没用 try/except 捕获，或者页面加载超时。

**解决：** 暂时加一个 `driver.maximize_window()` 先看浏览器里到底发生了什么——也许页面确实打开了但标题不是你以为的那个。或者用 `input("按回车关闭浏览器")` 在 `quit()` 之前暂停一下，手动看看浏览器状态。

---

## 接下来

现在你已经能打开浏览器、跳转页面、打印标题了。但自动化测试不是用来看百度标题的——下一步，你要学会在页面上找到元素并操作它。

下一篇讲**最小可执行链路**：定位文本框、输入内容、点击按钮、读取文字——然后做一个完整的小脚本。这些都是自动化测试的基本动作，每个你都会用几十上百遍。

---

> 下一篇：《Selenium 最小可执行链路：启动 → 定位 → 操作 → 断言》——从打开页面到完成第一个有效用例。

#Selenium #Web自动化 #Python #环境搭建 #软件测试

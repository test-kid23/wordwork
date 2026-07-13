# Claude Code 装不上？我踩了 5 个坑，第 3 个 90% 的人都会遇到

> 从零到第一个对话的完整指南，手把手带你绕过所有安装陷阱——尤其是国内网络环境下那些官方文档根本不会写的事。

---

上篇说了 Claude Code 是什么、跟 Copilot/Cursor 的区别。这篇兑现承诺：**手把手带你装好 Claude Code，敲出第一个对话**。

我装它的那个下午，说实话体验并不好。遇到了一堆坑——网络问题、API 报错、终端编码乱码、NPM 装到一半报权限错误……如果是三年前的我，装到第三个报错可能就关了终端打开 Steam 了。

所以这篇不只是"翻译官方文档"。我会按**国内用户的真实网络环境**来写，把每一个会卡住的地方提前标出来。你跟着走，就不会踩我踩过的坑。

---

**本文目录：**

- 一、装前准备：别急着敲命令
- 二、安装 Claude Code 本体
- 三、搞定 API：直连 vs 中转
- 四、第一个对话
- 五、5 个高频坑（附解法）

---

## 一、装前准备：别急着敲命令

先搞清楚你要准备什么，然后再动手。

| 你需要 | 为什么 |
|--------|--------|
| 一个终端 | macOS 用 Terminal/iTerm2，Windows 用 PowerShell 或 WSL，Linux 不用说了 |
| 一个能用的 API Key | Anthropic 官方的（如果你能搞定）或者第三方模型 API Key（OpenAI / DeepSeek / 智谱等） |
| 一个中转工具（国内用户） | 因为 Claude Code 默认直连 Anthropic，国内网络不通，需要中间代理 |

### 最重要的判断：你是走直连还是中转？

这是安装前要做的**唯一一个关键决策**，决定了后面所有步骤。

如果你人在海外、网络能直连 Anthropic：走官方路径，直接用 Anthropic API Key，安装 → 配置环境变量 → 搞定。全程 5 分钟。

如果你在国内：走中转路线。先装 Claude Code 本体，再配一个叫 **ccswitch** 的中转代理，把 Claude Code 发出的请求转发到你能用的模型 API 上。

这俩路线的安装命令是一样的，差别只在 API Key 和服务端点的配置上。后面会分开讲。

> **先确认你能用哪个模型。** 别装好了才去找 Key，大概率会卡在"有客户端、没后端"这个尴尬状态。

---

## 二、安装 Claude Code 本体

Claude Code 的安装方式有官方脚本和包管理器两种。**推荐官方脚本**，最简单。

### macOS / Linux

打开终端，一条命令：

```
curl -fsSL https://claude.ai/install.sh | bash
```

如果你用 Homebrew：

```
brew install --cask claude-code
```

两个方法都一样，官方脚本是 Anthropic 推荐的方式，Homebrew 是 macOS 用户更熟悉的渠道。

### Windows

**推荐用 PowerShell（管理员模式）**：

```
irm https://claude.ai/install.ps1 | iex
```

或者用 WinGet：

```
winget install Anthropic.ClaudeCode
```

### 一个不要做的事

你可能会在各种教程里看到这条命令：

```
npm install -g @anthropic-ai/claude-code
```

**别用。** NPM 安装方式已经被 Anthropic 官方废弃了。用 NPM 装的版本可能缺少关键更新和功能，后续可能完全不支持。走上面的官方脚本或包管理器就行。

---

装了之后，在终端里敲 `claude` 试试。如果能进去（即使还没配 API Key），说明本体装好了。如果敲了没反应，关掉终端重开一次——环境变量刚写进去有时候没生效。

---

## 三、搞定 API：直连 vs 中转

这是国内用户最容易卡住的环节。分开讲。

### 3.1 直连路线（海外用户 / 能翻墙）

如果你能直连 Anthropic 的服务，设置很简单：

**第一步：获取 API Key**

去 [console.anthropic.com](https://console.anthropic.com) 注册账号，在 API Keys 页面创建一个 Key。

**第二步：设置环境变量**

```bash
# macOS / Linux
export ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxx"

# Windows PowerShell
$env:ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxx"
```

建议把这一行加到 shell 配置文件里（`~/.zshrc` 或 `~/.bashrc`），这样每次打开终端不用重新设。

**第三步：验证**

```bash
claude --version
# 或者直接进项目目录，敲 claude 开始对话
```

如果能正常进入交互界面，直连路线就通了。

### 3.2 中转路线（国内用户实测可用）

走中转的本质：Claude Code 以为它在跟 Anthropic 对话，实际上中间有个翻译官，把它的请求"翻译"成 OpenAI 格式，发给 DeepSeek 或其他你买得到的模型 API。

**第一步：准备好你的模型 API Key**

OpenAI、DeepSeek、智谱、通义千问……你手头有哪个能用就用哪个。建议至少准备一个便宜好用的模型，推荐 DeepSeek V3，性价比极高。

**第二步：安装 cswitch**

ccswitch 是一个本地代理工具，把你的 Claude Code 请求转发到指定模型的 API。它是一个开源工具，GitHub 上直接搜索 **ccswitch** 就能找到。

安装方式通常是一键脚本或者二进制下载。具体跟着它的 README 走就行——不同版本安装方式可能不同，这里不写死命令。

**第三步：配置 cswitch**

启动 cswitch，在它的配置里填好：

- 你用的模型 API 地址（比如 DeepSeek 是 `https://api.deepseek.com`）
- 你的 API Key
- 端口号（默认一般是某个本地端口，比如 8080）

启动后，ccswitch 会在你本地开一个代理服务。

**第四步：让 Claude Code 走代理**

```bash
# 设置 API Key 为任意非空值（ccswitch 会拦截并替换）
export ANTHROPIC_API_KEY="ccswitch-proxy"

# 设置代理地址
export ANTHROPIC_BASE_URL="http://localhost:8080/v1"
```

Windows PowerShell 版本：

```
$env:ANTHROPIC_API_KEY="ccswitch-proxy"
$env:ANTHROPIC_BASE_URL="http://localhost:8080/v1"
```

**第五步：验证**

```bash
claude
```

进入交互界面，随便问个简单的问题测试一下。如果正常回复了，中转路线就通了。

### 中转路线的注意事项

- 不同模型的 API 格式略有差异，ccswitch 的兼容性取决于你用的模型。如果遇到奇怪的报错，先查 cswitch 文档里支持的模型列表。
- 中转有额外的延迟。如果你的模型本身在海外服务器 + 中间还过了一层代理，响应速度会比直连慢一些。正常，别慌。
- 某些 Claude Code 的高级功能（比如 `/compact` 上下文压缩）依赖 Claude 模型特有的部分 API，中转到非 Claude 模型时可能不完整。大部分日常使用不受影响。

---

## 四、第一个对话：感受"Agent 直接动手"

装好了，别急着炫技，先做一件事：**让 Claude Code 读你的项目，然后问它问题**。

### 4.1 进项目目录

Claude Code 不是聊天机器人，它需要**在项目目录里运行**才能发挥完整能力。如果你在不包含代码的目录里启动，它会少很多核心功能（读文件、改代码、跑命令）。

```bash
cd /你的/项目/路径
claude
```

### 4.2 第一次对话：让它解释你的代码

如果你有一个现成的项目，跟它说：

> 分析一下这个项目的整体结构，告诉我主要模块是什么、它们之间怎么协作的

Claude Code 会自动翻你的目录、读关键文件，然后给你一份结构分析。不需要你手动告诉它"这个文件是干嘛的"——它自己会看。

如果你没有现成项目，随便建一个测试文件：

```bash
mkdir claude-test && cd claude-test
echo "print('hello')" > main.py
claude
```

然后跟它说：

> 创建一个简单的 Python Web 应用，用 Flask，有一个 /api/hello 接口返回 JSON

Claude Code 会自动创建文件、写代码、安装依赖、启动服务。你只用看着。

### 4.3 感受"代理"和"辅助"的区别

这个时刻你会感受到上一篇讲的那个差异：

- Copilot / Cursor：你需要打开文件，选中位置，等补全建议，按 Tab 接受。
- Claude Code：你说话，它动手。创建文件、写代码、跑命令、改配置——全自动。

**第一次用的心理建议：** 别怕。它改的文件你随时可以 `git diff` 看变化，不爽就 `git checkout` 回退。Claude Code 不会绕过你的 git 版本管理，一切都可回溯。

---

## 五、安装过程中 5 个高频坑（附解法）

这些是我自己踩过、也在各种社区看到别人反复踩的坑。每个都给你标了现象、原因和一步解法。

### 坑 1：敲了 claude 没反应

**表现：** 装完脚本显示成功，但在终端里敲 `claude` 提示 "command not found"。

**真相：** 安装脚本改了 PATH，但当前终端会话还没刷新。这是跨平台通病，macOS、Linux、Windows 都遇到过。

**解法：**

- 关掉当前终端窗口，重新打开一个。99% 的情况这就好了。
- 如果还不行，手动检查 PATH。macOS/Linux 查 `echo $PATH` 里有没有 claude 的安装路径。Windows 查系统环境变量。

### 坑 2：API Key 报 "401 Unauthorized"

**表现：** `claude` 启动后，发消息报 401 错误。

**真相：** 有几种可能，按顺序排查：Key 确实填错了（多了空格/换行符）、该 Key 所属的账户没充值、Key 已被删除或过期。

**解法：**

1. 先确认环境变量是不是真的写进去了：`echo $ANTHROPIC_API_KEY`（macOS/Linux）或 `echo $env:ANTHROPIC_API_KEY`（Windows PowerShell）
2. 去 Anthropic Console 或你的模型 API 平台确认 Key 状态
3. 如果走中转，确认 cswitch 是否正在运行、端口是否正确

### 坑 3：网络超时 / Connection Refused（90% 的人栽这）

**表现：** 消息发出去一直转圈，最后报 Connection Error 或 Timeout。

**真相：** 国内网络环境直连 Anthropic API 会被墙。就算你挂了全局代理，终端里的非 HTTP 流量不一定走代理——这也是为什么很多人说"我开着 VPN 啊怎么还连不上"。

**解法：** 走中转路线（见上面第三章）。或者如果你有可靠的 HTTP 代理，需要单独配置终端的代理环境变量：

```bash
# macOS / Linux
export HTTPS_PROXY=http://127.0.0.1:7890
export HTTP_PROXY=http://127.0.0.1:7890

# Windows PowerShell
$env:HTTPS_PROXY="http://127.0.0.1:7890"
$env:HTTP_PROXY="http://127.0.0.1:7890"
```

端口号换成你自己的代理端口。如果你不确定代理端口是多少，去你的代理软件设置里找。

### 坑 4：Windows 终端中文乱码

**表现：** Claude Code 返回的中文内容在 Windows 终端里显示为乱码或方块。

**真相：** Windows 的 PowerShell 默认编码是 GBK，不是 UTF-8。Claude Code 输出的是 UTF-8 编码。

**解法：**

打开 PowerShell，执行：

```
[System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
```

或者更一劳永逸——用 Windows Terminal（微软商店免费下载），它默认 UTF-8，没有编码问题。直接在 PowerShell 里用也经常中招，Windows Terminal 是更好的选择。

### 坑 5：NPM 装完之后版本不对 / 功能缺失

**表现：** 用 NPM 装的旧版本，有些命令找不到，或者体验跟教程里描述的不一样。

**真相：** 你大概率是用 `npm install -g @anthropic-ai/claude-code` 装的，而这条路已被废弃。

**解法：** 先卸载 NPM 版本：

```bash
npm uninstall -g @anthropic-ai/claude-code
```

然后用官方脚本或包管理器重装（见上面第二章）。装完之后 `claude --version` 确认是最新版。

---

## 写在最后

装好 Claude Code 不是终点，是起点。

第一次让它改你项目代码的时候，你的本能反应可能是"等等你别动那个文件"。这种感觉我在上篇写过——它干活的方式跟你习惯的所有工具都不一样。不是辅助，是代理。

但一旦你跨过那个心理门槛，你会发现自己开始把越来越多的事情丢给它做。不是因为你变懒了，而是你发现你的时间花在**想清楚要什么**上，比花在**动手做**上，产出高太多了。

**找一个小项目试试。让它帮你做一件事——哪怕只是新建一个文件夹、写一个 Hello World、跑一遍测试。让它动一次手，你就知道我在说什么。**

下一期聊 **CLAUDE.md —— 给 AI 同事的项目说明书**。这是 Claude Code 最被低估的功能，写好了它能让 AI 对你的项目了如指掌，写不好它就是盲人摸象。模板和写法一起给你。

---

*Claude Code 入门系列 · 安装与配置*
*适用对象：想用 Claude Code 但卡在安装/配置/网络问题上的开发者*
*本系列更多文章可在公众号合集中查看*

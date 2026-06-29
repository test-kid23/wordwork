# Appium 3 环境搭建避坑指南

> 这篇大概是整个系列里最长、也最劝退的一篇。但如果你能扛过去，后面学什么都顺。说实话，Appium 环境搭建我用过的所有自动化工具里排第一难——这篇不是教你装软件，是帮你避坑。

---

## 这篇是帮你干什么的

上一个系列 Selenium 环境搭建就两行命令搞定。这篇 Appium 环境搭建——你得装 Node.js、Appium Server、平台驱动、Java JDK、Android SDK、模拟器，然后配一堆环境变量，中间哪个环节歪了都跑不起来。

我上次帮一个同事从零搭 Appium 环境，他在 `ANDROID_HOME` 路径里多打了个空格，卡了三个小时。这不是他笨，是 Appium 的报错信息有时候根本看不出是哪出了问题。

所以这篇不是按「装软件的步骤」组织的——是按「卡在哪一步」组织的。每步都标注最容易出问题的地方和解决方案，你卡住了直接对照找。

---

## 你需要准备什么——全景图

先给你看全貌，你心里有个数。这些东西，缺一个都跑不起来：

| 组件 | 干什么的 | 最低版本要求 | 容易卡在哪 |
|------|---------|-------------|-----------|
| **Python** | 写自动化脚本 | 3.8+（建议 3.10+） | 没加入 PATH |
| **Node.js** | Appium Server 的运行环境 | **≥ 20.19.0**（Appium 3 硬性要求） | 公司电脑装的老版本不够 |
| **Appium Server** | 自动化服务端，翻译指令 | 3.x（当前最新 3.5.x） | 装完没装驱动 |
| **UiAutomator2 驱动** | 控制 Android 手机 | 最新 | Appium 3 必须手动装 |
| **Java JDK** | Android SDK 需要 Java | JDK 17+ | 版本太旧，安卓 SDK 不认 |
| **Android SDK** | 和手机沟通的桥梁 | platform-tools 最新 | ANDROID_HOME 路径配错 |
| **模拟器 / 真机** | 跑 App 设备 | Android 10+ | 连不上 adb |
| **Appium-Python-Client** | Python 发送指令给 Server | 最新 | 和 Selenium 版本冲突 |

如果你在搞 iOS 自动化还得加个 Xcode + 苹果开发者证书——那个更麻烦，不在本篇展开。这篇只讲 Android 端，因为 90% 的人入门是从 Android 开始的。

---

## 第 1 步：装 Python（假如你还没装）

```bash
python --version  # 确认 ≥ 3.8
pip --version      # 确认能用
```

没装的话去 python.org 下最新版 3.12.x，安装时**勾上「Add Python to PATH」**。这步不展开，Selenium 那篇讲过了。

---

## 第 2 步：装 Node.js——版本是第一个坑

Appium Server 是用 Node.js 写的，你得先装 Node。

去 nodejs.org 下载 LTS 版本。装完验证：

```bash
node -v
npm -v
```

这两个命令必须能跑通。

**⚠️ Appium 3 的坑在这：你必须装 Node.js ≥ 20.19.0。**

低了直接报错，而且报错信息不够明显。你可能会看到一坨 `npm ERR!` 或者 `appium: command not found`，死活想不明白是为什么。

我踩过这个坑。公司电脑上装的 Node 16，我直接 `npm install -g appium`，报了一屏红字。查了半小时才发现 Appium 3 要求的 Node 版本底线是 20.19。重装 Node 之后就好了。

**如果你电脑上已经有 Node 但版本太低：**

```bash
node -v   # 如果是 ≤ 20.18，比如 16.x 或 18.x
```

去 nodejs.org 重新下载安装包覆盖安装就行。装完再 `node -v` 确认。

**Mac 用户：** `brew install node@22` 或 `brew upgrade node`。

不推荐用 nvm 来管理 Node 版本然后给 Appium 开一个独立环境，虽然理论上可以。问题是 `npm install -g appium` 的 `-g` 是全局的，你切一次 Node 版本它就可能找不到。一步到位装最新 LTS 版最简单。

---

## 第 3 步：装 Appium Server

```bash
npm install -g appium
```

等它跑完。装完之后验证：

```bash
appium -v
```

输出应该类似 `3.5.0`。

**现在不要急着启动 Appium Server。** 你还没装驱动，启动了也用不了。继续往下走。

有个细节：`npm install -g appium` 在某些网络环境下可能很慢（特别是国内）。如果等了五分钟还没装完：

```bash
npm install -g appium --registry=https://registry.npmmirror.com
```

用淘宝镜像装，快很多。

---

## 第 4 步：装平台驱动——Appium 3 最大的变化

**Appium 2 时代，你装完 Server 就能用。Appium 3 改了——驱动必须单独装。**

装 Android 驱动（必选）：

```bash
appium driver install uiautomator2
```

装 iOS 驱动（如果你要测 iOS，而且用的是 Mac）：

```bash
appium driver install xcuitest
```

装完验证，看驱动列表：

```bash
appium driver list
```

输出大概长这样：

```
✔ Listing available drivers
- uiautomator2 [installed (npm)]
- xcuitest [installed (npm)]
```

**看到 `[installed]` 才算成功。** 如果某个驱动显示 `[not installed]`，说明没装上——后面跑脚本的时候 Appium 会报「找不到驱动」。

这步忘了的人特别多。因为网上 Appium 2 的教程不会让你装驱动，很多人以为装完 Appium Server 就完事了，结果跑脚本时报错一脸懵。

---

## 第 5 步：装 Java JDK

Android SDK 的一部分工具依赖 Java。Appium 3 推荐 JDK 17+。

去 [Oracle JDK](https://www.oracle.com/java/technologies/downloads/) 或 [Adoptium (OpenJDK)](https://adoptium.net/) 下载安装。

装完验证：

```bash
java -version
javac -version
```

两个命令都回显版本号就行。

**⚠️ 又一个坑：** Android SDK 的 `sdkmanager` 工具在某些 JDK 版本下有兼容问题。我遇到过装 JDK 21 后在 Android Studio 里下载 SDK 组件时 `sdkmanager` 报 class 版本不匹配。退到 JDK 17 就好了。所以建议你就装 JDK 17，稳。

---

## 第 6 步：装 Android SDK——这是最大的坎

Android SDK 是连接电脑和 Android 设备的桥梁。你得装它，Appium 才能通过 adb 操控手机。

**装 Android SDK 有两种方式：**

### 方式 A：装 Android Studio（推荐，一站式）

下载 [Android Studio](https://developer.android.com/studio)，安装时注意：

1. 安装向导里默认会勾选「Android SDK」和「Android Virtual Device」（模拟器），两个都勾上。
2. 装完之后打开 Android Studio，进 SDK Manager，确认至少装了**一个 Android 系统版本（建议 API 34 或 35）**和 **platform-tools**。

### 方式 B：只装命令行工具（轻量，不要 IDE）

如果你不写 Android 代码，只需要 SDK 的命令行部分：

1. 去 [Android Studio 下载页](https://developer.android.com/studio) 拉到最下面「Command line tools only」，下载对应系统的 zip。
2. 解压到一个路径，比如 `C:\android-sdk\`。
3. 用 `sdkmanager` 装必要组件：
   ```bash
   cd C:\android-sdk\cmdline-tools\latest\bin
   sdkmanager "platform-tools" "platforms;android-35"
   ```

方式 A 适合新手，方式 B 适合有洁癖的。我两种都干过——方式 A 最省心。

### 配环境变量——最多人死在这步

**Windows：**

在「系统属性 → 环境变量」里加两个变量：

```
变量名：ANDROID_HOME
变量值：C:\Users\你的用户名\AppData\Local\Android\Sdk
```

然后在 `Path` 变量里新增两行：

```
%ANDROID_HOME%\platform-tools
%ANDROID_HOME%\tools
```

**macOS/Linux（bash/zsh）：**

在 `~/.bashrc` 或 `~/.zshrc` 里加上：

```bash
export ANDROID_HOME=$HOME/Library/Android/sdk   # macOS
# 或
export ANDROID_HOME=$HOME/Android/Sdk            # Linux

export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/tools
```

然后 `source ~/.bashrc`（或重启终端）。

### 验证有没有配对

```bash
adb --version
```

看到版本号就对了。如果提示 `adb: command not found`，说明环境变量没配对——回去检查 `ANDROID_HOME` 路径和 `Path` 变量。

**我踩过的坑：** `ANDROID_HOME` 路径里不能有空格和解法字符。我同事把 SDK 装到了 `D:\Program Files\Android\Sdk`——路径中间有个空格，部分 SDK 工具直接罢工，报错还很魔幻。后来挪到 `D:\Android\Sdk` 才正常。

---

## 第 7 步：搞一个 Android 设备（模拟器 or 真机）

你要有东西跑 App。两种选择：

### 选模拟器

Android Studio 自带的 AVD（Android Virtual Device）就行。打开 Android Studio → Device Manager → Create Device → 选一个手机型号 → 选系统镜像（API 35 推荐）→ 完成。

启动模拟器之后验证连接：

```bash
adb devices
```

输出类似：

```
List of devices attached
emulator-5554   device
```

**⚠️ 模拟器性能问题：** 如果你电脑内存小于 8GB，模拟器跑起来可能会很卡，连带着 Appium 脚本超时。建议至少 16GB 内存。如果电脑配置不够，用真机。

### 选真机

拿一根数据线把手机插电脑上。

1. 手机上开启**开发者选项**（设置 → 关于手机 → 连续点 7 次「版本号」）。
2. 进入开发者选项，打开 **USB 调试**。
3. 插上数据线，手机上会弹「允许 USB 调试吗」→ 点允许。

验证连接：

```bash
adb devices
```

看到设备号就行。如果显示 `unauthorized`，说明手机上没点允许，解锁屏幕重新插拔一下。

### 模拟器和真机选哪个？

说实话，入门建议模拟器：
- 不用插线
- 重启快
- 随便翻车不心疼

真机的优势是性能好、更贴近真实用户场景。但入门阶段，一个模拟器够用了。

---

## 第 8 步：装 Python 客户端

```bash
pip install Appium-Python-Client
```

这个包是 Python 和 Appium Server 之间的桥梁。装的它会自动带上 Selenium 包作为依赖（是的，Appium 底层沿用了 Selenium 的 WebDriver 协议）。

验证装好了没有：

```bash
pip show Appium-Python-Client
```

---

## 第 9 步：跑第一个验证脚本——测试完整链路

环境搭完，别急着写用例，先跑一个极简脚本验证整个链路通不通。

新建 `test_appium.py`：

```python
from appium import webdriver
from appium.options.android import UiAutomator2Options

# 1. 配置选项
options = UiAutomator2Options()
options.platform_name = "Android"
options.automation_name = "UiAutomator2"
options.device_name = "emulator-5554"  # 模拟器名称，adb devices 看到的那个
options.app_package = "com.android.settings"  # 系统设置 App
options.app_activity = ".Settings"

# 2. 启动 Appium Session
driver = webdriver.Remote("http://localhost:4723", options=options)

# 3. 打印一下当前页面的 Activity，确认连上了
print(f"当前页面: {driver.current_activity}")

# 4. 关掉
driver.quit()
```

### 跑之前——先启动 Appium Server

新开一个终端窗口，敲：

```bash
appium
```

你会看到一屏日志，最后一行大概是：

```
[Appium] Welcome to Appium v3.5.0
[Appium] Appium REST http interface listener started on http://0.0.0.0:4723
```

**不要关这个窗口。** Appium Server 需要一直在后台跑着，你的 Python 脚本通过 `http://localhost:4723` 连它。

然后在另一个终端里跑脚本：

```bash
python test_appium.py
```

如果终端打印出 `当前页面: .Settings`（或类似的内容），**恭喜你，全链路通了。**

如果没有——跳到最后一大节「常见报错逐个拆」，对着找。

---

## 第 10 步（可选但强烈推荐）：装 Appium Inspector

Inspector 是个图形化工具，让你能看到 App 界面上每个元素的属性——这在后面写定位代码的时候是必不可少的。

Appium 3 把 Inspector 做成了插件，直接在 Server 端装：

```bash
appium plugin install inspector
```

装完之后，启动 Appium Server 时会自动带上 Inspector。然后浏览器打开：

```
http://localhost:4723/inspector
```

看到的就是 Appium Inspector 的 UI 界面。在里面填上连接参数（device name、app package 等），就能实时预览 App 的界面元素树了。

---

## 常见报错逐个拆

环境搭建阶段的报错，列出最常见的几种。你按顺序对。

### 报错一：`node: command not found` / `appium: command not found`

**原因：** Node.js 没装，或者装了没加入 PATH。

**解决：** 重新运行 Node 安装包，或者检查系统 PATH。`node -v` 能跑才是装好了。

### 报错二：`appium driver install uiautomator2` 报 502/connect timeout

**原因：** npm 源连不上。

**解决：** 加镜像源：

```bash
appium driver install uiautomator2 --source=npm --npm-registry=https://registry.npmmirror.com
```

### 报错三：`adb: command not found`

**原因：** `ANDROID_HOME` 没配对，或者 `platform-tools` 没加到 PATH。

**解决：** 重新检查环境变量。在终端里 `echo %ANDROID_HOME%`（Windows）或 `echo $ANDROID_HOME`（Mac/Linux），看输出路径是不是正确的 SDK 目录。

去那个目录下看看有没有 `platform-tools` 文件夹，里面有 `adb.exe`。

### 报错四：`could not connect to server 127.0.0.1:4723`

**原因：** 你没启动 Appium Server。

**解决：** 开一个新终端，敲 `appium`，看到那行绿色的 `listener started on http://0.0.0.0:4723` 再跑脚本。

### 报错五：`An unknown server-side error occurred ... The application at '...' does not exist or is not accessible`

**原因：** 脚本里指定的 App（比如 `com.example.app`）在模拟器/真机上没装。

**解决：** 要么把 App 的 APK 装到设备上，要么像我刚才的验证脚本一样用系统的 Settings App（`com.android.settings`）来测连通性。

### 报错六：`SessionNotCreatedException ... UiAutomator2 driver is not installed`

**原因：** 忘了装 UiAutomator2 驱动。

**解决：** `appium driver install uiautomator2`，装完 `appium driver list` 确认驱动状态。

### 报错七：模拟器启动了，但 `adb devices` 看不到

**原因：** 模拟器和 adb 不在同一用户权限下启动的。

**解决：** 先 `adb kill-server`，再 `adb start-server`，然后 `adb devices`。

### 报错八：`error: protocol fault (couldn't read status): connection reset`

**原因：** adb 连接断了。可能模拟器卡了，或者 USB 线松了。

**解决：** `adb kill-server` → `adb start-server` → `adb devices` 三连重连。

---

## 不推荐的方案：两种看似省事但后患无穷的装法

### ❌ 用 Appium Desktop 代替 Appium Server 命令行

Appium Desktop（图形界面版）2024 年就停止维护了，最后一次更新停在 Appium 1.x 时代。你装它，跑的 Appium 版本是 1.22——而现在是 3.5。中间隔了两次重大版本升级。

很多人搜「Appium 安装教程」第一条就是下载 Appium Desktop——那个教程 2019 年的，现在已经不能用了。Appium 3 只能用命令行 `npm install -g appium` 安装。

### ❌ 在 WSL 里搭 Android 开发环境

Windows 上的 WSL（Linux 子系统）跑 Android 模拟器极其痛苦——WSL 默认不支持硬件加速，模拟器慢到没法用。而且 USB 设备透传到 WSL 也要额外配置。

如果你在 Windows 上，就在 Windows 上直接搭。不要把问题复杂化。

---

## 搭完了，然后呢？

如果你跑通了验证脚本——说真的，最难的一关过了。接下来每一章都不会比这章更麻烦。

下一章讲**最小可执行链路**：从连接设备到操作元素到断言结果——一条完整的流水线。环境已经好了，开始动起来。

---

> 下一篇：《Appium 最小可执行链路：连设备 → 找元素 → 操作 → 断言》——搞懂 Appium 脚本的基本骨架。

#Appium #App自动化 #Python测试 #环境搭建 #软件测试

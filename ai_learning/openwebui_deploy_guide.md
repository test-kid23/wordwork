# Open WebUI 本地部署实战：给本地模型配上 ChatGPT 一样的界面

> **编写日期**: 2026-06-12
> **适用平台**: Windows 10/11 · Linux (Ubuntu 22.04/24.04) · macOS
> **Open WebUI 官网**: https://docs.openwebui.com
> **前置阅读**: 推荐先完成 [Ollama 部署教程](./ollama-windows-deploy-guide.md) 或 [llama.cpp 部署教程](./llama_cpp_deploy_guide.md)

## 目录

1. [为什么要用 Open WebUI？](#1-为什么要用-open-webui)
2. [环境要求](#2-环境要求)
3. [Docker 安装（强烈推荐）](#3-docker-安装强烈推荐)
   - [3.1 Windows 环境](#31-windows-环境)
   - [3.2 Linux 环境](#32-linux-环境)
   - [3.3 Docker Compose 方式](#33-docker-compose-方式)
4. [Python 安装（备选方案）](#4-python-安装备选方案)
5. [连接模型后端](#5-连接模型后端)
   - [5.1 连接本地 Ollama](#51-连接本地-ollama)
   - [5.2 连接 llama.cpp server](#52-连接-llamacpp-server)
   - [5.3 同时连接多个后端](#53-同时连接多个后端)
6. [首次配置与界面导览](#6-首次配置与界面导览)
7. [核心功能实战](#7-核心功能实战)
   - [7.1 基础对话](#71-基础对话)
   - [7.2 知识库（RAG）——让模型读你的文档](#72-知识库rag让模型读你的文档)
   - [7.3 联网搜索——让本地模型也能上网](#73-联网搜索让本地模型也能上网)
   - [7.4 多模型并发对比](#74-多模型并发对比)
   - [7.5 图像识别与生成](#75-图像识别与生成)
8. [进阶：团队部署与多用户管理](#8-进阶团队部署与多用户管理)
9. [常见报错排查](#9-常见报错排查)
10. [总结：你的本地 AI 工作站](#10-总结你的本地-ai-工作站)

---

## 1. 为什么要用 Open WebUI？

**如果你已经用 Ollama 或 llama.cpp 跑起了本地大模型，那恭喜你——你已经有了引擎，但还缺一个驾驶舱。**

Ollama 和 llama.cpp 的默认交互方式都是**命令行**：

- Ollama：`ollama run qwen2.5:7b`，黑底白字的终端对话
- llama.cpp：`./llama-cli -m model.gguf -p "你好"`，更原始的 CLI

命令行没问题，但**不像一个现代 AI 产品**——没有对话历史管理、没有 Markdown 渲染、没有图片识别、没法上传 PDF 让 AI 帮你读。

**Open WebUI 就是来解决这个问题的。**

它给你的本地大模型配上一个**和 ChatGPT 几乎一模一样的 Web 界面**，但完全运行在你自己的电脑上，数据不离本地，零成本、零隐私泄露。

### Open WebUI 的核心能力

| 能力 | 一句话说明 |
|------|-----------|
| 🗣️ **类 ChatGPT 对话** | Markdown 渲染 + 代码高亮 + 深色模式 |
| 📚 **知识库（RAG）** | 上传 PDF/Word/Excel，AI 基于你的文档回答 |
| 🔍 **联网搜索** | 集成 Google/DuckDuckGo，本地模型也能上网查资料 |
| 🔀 **多模型并发** | 一个窗口同时和两个模型对话，实时对比效果 |
| 🖼️ **图像识别** | 上传图片，让多模态模型（如 Llava、Qwen-VL）看图说话 |
| 👥 **多用户管理** | 建账号、分权限、按角色分配模型，团队共享 |
| 🔌 **插件生态** | Pipelines、MCP 协议、第三方工具接入 |

> Open WebUI 原名 Ollama WebUI，虽然名字变了，但它连接 Ollama 依然是**最丝滑**的场景。同时也支持连接 OpenAI API、llama.cpp server、vLLM 等任何 OpenAI 兼容后端。

---

## 2. 环境要求

| 组件 | 最低要求 | 推荐 |
|------|----------|------|
| **Docker** | Docker Engine 24+ | Docker Desktop 26+ |
| **内存**（仅 Open WebUI） | 2 GB RAM | 4 GB RAM |
| **磁盘** | 5 GB 可用空间 | 20 GB+（含模型） |
| **Ollama** 或 **llama.cpp server** | 已安装且正常运行 | 已配置模型 |
| **浏览器** | Chrome/Edge/Firefox 最新版 | Chrome 最新版 |

> **不需要 GPU**：Open WebUI 本身只是界面层，不需要显卡。GPU 需求取决于你用的推理引擎（Ollama / llama.cpp）。

**Windows 用户注意**：安装 Docker 前需要确认：
- Windows 10 版本 ≥ 21H2，或 Windows 11
- 在 BIOS 中开启虚拟化（VT-x / AMD-V）
- WSL 2 已正确安装（Docker Desktop 会自动帮你装）

**Linux 用户**：直接安装 Docker Engine 即可，比 Windows 更精简。

---

## 3. Docker 安装（强烈推荐）

> Docker 是官方强烈推荐的方式，也是**最省心**的方式——一条命令跑起来，升级也只需要重新拉镜像。

### 3.1 Windows 环境

#### Step 1：安装 Docker Desktop

1. 访问 [Docker Desktop 下载页](https://www.docker.com/products/docker-desktop/)
2. 下载 Windows 版安装包
3. 双击安装，保持默认选项，中间会自动安装 WSL 2（如果还没有的话）
4. 安装完成后**重启电脑**
5. 重启后 Docker Desktop 会自动启动，任务栏右下角看到 Docker 鲸鱼图标即为成功

验证：

```powershell
docker version
docker run hello-world
```

看到 "Hello from Docker!" 就说明 Docker 已经可以正常使用了。

#### Step 2：拉取并启动 Open WebUI

```powershell
# 拉取镜像
docker pull ghcr.io/open-webui/open-webui:main

# 启动容器（关键参数说明见下方）
docker run -d `
  -p 3000:8080 `
  --add-host=host.docker.internal:host-gateway `
  -v open-webui:/app/backend/data `
  --name open-webui `
  --restart always `
  ghcr.io/open-webui/open-webui:main
```

**参数说明**：

| 参数 | 含义 |
|------|------|
| `-d` | 后台运行容器 |
| `-p 3000:8080` | 把容器的 8080 端口映射到本机的 3000 端口 |
| `--add-host=...` | **关键！** 让 Docker 容器能访问宿主机上运行的 Ollama |
| `-v open-webui:...` | 数据持久化容器卷，聊天记录、配置都存在这里 |
| `--name open-webui` | 给容器起个名字 |
| `--restart always` | Docker 重启后自动启动容器 |

#### Step 3：打开浏览器

访问 **http://localhost:3000**，你应该看到 Open WebUI 的注册页面。

> **如果是第一次使用**：注册一个管理员账号。第一个注册的账号自动成为管理员，后续注册的用户需要你审批后才能登录。

---

### 3.2 Linux 环境

#### Step 1：安装 Docker Engine

```bash
# Ubuntu 快速安装
curl -fsSL https://get.docker.com | sh

# 把当前用户加入 docker 组（免 sudo）
sudo usermod -aG docker $USER

# 重新登录或执行
newgrp docker

# 验证
docker version
```

#### Step 2：启动 Open WebUI

```bash
docker run -d \
  -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

#### GPU 加速版本（NVIDIA 显卡）

如果想让 Open WebUI 内部的嵌入模型（用于 RAG）也跑在 GPU 上：

```bash
# 先安装 NVIDIA Container Toolkit
# 参考：https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html

docker run -d \
  -p 3000:8080 \
  --gpus all \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:cuda
```

> 注意这里用 `open-webui:cuda` 标签而不是 `:main`。普通用户不需要这一行，"无 GPU"版本完全够用。

---

### 3.3 Docker Compose 方式

如果你更喜欢用配置文件管理，创建 `docker-compose.yml`：

```yaml
services:
  openwebui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    ports:
      - "3000:8080"
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - open-webui:/app/backend/data
    restart: always

volumes:
  open-webui:
```

启动：

```bash
docker compose up -d
```

---

### 镜像更新

```bash
# 拉取最新镜像
docker pull ghcr.io/open-webui/open-webui:main

# 删除旧容器
docker rm -f open-webui

# 用同样的命令重新创建容器（数据在 Volume 中不会丢失）
docker run -d ...  # 和上面一样的参数
```

> **生产环境建议固定版本号**，比如用 `open-webui:v0.9.6` 而不是 `:main`，避免自动更新导致不兼容。

---

## 4. Python 安装（备选方案）

如果你不想装 Docker（比如电脑配置低、公司限制安装容器软件），可以用 pip 直接安装。

**前置条件**：Python 3.11（不支持 3.13 及以上版本）

```bash
# 推荐用虚拟环境隔离
python -m venv openwebui-env
source openwebui-env/bin/activate  # Windows: openwebui-env\Scripts\activate

# 安装
pip install open-webui

# 启动（默认监听 8080 端口）
open-webui serve

# 或指定端口
open-webui serve --port 3000
```

访问 **http://localhost:8080**（或你指定的端口）。

> **Python 方式的限制**：
> - 不提供自动重启功能（需要手动配合 systemd 或任务计划程序）
> - 依赖 Python 3.11，版本管理稍微麻烦
> - 升级需要 `pip install -U open-webui`
> - 不如 Docker 稳定，偶尔会有 Python 环境冲突
>
> 总之：能 Docker 就 Docker，实在不行再用 Python。

---

## 5. 连接模型后端

Open WebUI 本身不带推理引擎，它需要连接一个或多个"模型后端"。最常见的是连接**本地 Ollama**。

### 5.1 连接本地 Ollama

如果你按照之前的教程装好了 Ollama，那么 Open WebUI **默认就会自动检测到本机的 Ollama**。

前提是你启动 Docker 时加了 `--add-host=host.docker.internal:host-gateway` 参数。

验证方法：打开 Open WebUI → 左上角选择模型 → 应该能看到你 Ollama 中已下载的模型列表。

**如果看不到模型**，检查以下配置：

```
# 确保 Ollama 监听所有网络接口
# Windows：打开系统环境变量，添加
OLLAMA_HOST=0.0.0.0

# Linux：
sudo systemctl edit ollama
# 添加：
[Service]
Environment="OLLAMA_HOST=0.0.0.0"

# 重启 Ollama
sudo systemctl restart ollama
```

然后在 Open WebUI 的 **Settings → Connections** 中，确保 Ollama Base URL 是：

```
http://host.docker.internal:11434
```

---

### 5.2 连接 llama.cpp server

如果你用的是 llama.cpp 的 `llama-server`（参考上一篇文章），Open WebUI 也能对接！

llama.cpp server 提供了 OpenAI 兼容 API，Open WebUI 原生支持 OpenAI 格式的后端：

1. 先确保 `llama-server` 正在运行：

```bash
./build/bin/llama-server \
  -m ./models/qwen2.5-7b-Q4_K_M.gguf \
  --n-gpu-layers -1 \
  --ctx-size 8192 \
  --host 0.0.0.0 \
  --port 8081
```

2. 在 Open WebUI 的 **Settings → Admin Settings → Connections → OpenAI API** 中添加：

| 字段 | 值 |
|------|-----|
| URL | `http://host.docker.internal:8081/v1` |
| Key | `not-needed`（llama-server 默认不需要 key） |
| Prefix ID | `llamacpp`（可选，用于区分模型来源） |

3. 点击"刷新模型列表"，你的 llama.cpp 模型就会出现在模型选择器中。

---

### 5.3 同时连接多个后端

Open WebUI 支持**同时连接多个后端**：

- 本地 Ollama（自动检测）
- 本地 llama.cpp server（手动配置 OpenAI 格式）
- 远程 OpenAI API（填入 API Key 即可）
- 其他兼容 OpenAI 格式的服务（如 vLLM、LocalAI 等）

所有模型会统一出现在模型选择器中，用标签区分来源，切换无缝。

---

## 6. 首次配置与界面导览

打开 **http://localhost:3000** 后，你会看到：

### 注册/登录页面

- 第一次访问会要求你**注册管理员账号**
- 输入用户名、邮箱、密码
- **第一个注册的用户自动成为管理员**，后续用户注册需要你审批

### 主要界面布局

```
┌──────────────────────────────────────────────────┐
│  侧边栏          │         主聊天区域              │
│                  │                                │
│  📝 新建对话      │  你好！我是 Qwen2.5-7B...       │
│  ────────────   │                                │
│  💬 对话历史      │  ┌用户消息┐                    │
│  · 昨天的讨论     │  └────────┘                    │
│  · 翻译任务      │  ┌AI 回复 ──────────┐          │
│  · ...          │  │Markdown 渲染      │          │
│                  │  │代码高亮           │          │
│  📚 知识库       │  └──────────────────┘          │
│  🔌 工作空间     │                                │
│                  │  ┌─────────────────┐           │
│  ⚙️ 设置        │  │ 输入框           │ 发送     │
│                  │  └─────────────────┘           │
└──────────────────────────────────────────────────┘
```

**关键区域说明**：

| 区域 | 功能 |
|------|------|
| **左上角模型选择器** | 切换当前使用的模型 |
| **对话历史** | 自动保存、可搜索 |
| **输入框** | 支持粘贴图片（多模态模型）、上传文件（RAG） |
| **知识库** | 管理文档集合，RAG 功能入口 |
| **工作空间** | 可接入 Pipelines 和外部工具 |
| **设置** | 通用设置 + 管理员设置 |

---

## 7. 核心功能实战

### 7.1 基础对话

和 ChatGPT 一样的体验：

- 选择模型 → 输入问题 → 回车发送
- 支持 Markdown 排版、代码块高亮、数学公式（LaTeX）
- 对话历史自动保存，左侧可搜索
- 支持**编辑已发送的消息**，重新生成 AI 回复
- 支持**对话重命名**、**归档**、**导出**

**暗藏功能**：在聊天中随时切模型。比如先用 Qwen2.5-7B 聊了几轮，觉得质量不够，直接把模型选择器切换到 DeepSeek-R1-32B，**对话上下文不丢失**，继续聊。

### 7.2 知识库（RAG）——让模型读你的文档

这是 Open WebUI **最杀手级的本地功能**——让 AI 基于你自己的私有文档回答。

#### 操作步骤：

**Step 1：创建知识库**

```
侧边栏 → 📚 知识库 → 点击"创建知识库"
输入名称，例如"公司手册"、"论文资料"、"技术文档"
```

**Step 2：上传文档**

- 支持格式：PDF、Word（.docx）、Excel（.xlsx）、PPT（.pptx）、.txt、.md、.csv、.html、.xml 等
- 拖拽或点击上传
- 自动分块（Chunking）并向量化
- 可以上传多个文件，也可以导入网页链接

**Step 3：在对话中使用**

在聊天输入框中输入 `#`，会弹出你的知识库列表，选择一个后：

```
#公司手册 今年的年假政策是什么？
```

模型就会基于你上传的员工手册来回答，而不是用通用知识瞎编。

#### 效果展示（示意）：

> **你**：#技术文档 这个 API 接口的超时时间是多久？
>
> **模型**：根据《后端 API 文档 v2.3》第 3.2 节，默认超时时间为 30 秒，可通过 `timeout` 参数调整，最大 120 秒。
>
> （来源：[后端 API 文档 v2.3.pdf，第 3.2 节]）

#### 高级用法：

- **混合检索**：同时用关键词匹配 + 语义理解
- **分块控制**：可调分块大小、重叠量
- **多知识库**：一次对话引用多个知识库，比如同时查"合同模板"和"法律条文"
- **实时更新**：知识库文件改了，索引会自动更新

> 这对职场人来说是**生产力神器**——把公司所有的 SOP、产品文档、历史邮件丢进去，AI 变成你最靠谱的内部顾问。

### 7.3 联网搜索——让本地模型也能上网

本地模型的知识停留在训练截止日期，2026 年 7 月发生的事它肯定不知道。

**解决**：开启联网搜索功能。

**设置步骤**：

1. 进入 **Settings → Admin Settings → Web Search**
2. 开启 Web Search
3. 选择搜索引擎：

| 搜索引擎 | 优点 | 配置难度 |
|----------|------|----------|
| **DuckDuckGo** | 免费、无需 API Key | ⭐ 极简（推荐新手） |
| **Google PSE** | 结果更精准 | ⭐⭐ 需申请 API Key |
| **SearXNG** | 自托管、隐私最佳 | ⭐⭐⭐ 需自己搭服务 |

**DuckDuckGo 配置（最简单）**：

直接选择 DuckDuckGo，不需要任何 Key，保存即可。

**使用方式**：

在聊天时，输入框旁边的"联网搜索"开关，打开后：

```
最近一周 AI 领域有什么重大新闻？
```

模型会：
1. 自动判断"这个问题需要联网" → 触发搜索
2. 检索 DuckDuckGo 结果
3. 把搜索结果注入上下文
4. 基于搜索 + 内建知识综合回答
5. 附上来源链接

**注意**：联网搜索会增加响应时间 5-15 秒，因为它要先搜再读再回答。

### 7.4 多模型并发对比

当你纠结"这个问题让 Qwen3 回答还是 DeepSeek-R1 回答更好"时，不用反复切换模型测试——**两个模型同时上**。

#### 使用方法：

1. 创建新对话
2. 在输入框右上角，找到"多模型"图标（两个重叠的圆圈）
3. 选择两个（或多个）模型
4. 输入问题后，两个模型的回复会**左右并排显示**

#### 典型场景：

- **翻译对比**：左边 Qwen2.5，右边 DeepSeek-R1，看谁翻得更地道
- **代码对比**：左边 CodeQwen，右边 DeepSeek-Coder，看谁的方案更优
- **质量检查**：一个模型生成内容，另一个模型做审核
- **模型选型**：不知道升级到新模型值不值得 → 直接 A/B 对比

### 7.5 图像识别与生成

Open WebUI 支持多模态，前提是你的后端模型本身支持。

#### 图像识别

支持的模型（需要你自己下载对应的多模态版本）：
- **Llava** 系列
- **Qwen-VL** 系列
- **Llama 4**（原生支持视觉）
- 其他任何具有视觉能力的开源模型

**使用方法**：在输入框中直接粘贴或拖入图片，输入"描述这张图片里有什么"，模型就会看图回答。

#### 图像生成

Open WebUI 本身不生成图像，但可以**对接外部图像生成后端**：

- **ComfyUI**：功能最强大的本地图像生成工作流
- **Automatic1111 / SD WebUI**：稳定的 Stable Diffusion 界面
- **DALL-E**：OpenAI 的图像生成 API

配置路径：**Admin Settings → Images → 启用图像生成 → 填入后端 URL**

---

## 8. 进阶：团队部署与多用户管理

如果你想把部署的 Open WebUI 分享给同事或朋友，而不仅仅是自己用，就需要了解多用户功能。

### 用户管理

**Admin Settings → Users**：

| 功能 | 说明 |
|------|------|
| **注册审批** | 开启后，新用户注册需要你手动批准 |
| **角色分配** | Admin（管理员）/ User（普通用户） |
| **模型权限** | 按用户组分配可用模型——比如实习生只能用 7B 小模型 |
| **对话审计** | （需用户同意开启隐私设置）查看用户的对话内容 |
| **禁用/删除** | 管理不活跃或有问题的账号 |
| **邮箱白名单** | 只允许特定域名（如 `@company.com`）注册 |

### 部署架构建议

```
┌─────────────────────────────────────┐
│        公司内网 / 同一台机器          │
│                                     │
│  Ollama / llama.cpp server          │
│  (GPU 推理, 端口 11434)              │
│         ▲                           │
│         │ 模型推理                    │
│         ▼                           │
│  Open WebUI (Docker, 端口 3000)      │
│         ▲                           │
│    ┌────┼────┐                      │
│    ▼    ▼    ▼                      │
│  用户A 用户B 用户C                    │
│  (浏览器访问 192.168.x.x:3000)       │
└─────────────────────────────────────┘
```

1. **推理服务器**：Ollama 或 llama.cpp server 跑在 GPU 机器上
2. **Web 界面**：Open WebUI 跑在同一台或另一台机器
3. **用户访问**：同事通过局域网浏览器访问

这样**一台机器上的 GPU 可以共享给全团队使用**，每个人有自己的账户和对话历史，互不干扰。

---

## 9. 常见报错排查

### Top 5 常见问题

**1. 打开 http://localhost:3000 什么也没有**

> → Docker 容器可能没有正确启动
> 
> ```bash
> docker ps   # 查看 open-webui 是否在运行
> docker logs open-webui   # 查看日志
> ```

**2. "Ollama connection failed" / 看不到模型**

> → **90% 的情况是因为没有加 `--add-host` 参数**
> 
> ```bash
> # 删除旧容器
> docker rm -f open-webui
> 
> # 重新创建（务必包含 --add-host）
> docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway ...
> ```

**3. 上传 PDF 后 RAG 没效果**

> → 检查嵌入模型是否已下载：
> 在 Admin Settings → Documents 中，确认默认嵌入模型（如 `nomic-embed-text`）已存在。
> 
> ```bash
> # 如果用的 Ollama，先拉取嵌入模型
> ollama pull nomic-embed-text
> ```

**4. 网页搜索无法使用（DuckDuckGo）**

> → 网络问题。DuckDuckGo 的默认 API 在国内可能被墙或速度慢。可以尝试：
> - 配置代理（Open WebUI 本身支持 HTTP_PROXY 环境变量）
> - 切换到 Google PSE（需要申请 API Key，但结果更稳定）
> - 搭 SearXNG 自托管（最稳定，但需要额外部署）

**5. Docker Desktop 启动失败（Windows）**

> → 检查：
> 1. BIOS 中虚拟化是否开启（VT-x / AMD-V）
> 2. WSL 2 是否正常：`wsl --version`
> 3. 是否安装了其他虚拟化软件（VirtualBox 等可能冲突）
> 4. Windows 版本是否低于 21H2

**6. 容器重启后聊天记录丢失**

> → 没有挂载数据卷（`-v open-webui:/app/backend/data`）。数据卷是持久化的关键，务必包含此参数。

---

## 10. 总结：你的本地 AI 工作站

恭喜你，现在你已经拥有了一个**完全本地化、和 ChatGPT 体验一致、但数据零泄露的 AI 工作站**。

让我们回顾一下整个技术栈：

```
┌─────────────────────────────────────────────┐
│                浏览器 (你的电脑)               │
│              http://localhost:3000            │
│                   Open WebUI                 │
│         类 ChatGPT 界面 · RAG · 联网搜索      │
└──────────────────┬──────────────────────────┘
                   │ OpenAI 兼容 API
┌──────────────────▼──────────────────────────┐
│           推理引擎 (同一台或另一台电脑)          │
│                                              │
│  ┌─────────────┐   ┌───────────────────┐     │
│  │   Ollama    │   │  llama.cpp server │     │
│  │  (易用入门)  │   │  (高性能推理)       │     │
│  └─────────────┘   └───────────────────┘     │
│                   GGUF 模型                   │
│          Qwen3 · DeepSeek · Llama 4          │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│               你的 GPU / CPU                  │
│         RTX 4090 / RTX 3060 / M2 Ultra       │
└─────────────────────────────────────────────┘
```

### 三篇文章的完整学习路径

| 阶段 | 文章 | 你学到什么 |
|------|------|-----------|
| 🟢 **入门** | [Ollama 部署教程](./ollama-windows-deploy-guide.md) | 5 分钟跑起本地大模型 |
| 🟡 **进阶** | [llama.cpp 部署教程](./llama_cpp_deploy_guide.md) | 从源码编译，深度掌控推理引擎 |
| 🔴 **实战** | **本文** ← 你在这里 | 给本地模型配上 ChatGPT 同款界面 + RAG + 联网 |

### 下一步可以做什么

- 搭一个知识库，把你的笔记/文档/合同都丢进去
- 开联网搜索，让本地模型也能回答实时问题
- 试试多模型对比，找到最适合你场景的模型
- 分享给同事，一起用一台 GPU 机器
- 探索 Pipelines 插件，写自定义的中转逻辑

> **你已经不再是"玩玩 AI"了——你正在搭建属于自己的、完整的本地 AI 工作体系。** 下一步，我们聊聊怎么把多个 AI 工具串联成自动化的 AI Agent 工作流。敬请期待！

---

## 快速上手 Checklist

- ☐ 安装 Docker Desktop（Windows）/ Docker Engine（Linux）
- ☐ 确保 Ollama 或 llama.cpp server 正在运行
- ☐ 拉取 Open WebUI 镜像：`docker pull ghcr.io/open-webui/open-webui:main`
- ☐ 启动容器（务必带 `--add-host` 参数）
- ☐ 浏览器访问 http://localhost:3000
- ☐ 注册管理员账号
- ☐ 确认能看到本地模型
- ☐ 试一个简单对话
- ☐ 上传一份 PDF 创建知识库，试试 RAG
- ☐ 打开联网搜索，问一个实时问题
- ☐ （可选）拉同事注册账号，体验多用户模式

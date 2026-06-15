# OpenHuman 系列创作大纲

> OpenHuman —— 你的个人 AI 超级智能，几分钟就懂你
>
> 源码：https://github.com/tinyhumansai/openhuman | tinyhumansai 出品 | GPL-3.0 协议 | 32k+ Stars

---

## 项目速写

**OpenHuman** 是一个开源的个人 AI 助手，定位和所有你见过的 AI 工具都不一样：它不只跟你聊天，而是真正"住进"你的设备、接入你的日常工作栈、持续自动拉取你的数据、构建关于你的记忆树，让你在和 AI 初次对话的几分钟内，它就了解你的工作、你的日程、你的项目——无需几天甚至几周的训练期。

如果说 Claude Code 是程序员的终端 Agent、OpenClaw 是多渠道消息助手、Hermes 是自我学习型 Agent，那 OpenHuman 的差异化在于：**它是为"普通人"设计的开箱即用全栈 AI 助手**——有桌面 UI（还有吉祥物表情！）、一键接入 118+ 第三方服务、自动每 20 分钟拉取最新数据、本地优先的记忆树 + Obsidian 知识库、TokenJuice 智能压缩省 80% 成本。

**四个字概括：本地记忆，云端能力。**

| 维度 | 说明 |
|------|------|
| 出品方 | tinyhumansai（Senam Akel 创始） |
| 定位 | UI 优先、开箱即用的个人 AI 超级智能 |
| 核心技术栈 | Rust 61.5% + TypeScript 35.6%（Tauri 桌面壳 + Web UI + Rust 内核） |
| 许可证 | GPL-3.0 |
| 交互方式 | 桌面应用（主要）+ 桌面吉祥物 + 语音 + Google Meet 参会 |
| 模型接入 | OpenHuman 后端自动路由（一个订阅覆盖所有模型）+ 可选本地 Ollama |
| 核心差异化 | Memory Tree + Obsidian 知识库、20 分钟自动同步、118+ 集成、TokenJuice 压缩、桌面吉祥物 |

**跟本系列其他工具的关系（给读者的定位地图）：**
- **Claude Code**：你写代码时的 AI 同事，终端里的 Agent
- **OpenClaw**：你的多渠道 AI 管家，微信/Telegram/Discord 统一入口
- **Hermes Agent**：会自我进化的 Agent，内置学习回路
- **OpenHuman**：开箱即用的全栈个人 AI，**唯一有 UI 桌面应用 + 自动同步 + Memory Tree** 的选项

它们在 wordwork 系列里不是"四选一"，而是**四种场景的分工**：写代码用 Claude Code，跨平台交互用 OpenClaw，要 Agent 学习能力用 Hermes，想要开箱即用全栈助手用 OpenHuman。

---

## 第一部分：入门教程系列

### 1.1 OpenHuman 是什么？—— 一个几分钟就懂你的 AI
- 一句话定位：开源桌面 AI 助手，接入你的数据 → 构建记忆 → 马上能帮你干活
- "几分钟就懂你"是怎么做到的：连接账号 → 自动拉取数据 → Memory Tree 压缩 → 立即可用
- 跟 ChatGPT/Claude 桌面端的根本不同：不是聊天窗口，是连接你整个数字生活的代理
- 跟 OpenClaw / Hermes 的差异化：
  - 唯一有桌面应用 + 吉祥物的
  - 唯一支持 20 分钟自动数据同步的
  - 唯一内置 Token 压缩层（TokenJuice）
- 吉祥物是什么：一个会说话、会表情、能"活"在桌面角落里的小角色
- 谁最适合用 OpenHuman：不想折腾配置的普通人、需要整合多平台数据的知识工作者、想一个账号覆盖所有模型的用户

### 1.2 安装与首次启动：从零到 AI 桌面伙伴
- 安装方式速览：
  - macOS：`brew tap tinyhumansai/core && brew install openhuman`
  - Linux (Debian/Ubuntu)：签名 apt 仓库安装
  - Windows：下载签名 .msi 安装包
- 为什么推荐原生包管理器安装：签名验证，安全性最好
- 首次启动：创建账号、基础配置、选择语言
- 吉祥物亮相：认识你的桌面 AI 伙伴
- 设置引导：几分钟内从"我是谁"到"它能干什么"
- 本地 + 托管服务的混合架构解读：什么存在本地、什么走云端、为什么

### 1.3 连接你的数字生活：118+ 集成一键接入
- 什么是集成（Integration）：OpenHuman 连接你已有服务的桥梁
- 支持的集成类别概览：
  - 邮箱：Gmail
  - 日历：Google Calendar
  - 文档协作：Notion、Google Drive
  - 代码托管：GitHub
  - 即时通讯：Slack、Discord
  - 项目管理：Linear、Jira
  - 支付/商务：Stripe
- OAuth 一键授权：无需手动填 API Key
- Managed vs Direct 模式：默认走 OpenHuman 托管层，也可以自配 Composio
- 连接后的第一个 20 分钟：自动同步发生了什么
- 实战：连接 Gmail + Calendar + Notion，看看 OpenHuman 知道了什么

### 1.4 第一次对话：让 OpenHuman 帮你做点实事
- 理解了你的数据后，AI 能回答什么：
  - "我今天有什么会？"
  - "帮我把上周 Notion 里的会议纪要整理成周报"
  - "GitHub 上最近谁给我提了 PR？"
- 内置工具巡览：
  - 网页搜索 + 内容抓取
  - 文件系统操作（读/写/搜索）
  - 代码工具（Git、Lint、测试、Grep）
  - 原生语音（STT 语音输入 + ElevenLabs TTS 语音输出）
- 吉祥物的交互方式：说话、表情反馈、背景持续思考
- 桌面应用 vs 命令行：两种使用方式的选择

---

## 第二部分：核心功能系列

### 2.1 Memory Tree 与 Obsidian 知识库：AI 如何"记住"你的一切
- Memory Tree 是什么：层次化记忆树的数据结构
- 数据是怎么被处理的：
  - 连接的服务数据 → 自动拉取 → 切成 ≤3000 Token 的 Markdown 块
  - 打分排序 → 构建层次化摘要树 → 存入本地 SQLite
- 同一份数据流入 Obsidian 兼容的 Markdown 知识库：你能直接打开浏览和编辑
- Karpathy 的 obsidian-wiki 工作流启发：这思路从哪来、为什么好用
- 实战：打开 Obsidian 知识库，看看 AI 眼中的"你"长什么样
- 记忆的持久性：关掉应用再打开，AI 还记得什么
- agentmemory 后端：如果你已经在用 Claude Code/Cursor/Codex 的 agentmemory，可以直接对接

### 2.2 Auto-Fetch：AI 自动"学习"你的世界
- 20 分钟自动同步循环：OpenHuman 最独特的能力
- 不需要写任何轮询脚本：连接即同步
- 同步了什么：新邮件、日历变更、Notion 更新、GitHub 动态、Slack 消息……
- "昨天的上下文今天早上就有了"：不用每次对话前手动喂数据
- 实战观察：连接 Gmail 和 Calendar 一小时后，问问 AI"今天有什么重要的事"
- 自动同步与隐私的平衡：数据拉到你本地，不是上传到云端训练

### 2.3 TokenJuice：AI 对话的"省油模式"
- Token 成本是什么：为什么 AI 对话会越来越贵
- TokenJuice 做了什么：
  - HTML → Markdown 转换（网页抓取省掉大量无意义标签 Token）
  - 长 URL 自动缩短
  - 工具输出的去重与摘要
  - CJK/Emoji 等宽字符逐字保留（不会乱码）
- 效果：**最高省 80% 的 Token 消耗**，同样的钱聊更久
- 跟直接调 API 不带压缩的成本对比
- TokenJuice 的"智能"在哪：不是粗暴截断，是有规则的精简
- 实战：同一组操作，开 vs 关 TokenJuice 的 Token 消耗对比

### 2.4 桌面吉祥物与语音交互：AI 的"肉身"
- 吉祥物不是噱头：它是什么、能做什么
  - 说话：TTS 语音输出 + 嘴型同步
  - 表情反应：根据对话内容做出表情变化（Rive 动画）
  - 背景思考：你没在打字的时候它也在处理
  - Google Meet 参会：作为真实参会者加入会议
- 语音交互全链路：
  - STT 语音转文字输入（你想说就说）
  - ElevenLabs TTS 文字转语音输出（AI "说"给你听）
- 为什么"有脸的 AI"体验完全不同：情感连接与注意力锚点
- 实战：让 OpenHuman 的吉祥物加入你的 Google Meet，会后自动生成纪要

### 2.5 模型路由：一个账号，所有模型
- OpenHuman 的模型路由策略：自动为每类任务选最合适的模型
  - 推理任务 → 推理模型
  - 快速响应 → 轻量模型
  - 视觉任务 → 多模态模型
- 一个订阅覆盖所有模型：不用分别注册 OpenAI / Anthropic / Google
- 可选本地模式：Ollama 接入，离线场景也能用
- 模型切换的透明性：用户不需要知道背后用了哪个模型
- 跟"自己管 API Key"的模式对比：省心 vs 灵活

---

## 第三部分：进阶实战系列

### 3.1 OpenHuman 的工作空间管理
- 工作空间的组织结构
- `.agents/`、`.claude/`、`.codex/` 目录的作用
- AGENTS.md / CLAUDE.md：注入项目级指令
- 工作空间配置与 Git 版本控制
- 多项目工作空间的隔离与切换

### 3.2 编码工具集的深度使用
- OpenHuman 内置的完整编码工具箱：
  - 文件系统操作（读/写/搜索文件）
  - Git 集成（查看 diff、提 PR、管理分支）
  - Lint 与测试运行
  - Grep 代码搜索
- 跟 Claude Code 的编码能力对比
- 什么时候用 OpenHuman 写代码、什么时候切 Claude Code
- 实战：让 OpenHuman 在一个项目中修 Bug + 跑测试 + 提 PR

### 3.3 消息渠道与自动化工作流
- OpenHuman 的消息收发能力
- 跨渠道的上下文连续性
- 工作流自动化：定时任务、事件触发
- 利用 118+ 集成编排复杂工作流
- 实战：每天早上自动汇总 Gmail + Slack + GitHub 动态，生成简报推送到手机

### 3.4 安全、隐私与本地优先架构
- "本地优先"到底是什么意思：什么存在本地、什么走云端
- 本地数据：Memory Tree、Markdown 知识库、工作空间配置、运行时状态
- 托管服务：账户登录、模型路由、网页搜索代理、OAuth 流程
- 加密与数据归属：你的数据是你的
- 自定义/本地设置：自建模型、自配 Composio、自管搜索
- 安全最佳实践清单

### 3.5 从零打造你的"数字分身"
- 数字化"你"的完整路径：
  - 第一步：接入所有日常服务（邮件、日历、文档、代码、通讯）
  - 第二步：让 auto-fetch 跑一周，积累你的数据画像
  - 第三步：打开 Obsidian 知识库，审核和编辑 AI 对"你"的认知
  - 第四步：调教工作流和回复风格
- 定制你的 AGENTS.md / CLAUDE.md
- 数字分身的边界：哪些决定 AI 可以做、哪些必须你来
- 长期维护：数据清理、记忆审计、模型升级

---

## 第四部分：踩坑与最佳实践

### 4.1 安装与配置常见问题
- macOS：Homebrew tap 安装失败排查
- Linux：apt 仓库签名问题、Wayland 下 AppImage 崩溃处理
- Windows：MSI 安装权限问题
- 首次启动卡住：网络、代理、防火墙
- Rust 工具链：源码编译的环境要求（Rust 1.93.0+、Node.js 24+、pnpm 10.10.0）
- 从源码构建的注意事项

### 4.2 集成连接的排查与修复
- OAuth 授权过期：表现与处理
- 某个集成不拉数据：权限、配额、API 变更
- Composio 连接器层的故障排查
- auto-fetch 的间歇性中断：原因与恢复
- 重新授权 vs 删除重连：什么时候该怎么做

### 4.3 性能与成本管理
- 桌面应用的资源占用预期
- Memory Tree 的大小增长趋势与维护
- TokenJuice 的压缩比例监测
- 订阅费用的实际使用体验
- 本地 Ollama  vs 托管模型的成本与质量权衡
- 什么场景值得自建模型路由

### 4.4 综合案例：用 OpenHuman 管理个人知识工作流
- 场景：一个知识工作者的日常
- 配置：Gmail + Calendar + Notion + GitHub + Slack
- 第一个月的变化路径：
  - 第一周：AI 了解你的基本信息和日程
  - 第二周：AI 开始能帮你总结和提醒
  - 第三周：AI 主动发现你的工作模式
  - 第四周：AI 成为你不可或缺的工作伙伴
- 与其他工具的配合：什么时候切 Claude Code、什么时候用 OpenClaw
- 最终复盘：哪些环节 AI 替代了人力、哪些仍然是人的领地

---

## 附录

### A. 常用操作速查表
- 安装命令（各平台）
- 核心配置路径
- 关键目录结构

### B. 与其他 Agent 工具的定位对比表
- OpenHuman vs Claude Code vs OpenClaw vs Hermes Agent
- 按使用场景推荐：谁适合用哪个

### C. 官方资源与社区索引
- GitHub：https://github.com/tinyhumansai/openhuman
- 官方网站：tinyhumans.ai/openhuman
- 官方文档
- Discord / Reddit / X(Twitter)
- 桌面吉祥物动画：Rive（`tiny_mascot.riv`）

### D. 更新日志
- 跟随 OpenHuman 版本更新持续同步（当前基准：v0.57.40）

---

*本大纲基于 tinyhumansai/openhuman 官方仓库（github.com/tinyhumansai/openhuman）信息与个人实践理解编写，内容为独立理解与表述。具体文章写作中如需引用官方原文或示例，将注明出处。大纲随 OpenHuman 版本更新持续迭代。*

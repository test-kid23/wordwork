# Hermes Agent 系列创作大纲

> Hermes Agent —— 会自我进化的 AI 代理，越用越懂你
>
> 源码：https://github.com/NousResearch/hermes-agent | Nous Research 出品 | MIT 协议 | 19k+ Stars

---

## 项目速写

**Hermes Agent** 是 Nous Research 打造的一个**自我改进型 AI 代理**。它不是普通的"调 API 聊天机器人"，而是内置了完整学习回路的自主代理——它能从对话中学到经验、自动创建可复用技能、在使用中不断改进这些技能、跨会话记忆你的偏好和习惯，像有记忆一样持续成长。

**跟 OpenClaw 的关系值得单独说明：** 两者在某些场景存在交集，但定位有本质差异。Hermes 更偏向"自主代理+技能学习回路"，OpenClaw 更偏向"多渠道消息网关+个人助手平台"。事实上 Hermes 还内置了 `hermes claw migrate` 命令，可以一键从 OpenClaw 导入配置和记忆。

**核心差异化：**
- **学习回路**：不是"会调工具的聊天机器人"，是"会从经验中学习的 AI"
- **技能进化**：完成一次复杂任务 → 自动生成技能 → 下次直接调用技能，而非重新推理
- **用户建模**：用 Honcho 辩证模型跨会话构建用户画像，越用越理解你的思维模式
- **低到离谱的部署成本**：最低 $5 VPS 就能跑，空闲时休眠几乎零成本
- **模型自由**：不绑定任何模型提供商，Nous Portal 一站式中转 + OpenRouter 200+ 模型 + 任意自定义端点

| 维度 | 说明 |
|------|------|
| 出品方 | Nous Research（开源 AI 研究机构） |
| 定位 | 自我改进型 AI 代理（Self-improving Agent） |
| 核心技术栈 | Python 82.4% + TypeScript 13.6%（代理核心 Python，前端/网关 TS） |
| 许可证 | MIT |
| 交互方式 | 终端 TUI（主力） + 多平台消息网关（Telegram/Discord/Slack/WhatsApp/Signal/Email） |
| 部署方式 | 本地 / Docker / SSH / Singularity / Modal 无服务器 / Daytona 无服务器 |
| 模型接入 | Nous Portal / OpenRouter / NovitaAI / NVIDIA NIM / Moonshot / MiniMax / HuggingFace / OpenAI / 自有端点 |
| 技能生态 | agentskills.io 开放标准，内置技能 + 自动创建技能 + 社区共享 |

---

## 第一部分：入门教程系列

### 1.1 Hermes Agent 是什么？—— 一个会成长的 AI
- 一句话：不是"聊天的 AI"，是"会学习、会进化、会记住你的 AI"
- Nous Research 是谁：开源 AI 研究机构，做模型也做工具
- Agent 的"学习回路"到底是怎么回事：执行→反思→提取→持久化→复用
- 跟 Claude/OpenAI 直接聊天的根本区别：Hermes 在聊天之外会"做事"和"记住"
- 跟 OpenClaw 的对比与协作：HermesClaw 社区桥接让两者共用微信
- 跟 LangChain/AutoGPT 的根本区别：后者是框架让你写 Agent，前者是开箱即用的 Agent
- 适用人群：想拥有个人 AI 助手的普通人、自动化需求重的开发者、AI Agent 研究者

### 1.2 安装与首次启动：十分钟拥有你的第一个 Agent
- 安装方式速览：
  - Linux / macOS / WSL2 / Termux：`curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`
  - Windows 原生：`iex (irm https://hermes-agent.nousresearch.com/install.ps1)`
- 安装脚本自动处理什么：uv 包管理器、Python 3.11、Node.js、ripgrep、ffmpeg、Git（隔离型 MinGit）
- 启动后的第一条命令：`hermes` 进入交互式 TUI
- Nous Portal OAuth 一站式配置：`hermes setup --portal`，一个账号搞定模型/搜索/画图/TTS/浏览器
- 手动配置模型：`hermes model` 选择任何模型提供商
- 首次对话体验：感受一个有"记忆"的助手跟你聊天

### 1.3 终端 TUI 完全指南
- TUI 到底长什么样，跟普通终端聊天有什么不同
- 多行编辑：再也不用把 prompt 挤在一行了
- 斜杠命令自动补全：`/model`、`/new`、`/reset`、`/retry`、`/stop`
- 对话历史搜索：跨会话回溯你说过什么、AI 做过什么
- 中断与重定向：`Ctrl+C` 中断当前操作，随时介入
- 流式工具输出：实时看到 Agent 在调用什么工具、拿到什么结果
- TUI 里的工具配置：`hermes tools` 增减可用的工具能力

### 1.4 消息网关：把 Hermes 接入你的日常聊天
- 什么是 Gateway：一个统一进程管理所有消息平台
- 支持平台一览：Telegram、Discord、Slack、WhatsApp、Signal、Email
- 启动网关：`hermes gateway`
- Telegram 接入实战（最常用、最成熟）
- WhatsApp / Discord 接入实战
- CLI 和消息平台命令统一：`/model`、`/personality`、`/retry` 在两个入口都能用
- 语音转文字支持：发语音给 Hermes 它也能听懂
- 跨平台连续性：Telegram 上未完成的对话，换到 CLI 接着聊

---

## 第二部分：核心功能系列

### 2.1 学习回路：AI 的"肌肉记忆"
- 学习回路的完整流程演示：
  - 你让 Hermes 做一个复杂任务（比如：把一篇文章改成小红书风格并配图）
  - Hermes 完成任务后，自动将这个流程提炼为技能
  - 下次你直接说"用小红书风格发这篇文章"，一步到位
- 技能自动创建 vs 手动创建：什么时候 AI 会自动创建，什么需要你手动教
- 技能自改进：多次使用同一技能后，Hermes 会基于执行经验优化它
- agentskills.io 开放标准：你的技能可以分享给别人，也能用别人的技能
- 实战：教 Hermes 学会你的写作风格，生成「写作风格技能」

### 2.2 记忆系统：Hermes 如何"记住"你
- 三层记忆架构：
  - 会话级：当前对话上下文，跟普通聊天一样
  - 摘要级：FTS5 全文搜索 + LLM 摘要，跨会话的关键信息提取
  - 用户模型级：Honcho 辩证建模，构建你的偏好、习惯、思维模式画像
- 主动提示自己持久化：Hermes 会在对话中发现重要信息时主动说"这个值得记住"
- 看 Hermes 记住了什么：如何查看和管理记忆
- 不想让它记住的东西：如何控制记忆范围
- 实战：用一个月的时间观察 Hermes 如何逐渐理解你的工作习惯

### 2.3 技能系统（Skills）深度使用
- 技能是什么：可复用的任务模板，存放在 `skills/` 目录
- 内置技能有哪些：文件操作、网络请求、代码执行等 40+ 工具
- 自动创建技能：触发条件、生成过程、首次使用体验
- 手动编写技能：自定义技能的结构与规范
- agentskills.io 技能中心：浏览和安装社区共享技能
- 实战：创建「每日公众号选题简报」技能

### 2.4 定时任务（Cron）：让 Hermes 无人值守工作
- 内置 cron 调度器：不需要额外的定时任务工具
- 自然语言设置：说"每天早上 9 点给我发微信汇报今日日程"就行
- 发送到任意平台：日报推 Telegram、周报发邮件、提醒发 WhatsApp
- 常见定时任务场景：
  - 每日行业动态简报
  - 每周工作总结
  - 夜间数据备份检查
  - 周期性内容发布
- 实战：搭建一个「每日 AI 资讯早报」自动推送

---

## 第三部分：进阶实战系列

### 3.1 模型灵活切换与成本控制
- Hermes 的模型无关设计：换模型不需要改代码，`hermes model` 一键切
- Nous Portal 是什么：单一订阅覆盖模型/搜索/画图/TTS/云端浏览器
- 主流模型渠道对比：
  - Nous Portal：官方一站式，体验最好
  - OpenRouter：200+ 模型，按用量付费
  - NovitaAI / Moonshot / MiniMax：性价比之选
  - 自有端点：数据中心/本地模型接入
- 策略：重活用好模型、轻活切便宜模型、离线场景切本地模型
- 成本实测：一周重度使用的 API 费用到底多少
- 本地 llama.cpp 模型配合：Hermes 对话用云端，离线任务切本地

### 3.2 子代理与并行处理
- 子代理（Sub-agents）是什么：隔离子代理并行处理多个工作流
- 什么时候该用子代理：同时要查资料、写代码、画图，拆分并行
- 隔离子代理的安全边界：子代理的权限与数据隔离
- 通过 RPC 写 Python 脚本调用 Hermes 工具
- 多步流水线压缩为零上下文开销：用脚本编排复杂任务
- 实战：子代理分工完成「行业调研 + 文章撰写 + 配图设计」

### 3.3 部署方案大全：从本地到云端
- 六大终端后端详解：
  - **本地**：你的电脑直接跑，最直接
  - **Docker**：标准容器化，适合服务器
  - **SSH**：远程连接已有机器上的 Hermes
  - **Singularity**：HPC 集群环境
  - **Modal**：无服务器，空闲零成本，按需唤醒
  - **Daytona**：无服务器开发环境
- $5 VPS 实战：一台最廉价云服务器怎么跑 Hermes
- 空闲休眠策略：不用时几乎不花钱
- GPU 集群部署方案：给研究和大规模场景
- 如何根据需求选后端：个人日常 vs 团队共享 vs 大规模研究

### 3.4 MCP 集成与能力扩展
- MCP（Model Context Protocol）在 Hermes 中的角色
- 连接 MCP 服务器：数据库、API、文件系统、浏览器……
- 实战：接入数据库 MCP 服务器，让 Hermes 直接帮你查数据
- 实战：接入浏览器 MCP 服务器，让 Hermes 自动抓网页信息
- Hermes + OpenClaw 的协作模式（HermesClaw 社区桥接）
- 从 OpenClaw 迁移：`hermes claw migrate` 一键导入 SOUL.md / 记忆 / 技能 / API 密钥 / 消息平台配置

### 3.5 Hermes 的个性定制（SOUL.md / PERSONALITY.md）
- SOUL.md 是什么：给你的 Agent 注入"灵魂"
- 为不同场景定制不同人格：
  - 工作模式：专业、简洁、直接
  - 写作模式：有文采、有观点、有温度
  - 生活助手：亲切、幽默、轻松
- /personality 命令快速切换
- AGENTS.md 注入提示：给 Agent 项目级指令
- 实战：打造一个「公众号写作人格」和一个「代码审查人格」

### 3.6 研究向功能：轨迹生成与模型训练
- Hermes 的研究友好设计
- 批量轨迹生成：让 Hermes 自动执行一批任务，收集决策链数据
- 轨迹压缩：把完整对话压缩为训练数据
- 用于训练下一代工具调用模型
- 这对开发者和研究者的意义
- 实战：用 Hermes 生成一批"写作 Agent"训练数据

---

## 第四部分：踩坑与最佳实践

### 4.1 安装与配置常见问题
- Windows 下的 PowerShell 执行策略问题
- uv / Python 3.11 环境冲突解决方案
- Node.js 版本要求与 nvm 管理
- 首次启动连接失败：网络/代理/防火墙排查
- `hermes doctor` 诊断工具的完整使用
- Git（MinGit）隔离环境的注意事项

### 4.2 消息网关踩坑
- Telegram Bot 创建与 Token 配置
- WhatsApp 接入的技术门槛与替代方案
- Discord Bot 权限配置
- 消息收不到 / 发不出的排查清单
- 网关进程的后台保活：systemd / launchd 配置

### 4.3 学习回路调优
- 什么时候技能自动创建效果好、什么时候该手动干预
- 技能过多导致混乱：如何清理和管理技能库
- 记忆膨胀问题：FTS5 搜索效率和记忆清理
- 用户画像"学偏"：如何纠正 Hermes 对你的错误认知
- 最佳实践：定期审计记忆和技能库

### 4.4 安全与隐私
- 本地部署 vs 云端部署的安全差异
- API 密钥管理：环境变量 vs 配置文件
- 网关暴露到公网的安全注意事项
- Hermes 会记录什么、存在哪、谁能看
- 审计日志：查看 Hermes 做过的所有操作
- 敏感信息过滤：不要让它记住银行卡号

### 4.5 综合案例：用 Hermes 搭建个人 AI 工作助手
- 场景目标：一个能写文章、查资料、定时推送、跨平台通知的个人助手
- 第一步：安装 + Nous Portal 配置
- 第二步：教 Hermes 理解公众号写作需求（技能创建 + 记忆积累）
- 第三步：配置 Telegram 网关 + 每日定时推送
- 第四步：子代理分工 + MCP 集成
- 第五步：一个月的使用复盘：哪些自动化了、哪些仍需人工
- 长期维护：更新、记忆管理、技能迭代

---

## 附录

### A. 常用命令速查表
- `hermes`：启动交互式 CLI
- `hermes model`：选择/切换模型
- `hermes tools`：配置启用的工具
- `hermes gateway`：启动消息网关
- `hermes setup`：完整设置向导
- `hermes setup --portal`：通过 Nous Portal OAuth 一站式配置
- `hermes doctor`：故障诊断
- `hermes update`：更新到最新版
- `hermes claw migrate`：从 OpenClaw 迁移
- TUI 内常用斜杠命令：`/model`、`/personality`、`/new`、`/reset`、`/retry`、`/stop`

### B. 官方资源与社区索引
- GitHub：https://github.com/NousResearch/hermes-agent
- 官方文档：hermes-agent.nousresearch.com/docs
- Nous Portal：模型/搜索/画图/TTS 一站式服务
- agentskills.io：技能开放标准与共享中心
- Discord 社区
- 相关项目：HermesClaw（微信桥接）、computer-use-linux（桌面控制 MCP）

### C. 更新日志
- 跟随 Hermes Agent 版本更新持续同步（当前基准：v0.16.0）

---

*本大纲基于 NousResearch/hermes-agent 官方仓库（github.com/NousResearch/hermes-agent）信息与个人实践理解编写，内容为独立理解与表述。具体文章写作中如需引用官方原文或示例代码，将注明出处。大纲随 Hermes Agent 版本更新持续迭代。*

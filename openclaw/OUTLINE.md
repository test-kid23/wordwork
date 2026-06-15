# OpenClaw 系列创作大纲

> OpenClaw（🦞 小龙虾）—— 本地优先个人 AI 助手的体系化实战指南
>
> 源码：https://github.com/openclaw/openclaw | TypeScript monorepo | 379k+ Stars

---

## OpenClaw 到底是什么？

**一句话：** OpenClaw 是一个跑在你**自己设备上**的个人 AI 助手，通过你**已经在用的聊天工具**（微信/QQ/Telegram/WhatsApp/Slack/Discord 等 26+ 平台）来交互。它不只是聊天——能语音唤醒、渲染实时画布、管理多智能体、执行定时任务，像一个长住在你手机和电脑里的 AI 管家。

**中文圈昵称"小龙虾"**，因为它最初是为一只叫 Molty 的太空龙虾 AI 助手 🦞 而构建的。

| 维度 | 说明 |
|------|------|
| 定位 | 本地优先的个人 AI 助手（不是模型管理工具，不是 LLM 工具链） |
| 核心架构 | Gateway（网关/控制平面）→ Agent Workspace → Channels + Tools |
| 技术栈 | TypeScript 91.7%，pnpm monorepo，Node 24 |
| 多平台 | macOS / iOS / Android / Windows 均有原生伴侣应用 |
| 消息渠道 | 26+ 平台：微信、QQ、WhatsApp、Telegram、Signal、iMessage、Slack、Discord、飞书、LINE 等 |
| 安全模型 | DM 配对机制 + 沙箱隔离 + 细粒度权限 |
| 技能系统 | 内置技能 + ClawHub 注册中心 + 工作空间自定义技能 |

---

## 第一部分：入门教程系列

### 1.1 OpenClaw 是什么？—— 你的私人 AI 管家
- 本地优先 vs 云端 AI 的本质区别：数据主权在谁手里
- Gateway 控制平面 + 多渠道收件箱的架构直觉
- 跟 ChatGPT/Claude 聊天工具的根本不同：不绑定平台，你选模型
- 跟 Ollama/LM Studio 的根本不同：不是模型管理，是助手平台
- 小龙虾 🦞 的由来：从 Molty 到 OpenClaw 的故事

### 1.2 环境要求与安装引导
- Node 24 运行时安装（推荐）或 Node 22.19+
- `npm install -g openclaw@latest` 全局安装
- `openclaw onboard --install-daemon` 引导式配置
- Gateway 守护进程：launchd（macOS）/ systemd（Linux）后台运行
- 首次启动验证：`openclaw gateway status`

### 1.3 接入第一个消息渠道
- 渠道配置入口：`openclaw onboard` 或手动编辑
- 微信 / QQ 接入（国内用户首选）
- Telegram / WhatsApp 接入
- 理解 DM 配对机制：为什么陌生人的消息不会被处理
- 发送第一条消息测试

### 1.4 初体验：跟你的小龙虾对话
- WebChat 界面快速上手
- 基础聊天命令：`/status`、`/new`、`/reset`、`/think`
- Agent 工作空间：`~/.openclaw/workspace` 目录结构
- `AGENTS.md` / `SOUL.md` / `TOOLS.md` 注入提示文件
- 第一次让 AI 帮你做点实事

---

## 第二部分：核心功能系列

### 2.1 多渠道收件箱：让 AI 无处不在
- 26+ 消息平台统一收件箱的概念
- 即时通讯类：微信、QQ、WhatsApp、Telegram、Signal、iMessage、LINE、Zalo
- 团队协作类：Slack、Discord、飞书、Teams、Google Chat
- 去中心化类：Matrix、Nostr
- 渠道独立配置与白名单管理

### 2.2 多智能体路由：一个助手不够，来一群
- 什么是多智能体路由：渠道 → Agent 映射
- 为不同渠道/账户配置隔离的 Agent 工作空间
- 每个 Agent 独立会话、独立工作空间、独立权限
- 实战：工作群和私人消息分别路由到不同 Agent
- Agent 配置：模型选择、思考深度、工具权限

### 2.3 语音唤醒与对话模式
- macOS/iOS：唤醒词 + 按键通话
- Android：持续语音模式
- ElevenLabs TTS 集成 + 系统 TTS 回退
- 语音触发转发：iOS/Android 作为语音节点
- 实战：开车时说句话让 AI 帮你发消息

### 2.4 实时画布（Live Canvas）
- Canvas 是什么：Agent 驱动的可视化工作空间
- A2UI（AI-to-UI）渲染机制
- 让 AI 画图、做表格、生成交互界面
- iOS/Android 作为 Canvas 渲染面
- 实战：让 AI 画一个项目进度看板

---

## 第三部分：进阶实战系列

### 3.1 技能系统（Skills）与 ClawHub
- 三种技能类型：内置技能 / 托管技能 / 工作空间技能
- `~/.openclaw/workspace/skills/<skill>/SKILL.md` 结构
- ClawHub 技能注册中心：社区共享技能
- 实战：写一个「每日天气简报」自定义技能
- 实战：写一个「会议纪要自动整理」技能

### 3.2 工具与自动化（Tools & Automation）
- 一等公民工具：Browser、Canvas、Nodes、Cron
- Cron 定时任务：让 AI 每天定时做一件事
- Webhooks：外部事件触发 Agent 执行
- Gmail Pub/Sub：邮件到达自动处理
- 实战：每天早上 9 点自动汇总未读消息

### 3.3 安全模型深入：DM 配对与沙箱
- **核心原则**：入站 DM 不可信
- DM 配对机制（dmPolicy=pairing）：走通配对码的白名单流程
- `openclaw pairing approve <channel> <code>` 管理白名单
- `openclaw doctor` 安全诊断
- 沙箱模式：Docker / SSH / OpenShell 三种后端
- 非主会话隔离：`sandbox.mode: "non-main"` 保护群组场景
- 远程暴露前的安全检查清单

### 3.4 模型配置与故障切换
- 支持的模型提供商：OpenAI、Anthropic 及各兼容 API
- 模型配置：`agent.model: "<provider>/<model-id>"`
- 认证配置文件轮换 + 回退机制（Model failover）
- OAuth 订阅 vs API Key 两种接入方式
- 实战：主模型挂了自动切备用模型

---

## 第四部分：伴侣应用系列

### 4.1 macOS 菜单栏应用
- 菜单栏网关控制与健康监控
- 语音唤醒 + 按键通话覆盖
- WebChat + 调试工具
- 通过 SSH 控制远程网关
- 签名构建：让 macOS 权限在更新后保持

### 4.2 iOS 节点
- 通过 WebSocket 配对为网关节点
- 语音触发转发到网关
- Canvas 渲染面：手机屏幕变成 AI 画布
- `openclaw nodes` 节点管理命令

### 4.3 Android 节点
- Connect / Chat / Voice 三大标签页
- Canvas + Camera + Screen capture + Android 设备命令族
- 设备配对流程
- 作为持续语音节点

### 4.4 Windows Hub 桌面伴侣
- 设置向导 + 托盘状态
- 聊天界面 + 节点模式
- 本地 MCP 模式
- Windows 环境下从零搭建全流程

---

## 第五部分：运维与踩坑

### 5.1 Gateway 运维指南
- Gateway 守护进程管理：启动、停止、状态、重启
- 端口配置与远程访问（含 Tailscale 方案）
- 日志体系：`openclaw gateway --verbose` 调试
- 更新策略：stable / beta / dev 三通道切换

### 5.2 部署方案
- Docker 部署
- Fly.io 部署
- Render 部署
- 自建服务器部署注意事项

### 5.3 常见问题排查
- 渠道不通：消息收不到 / 发不出
- Gateway 启动失败
- 模型调用报错
- 配对码不生效
- Node 版本兼容性

### 5.4 安全加固实战
- DM 策略审计
- 沙箱规则定制
- 白名单管理最佳实践
- 远程访问安全配置
- 审计日志

---

## 第六部分：综合案例

### 6.1 案例：个人全平台 AI 管家
- 场景：一个 Agent 管理微信 + Telegram + 邮件 + 日历
- 渠道配置 + Agent 路由
- Cron 日报 + Webhook 通知
- 安全配置复盘

### 6.2 案例：小团队协作助手
- 场景：Discord/Slack 团队 AI 助手
- 主会话（管理员）+ 群组沙箱隔离
- 技能：代码审查、文档生成、会议纪要
- 多 Agent 分工

### 6.3 案例：从零定制自己的小龙虾
- 定制 SOUL.md：给 AI 一个"性格"
- 定制 TOOLS.md：精准控制 AI 的能力边界
- ClawHub 上发布一个共享技能
- 打造有个人风格的专属助手

---

## 附录

### A. 官方资源索引
- GitHub: https://github.com/openclaw/openclaw
- 官方文档导航：按目标分类（入门 / 渠道 / 应用 / 配置安全 / 远程 / 工具自动化 / 架构 / 排障）

### B. 关键概念速查表
- Gateway、Agent Workspace、Channel、Node、Skill、Canvas、Sandbox

### C. 更新日志

---

*本大纲跟随 OpenClaw 官方版本更新持续迭代。2026.6 基于 openclaw v2026.6.6 编写。*

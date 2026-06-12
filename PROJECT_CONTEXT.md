# wordwork · AI 系列文章写作项目

## 项目定位

多平台知识写作项目，目前覆盖：
- **微信公众号**：面向 **想学 AI 但不知道怎么学** 的人（深度长文）
- **小红书**：面向 **测试工程师 / QA**，分享 AI 辅助测试实战（轻阅读笔记）
- **公众号**：面向 **软件测试工程师**，分享测试技能与职业发展知识

## 目标受众

- 职场人
- 自由职业者
- 自媒体博主
- 小型创业者
- 技术从业者（含软件测试工程师）

## 核心差异化：入门 vs 进阶

| 层次 | 定位 |
|------|------|
| **入门** | 教"用 AI 工具"——单个工具怎么用、prompt 怎么写 |
| **进阶** | 教"把 AI 当成团队成员"——搭建分工明确、自动化流转、可长期迭代的协作体系 |

## 核心主旨

> 拒绝零散"玩 AI"，用体系化 AI 团队提升个人/组织竞争力，避免被 AI 浪潮淘汰。

融入深度内容：
- 多模型协同
- AI Agent 工作流
- 私有知识库（RAG）
- 本地部署大模型
- 流程风控
- Skills 机制 · MCP 协议 · Automation 自动化

## 目录结构

```
wordwork/
├── PROJECT_CONTEXT.md          # 本文件
├── ai_learning/                # AI 学习系列（入门向）
│   ├── ai-beginner-guide.md           # AI 入门指南
│   ├── advanced-ai-team-building-guide.md  # 进阶：AI 团队搭建
│   ├── llama_cpp_deploy_guide.md       # llama.cpp 部署指南
│   └── local-llm-gpu-guide.md          # 本地大模型 GPU 部署指南
├── ai_road/                    # AI 进阶之路系列（深度版，7 章）
│   ├── chapter-01-cognitive-upgrade.md   # 认知升级
│   ├── chapter-02-core-principles.md     # 核心原则
│   ├── chapter-03-team-architectures.md  # 团队架构
│   ├── chapter-04-workflow-engine.md     # 工作流引擎
│   ├── chapter-05-advanced-ops.md        # 进阶运维
│   ├── chapter-06-pitfalls.md            # 踩坑实录
│   ├── chapter-07-summary-action.md      # 总结与行动
│   └── bak-chapter-03-role-definition.md # 旧版：角色定义（备份）
├── ai_road_wx/                 # AI 进阶之路（微信公众号适配版，6 篇）
│   ├── wx-01-pitfalls.md        # 踩坑篇
│   ├── wx-02-main.md            # 正文核心
│   ├── wx-03-studio.md          # AI Studio
│   ├── wx-04-local-dev.md       # 本地开发
│   ├── wx-05-ops.md             # 运维篇
│   └── wx-06-action.md          # 行动篇
├── codebuddy/                  # CodeBuddy 深度使用系列
│   └── 1.1~1.5 已写 5 篇（含 .md 与 -wx.html）
├── rag/                        # RAG 私有知识库系列
│   └── 1.1~1.4 已写 4 篇（含 .md 与 -wx.html）
├── claude_code/                # Claude Code 工作流系列
│   ├── OUTLINE.md
│   └── claude_write_case01.md  # 首篇
├── personal_skill/             # 个人技术备忘（性能测试工具等）
│   ├── cosbench.md
│   └── vdbench.md
├── testengineer/               # 软件测试工程师技能与职业发展系列（新建）
├── ai_test_xhs/                # AI + 测试 小红书系列（轻阅读向）
│   ├── README.md               # 系列说明与选题规划
│   ├── OUTLINE.md
│   ├── rednote_account_plan.md # 账号规划
│   ├── xhs-01~03 已写 3 篇
│   └── xhs-04~13 规划 10 篇
├── hermes/                     # Hermes 智能 Agent 框架系列（待创作）
├── openclaw/                   # OpenClaw 开源 LLM 工具链系列（待创作）
├── openhuman/                  # OpenHuman AI 赋能个体能力系列（待创作）
└── llamacpp/                   # llama.cpp 本地部署大模型系列（待创作）
```

## 各系列创作进度（跟随 AI 浪潮持续更新）

| 目录 | 系列主题 | 状态 |
|------|---------|------|
| `ai_learning/` | AI 学习系列（入门向） | ✅ 已完成 4 篇 |
| `ai_road/` | AI 进阶之路（深度版） | ✅ 已完成 7 章 |
| `ai_road_wx/` | AI 进阶之路（公众号适配版） | ✅ 已完成 6 篇 |
| `codebuddy/` | CodeBuddy 深度使用与能力挖掘 | 🔥 连载中，已写 5 篇 |
| `rag/` | RAG 私有知识库搭建 | 🔥 连载中，已写 4 篇 |
| `claude_code/` | Claude Code 深度使用与工作流 | 🔥 连载中，已写 1 篇 |
| `ai_test_xhs/` | AI + 测试 小红书系列 | 🔥 连载中，已写 3 篇 |
| `testengineer/` | 软件测试工程师技能与职业发展 | 📁 目录已建，待创作 |
| `personal_skill/` | 个人技术备忘 | 📝 积累中（2 篇） |
| `hermes/` | Hermes 智能 Agent 框架 | 📁 目录已建，待创作 |
| `openclaw/` | OpenClaw 开源 LLM 工具链 | 📁 目录已建，待创作 |
| `openhuman/` | OpenHuman AI 赋能个体能力 | 📁 目录已建，待创作 |
| `llamacpp/` | llama.cpp 本地部署大模型 | 📁 目录已建，待创作 |

## 排版规范

| 平台 | 规范文件 | 说明 |
|------|---------|------|
| 微信公众号 | `wx_format_guide.md` | HTML → 微信编辑器，全内联样式，蓝紫配色 |
| 小红书 | `xhs_format_guide.md` | 纯文本 + emoji 排版，口语化短句，卡片式结构 |

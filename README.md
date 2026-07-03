# wordwork · AI 系列文章写作项目

> 多平台知识写作工程，三条内容线并行推进：
> - **AI 协作体系**（公众号）：面向想学 AI 但不知道怎么学的人，从入门工具到搭建 AI 团队
> - **AI 测试技术**（CSDN + 小红书）：面向软件测试工程师，从 API/Web/移动端自动化到 AI 测试平台开发
> - **一人公司探索**（公众号）：面向想用 AI 一个人干一个团队的事的创业/自由职业者
>
> 现在是2026年6月，不要引用太旧的知识和内容，保持文章实时性，真实性
---

## 项目定位

这不是一个"教你玩 AI 工具"的账号，也不是一个纯技术博客——而是**横跨 AI 应用、测试工程、一人商业三条线的体系化内容工程**。

| 内容线 | 受众 | 平台 | 深度 |
|--------|------|------|------|
| **AI 协作体系** | 职场人、自由职业者 | 微信公众号 | 入门→进阶，建体系 |
| **AI 测试技术** | 软件测试工程师 | CSDN 深度长文 + 小红书轻笔记 | 保姆级教程 + 平台架构 |
| **一人公司** | 创业者、超级个体 | 微信公众号 | 认知→工具→实战→反思 |

### 核心主旨

> 不追热点，建体系。用 AI 提升个人竞争力，拒绝零散"玩 AI"，把 AI 当成可长期迭代的协作团队。

---

## 目标受众

职场人 · 自由职业者 · 自媒体博主 · 小型创业者 · 技术从业者 · 软件测试工程师

---

## 目录结构

```
wordwork/
├── README.md                    # 本文件
├── PROJECT_CONTEXT.md           # 项目上下文（供 AI 辅助创作使用）
│
├── ai_road_wx/                  # AI 进阶之路主目录
│   ├── ai_beginner_wx/          #  AI 小白入门系列（公众号）✅ 6 篇
│   ├── ai_learning/             #  AI 学习系列（入门向）✅ 4 篇
│   ├── ai_road/                 #  AI 进阶之路（深度版）✅ 7 章
│   ├── image/                   #  配图资源
│   └── Published/               #  已发布内容存档
│
├── ai_test_csdn/                # AI 测试技术分享（CSDN 深度长文）🔥 连载中 3+ 篇
│   ├── selenium_webui/          #  Selenium WebUI 自动化保姆级教程 🆕 6 篇
│   └── appium_mobile/           #  Appium App 自动化保姆级教程 🆕 6 篇
│
├── ai_test_xhs/                 # AI + 测试 小红书系列 🔥 连载中 3 篇
├── codebuddy/                   # CodeBuddy 深度使用系列 🔥 连载中 5 篇
├── rag/                         # RAG 私有知识库系列 🔥 连载中 4 篇
├── claude_code/                 # Claude Code 工作流系列 🔥 连载中 1 篇
├── scene_ocp/                   # 一人公司 OCP 系列 📝 知识库已建，待创作
├── comfyui/                     # ComfyUI 节点化 AI 视觉生成系列（待创作）🎨
├── testengineer/                # 软件测试工程师技能与职业发展 📁 目录已建
├── personal_skill/              # 个人技术备忘（2 篇）
│
├── hermes/                      # Hermes 智能 Agent 框架系列（待创作）
├── openclaw/                    # OpenClaw 本地优先个人 AI 助手系列（待创作）🦞
├── openhuman/                   # OpenHuman AI 赋能个体系列（待创作）
└── llamacpp/                    # llama.cpp 本地部署大模型系列（待创作）
```

---

## 系列总览

### 已完成系列

| 系列 | 目录 | 篇数 | 说明 |
|------|------|------|------|
| 小白入门（公众号） | `ai_road_wx/ai_beginner_wx/` | 6 篇 | 面向零基础，从概念到「下一步」 |
| AI 学习（入门向） | `ai_road_wx/ai_learning/` | 4 篇 | 从基础到本地部署 |
| 进阶之路（深度版） | `ai_road_wx/ai_road/` | 7 章 | 体系化 AI 协作方法论 |
| 进阶之路（公众号版） | `ai_road_wx/Published/` | 6 篇 | 面向公众号读者的精编版 |

### 连载中系列

| 系列 | 目录 | 进度 | 核心主题 |
|------|------|------|---------|
| AI 测试（CSDN） | `ai_test_csdn/` | 3 篇正刊 + 12 篇子系列 | API/Web/平台三条主线 + Selenium & Appium 保姆级教程 |
| ├ Selenium WebUI | `ai_test_csdn/selenium_webui/` | 6/12 篇 | 从零到工程化，Selenium 全集 |
| ├ Appium 移动端 | `ai_test_csdn/appium_mobile/` | 6/12 篇 | Appium 3 从环境到进阶 |
| AI + 测试（小红书） | `ai_test_xhs/` | 3/13 篇 | AI 辅助软件测试实战 |
| CodeBuddy | `codebuddy/` | 5/19 篇 | CodeBuddy 深度使用与工作流构建 |
| RAG | `rag/` | 4/19 篇 | 私有知识库从原理到企业级平台 |
| Claude Code | `claude_code/` | 1/17 篇 | Claude Code 从入门到项目级应用 |
| 一人公司 OCP | `scene_ocp/` | 知识库 4 篇已建 / 正文 0/7 | AI 时代一人公司的认知、工具、实战与反思 |

### 规划中系列

| 系列 | 目录 | 规划篇数 | 核心主题 |
|------|------|---------|---------|
| 测试工程师 | `testengineer/` | 待定 | 软件测试技能与职业发展 |
| ComfyUI | `comfyui/` | 待定 | 节点化 AI 视觉生成工作流 🎨 |
| Hermes | `hermes/` | 16 篇 | 智能 Agent 框架入门→生产部署 |
| OpenClaw | `openclaw/` | 待定 | 本地优先个人 AI 助手全流程实战 🦞 |
| OpenHuman | `openhuman/` | 17 篇 | AI 赋能个人效率与能力提升 |
| llama.cpp | `llamacpp/` | 19 篇 | 本地大模型部署从编译到工作站 |

---

## 内容深度关键词

多模型协同 · AI Agent 工作流 · 私有知识库（RAG） · 本地部署大模型 · 流程风控 · Skills 机制 · MCP 协议 · Automation 自动化 · 向量数据库 · GGUF 量化 · 软件测试 · 职业发展 · 一人公司 · AI 自动化测试 · API/Web/移动端测试 · Playwright · Selenium · Appium · pytest · ComfyUI

---

## 创作原则

1. **不追热点，建体系** — 每篇文章服务于整体知识框架
2. **可操作，不空谈** — 每一步读者都能跟着做
3. **有场景，接地气** — 从职场人、自由职业者、测试工程师的真实需求出发
4. **持续迭代** — 跟随 AI 浪潮更新内容，大纲不是死的

---

## 使用方式

本项目配合 AI 辅助创作（CodeBuddy / Claude Code），在 `PROJECT_CONTEXT.md` 中维护项目上下文，让 AI 理解创作风格和内容定位。

```bash
# 克隆项目
git clone <repo-url>
cd wordwork

# 开始创作
# 用 CodeBuddy 打开项目，加载对应 Skills，开始写作
```

---

## License

MIT

---

*📝 跟随 AI 浪潮，持续更新中。*

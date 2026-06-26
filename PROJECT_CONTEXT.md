# wordwork · AI 系列文章写作项目

## 项目定位
现在是2026年6月，不要引用太旧的知识和内容，保持文章实时性，真实性
多平台知识写作项目，目前覆盖：
- **微信公众号**：面向 **想学 AI 但不知道怎么学** 的人（深度长文）
- **小红书**：面向 **测试工程师 / QA**，分享 AI 辅助测试实战（轻阅读笔记）
- **公众号**：面向 **软件测试工程师**，分享测试技能与职业发展知识
- **一人公司 OPC**：面向 **想用 AI 一个人干一个团队的事** 的创业/自由职业者

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
├── ai_beginner_wx/             # AI 小白入门系列（微信公众号）✅ 6篇完成
│   ├── PLAN.md                         # 系列选题规划
│   ├── README.md                       # 使用说明
│   ├── wx-beginner-00-concepts.html    # 第0篇：大模型基础概念介绍
│   ├── wx-beginner-01-scenarios.html   # 第1篇：5个打工人必备AI场景
│   ├── wx-beginner-02-prompt.html      # 第2篇：普通人Prompt炼金术
│   ├── wx-beginner-03-tools.html       # 第3篇：这些AI工具全是免费的
│   ├── wx-beginner-04-mindset.html     # 第4篇：AI时代不被替代的能力
│   └── wx-beginner-05-nextstep.html    # 第5篇：用熟了Kimi和豆包，然后呢？
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
├── hermes/                     # Hermes Agent 自我进化 AI 代理系列（待创作）
├── openclaw/                   # OpenClaw 本地优先个人 AI 助手系列（待创作）🦞
├── openhuman/                  # OpenHuman 个人 AI 超级智能系列（待创作）
├── llamacpp/                   # llama.cpp 本地部署大模型系列（待创作）
├── scene_ocp/                  # 一人公司 OPC 系列（新建）🏢
│   ├── README.md               # 系列概览
│   ├── PLAN.md                 # 详细选题规划（7 篇）
│   ├── ocp-knowledge-01-trend-data.md  # 知识库：趋势与数据
│   ├── ocp-knowledge-02-cases.md       # 知识库：案例拆解
│   ├── ocp-knowledge-03-tools.md       # 知识库：AI 工具链
│   └── ocp-knowledge-04-painpoints.md  # 知识库：陷阱与痛点
└── comfyui/                    # ComfyUI 节点化 AI 视觉生成系列（待创作）🎨
```

## 各系列创作进度（跟随 AI 浪潮持续更新）

| 目录 | 系列主题 | 状态 |
|------|---------|------|
| `ai_beginner_wx/` | AI 小白入门系列（公众号）| ✅ 已完成 6/6 篇 |
| `ai_learning/` | AI 学习系列（入门向） | ✅ 已完成 4 篇 |
| `ai_road/` | AI 进阶之路（深度版） | ✅ 已完成 7 章 |
| `ai_road_wx/` | AI 进阶之路（公众号适配版） | ✅ 已完成 6 篇 |
| `codebuddy/` | CodeBuddy 深度使用与能力挖掘 | 🔥 连载中，已写 5 篇 |
| `rag/` | RAG 私有知识库搭建 | 🔥 连载中，已写 4 篇 |
| `claude_code/` | Claude Code 深度使用与工作流 | 🔥 连载中，已写 1 篇 |
| `ai_test_xhs/` | AI + 测试 小红书系列 | 🔥 连载中，已写 3 篇 |
| `scene_ocp/` | 一人公司 OPC 系列 | 📝 知识库已建，规划 7 篇待创作 |
| `testengineer/` | 软件测试工程师技能与职业发展 | 📁 目录已建，待创作 |
| `personal_skill/` | 个人技术备忘 | 📝 积累中（2 篇） |
| `hermes/` | Hermes Agent 自我进化 AI 代理 | 📁 目录已建，待创作 |
| `openclaw/` | OpenClaw 本地优先个人 AI 助手 🦞 | 📁 目录已建，待创作 |
| `openhuman/` | OpenHuman 个人 AI 超级智能 | 📁 目录已建，待创作 |
| `llamacpp/` | llama.cpp 本地部署大模型 | 📁 目录已建，待创作 |
| `comfyui/` | ComfyUI 节点化 AI 视觉生成 🎨 | 📁 目录已建，待创作 |

## 排版规范

| 平台 | 规范文件 | 说明 |
|------|---------|------|
| 微信公众号 | `wx_format_guide.md` | HTML → 微信编辑器，全内联样式，蓝紫配色 |
| 小红书 | `xhs_format_guide.md` | 纯文本 + emoji 排版，口语化短句，卡片式结构 |

## 微信公众号运营笔记（2026.06 补充）

### 标题公式

微信阅读的本质：读者在刷订阅号列表，你的标题只有 **0.5 秒** 的机会。

**黄金三角公式：**

```
[具体数字] + [痛苦场景] + [反常识结论]
```

**三大常见问题：**
- ❌ 用「我想写什么」起标题，而不是「读者想看到什么」
- ❌ 标题太像教程目录，没有制造「认知缺口」
- ❌ 技术名词孤零零当标题（如 `MCP 协议：xxx`）——不是不能用名词，是要搭配场景钩子，让不搜这个词的人也想点

**好标题 vs 差标题：**

| ❌ 差标题 | ✅ 好标题 |
|----------|----------|
| 别再零散用 AI 了——手把手教你搭一支自己的"AI 团队" | 我一个人管 5 个 AI 干活，效率翻了 3 倍（附完整搭建方案） |
| AI 团队搭好了，但怎么知道它在退步？——长期运维指南 | AI 用了 3 个月突然变笨了？不是你幻觉，是它在退化 |
| 免费 AI 实战：搞定 5 类高频工作，效率翻倍 | 每天被周报、PPT、会议纪要折磨？5 个免费 AI 一键搞定 |
| AI 代码工具入门：一行代码不会写，也能做小工具、改脚本、搭网站 | 不会写代码的人，已经开始用 AI 做网站赚钱了 |

### 封面图 > 标题

微信是**先看到封面，再看到标题**的：
- 用真人或真实场景（办公桌、屏幕截图、手机界面），不要通用 AI 机器人图
- 封面图上加 1-2 个醒目大字（如「3倍效率」「0元免费」）
- 配色往黄/橙色走，订阅号列表里最跳

### 开头 100 字决定跳出率

- 删掉所有铺垫和客套话（「AI 时代来了」「最近很多朋友问我」）
- **第一句话直接戳痛点**
- 示例：
  > ❌ "随着大模型技术的飞速发展，越来越多的职场人开始使用AI工具..."
  > ✅ "你上周写的周报，AI 写得比你好。但你用了 3 个月，发现自己反而更累了——这不对劲。"

### 冷启动传播 checklist

新号阅读量低不一定是内容问题，可能缺传播：
- [ ] 发朋友圈不要只甩链接，配 100 字「痛点自述」文案
- [ ] 找 3-5 个朋友帮忙转发（第一批种子传播极关键）
- [ ] 在相关社群/即刻/知乎发干货内容引流（不硬甩链接，用干货带钩子）
- [ ] 用好公众号「合集」功能，微信会推合集
- [ ] 固定发布时间：每周二/四 8:00 或 21:00（通勤/睡前高峰）
- [ ] 新号不要日更，一周 1-2 篇，留时间做传播
- [ ] 新号文章控制在 1500-2500 字，不要上来就 3000-5000 字

### 系列化标题规范

同一系列文章，标题遵循统一格式增强辨识度：
- 总字数控制在 **15-25 字**
- 优先使用 `[场景钩子/痛点] + [技术名词（可选）]` 公式
- 技术名词可以作为搜索锚点，但必须搭配场景钩子，不要名词单独做标题

### 内容漏斗策略（2026.06 新增）

基于微信搜一搜数据分析，"AI怎么用"是第二大搜索词，"AI零基础入门指南"是点击最高的文章。大量小白用户涌入，但现有内容在入门之后直接跳到了技术深度，存在明显断层。

**漏斗模型：**

```
流量层：小白入门系列（ai_beginner_wx/）
  ↓ 文末挂进阶文章链接
粘性层：工具深度系列（codebuddy/、rag/、claude_code/）
  ↓ 文末挂体系化内容链接
壁垒层：进阶之路系列（ai_road/、ai_road_wx/）
  ↓ 文末挂技术深度内容链接
深度层：技术系列（hermes/、openclaw/、llamacpp/）
```

**关键原则**：流量在入门，粘性在深度。用入门内容扩大受众基数，用专业内容筛选和留住核心用户。

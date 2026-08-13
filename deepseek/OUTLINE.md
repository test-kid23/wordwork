# DeepSeek V4 + Harness 系列创作大纲

> DeepSeek V4 Pro 0813 正式版 + DeepSeek Harness 深度实战系列
>
> 📅 建立：2026 年 8 月 13 日（V4 Pro 正式版发布当日 / Harness 开源当日）
>
> 🎯 目标受众：职场人、开发者、AI Agent 实践者、想用 DeepSeek 搭建自动化工作流的人

---

## 🆕 2026年8月13日 系列建立背景

> 一天之内两件大事，这个系列应运而生：

| 事件 | 时间 | 一句话说明 |
|------|------|-----------|
| **DeepSeek-V4-Pro-0813 正式版发布** | 8月13日凌晨无预告上线 | V4 系列旗舰模型首个正式版，Agent 能力全面跃升，双协议 API 兼容 |
| **DeepSeek Harness（DSH）开源** | 8月13日晚发布开发者预览版 | DeepSeek 首款 Agent 执行框架，属于 DeepSeek 自己的"Vibe Coding 入口" |

**系列定位**：不是"DeepSeek 新闻播报"，而是抓住这两个节点，带读者**学会用 DeepSeek 建自己的 Agent 工作流**——V4 Pro 负责"更强的模型"，Harness 负责"让模型真正开始干活"。

---

## 核心背景速览（写作时随时查阅）

### DeepSeek-V4-Pro-0813 关键规格

| 项目 | 参数 |
|------|------|
| 总参数量 | 1.6T（MoE 架构，激活约 49B/token） |
| 上下文窗口 | 1M token |
| 最大输出 | 384K token |
| 注意力架构 | CSA（压缩稀疏注意力）+ HCA（高度压缩注意力） |
| 推理模式 | `"none"`（非思考）/ `"high"` / `"max"`，通过 `reasoning_effort` 控制 |

### Agent 基准（vs 4月预览版）

| 测试集 | 预览版 | 0813 正式版 | 涨幅 |
|--------|--------|-------------|------|
| DeepSWE（软件工程 Agent） | 12.8 | **62.7** | +390% |
| NL2Repo（自然语言生成仓库） | 38.5 | **61.5** | +60% |
| DSBench-Hard（全栈高难编码） | ~33 | **67.2** | 约翻倍 |
| Terminal Bench 2.1 | — | **87.9** | — |
| Toolathlon-Verified | — | **74.1** | — |
| DSBench-FullStack | — | **71.1** | — |

### 第三方 BenchLM 数据（V4 Pro High 模式）

| 类别 | 测试集 | 分数 |
|------|--------|------|
| 编程 | SWE-bench Verified | 79.4% |
| 编程 | LiveCodeBench COT | 89.8% |
| 编程 | Codeforces Rating | 2919 |
| 推理 | GPQA Diamond | 89.1% |
| 长上下文 | MRCR 1M token | 83.3% |
| 智能体 | BrowseComp | 80.4% |
| 数学 | HMMT Feb 2026 | 94.0% |

### API 能力（重点写作素材）

- **新增双协议**：
  1. OpenAI Responses API：`base_url="https://api.deepseek.com/v1"`，`client.responses.create()`
  2. Anthropic API 协议：`base_url="https://api.deepseek.com"`，**可直接兼容 Claude Code**
- 标准 OpenAI Chat Completions 不变，`model` 填 `deepseek-v4-pro` 自动指向最新版
- **迁移红利**：现有 Claude Code、Codex 工作流只需切换 base_url + api_key 即可零改动接入测试
- ⚠️ 迁移注意：thinking 模式与 Claude extended thinking 实现不同，streaming 的 `reasoning_content` 字段格式有差异

### 价格（⚠️ 已公布新价，2026-08-17 00:00 生效，峰谷定价）

**旧价（截至 8 月 17 日 00:00 前）：**

| 计费类型 | V4-Flash | V4-Pro |
|----------|----------|--------|
| 输入（缓存未命中） | ¥1/M | ¥3/M |
| 输入（缓存命中） | ¥0.008/M | ¥0.025/M |
| 输出 | ¥2/M | ¥6/M |
| 并发限制 | 2500 | 500 |

**新价（8 月 17 日 00:00 起生效）：**

| 计费类型 | V4-Flash 空闲 | V4-Flash 高峰 | V4-Pro 空闲 | V4-Pro 高峰 |
|----------|---------------|---------------|-------------|-------------|
| 输入（缓存命中） | ¥0.05/M | ¥0.10/M | ¥0.15/M | ¥0.30/M |
| 输入（缓存未命中） | ¥1.5/M | ¥3/M | ¥4.5/M | ¥9/M |
| 输出 | ¥4.5/M | ¥9/M | ¥13.5/M | ¥27/M |

> **峰谷规则**：高峰时段为北京时间 9:00-12:00、14:00-18:00（其余为空闲时段）；空闲时段价格为高峰时段的一半。新价于 **2026 年 8 月 17 日 00:00** 生效。
>
> 官方原话（涨价预告）：**"We plan to raise the overall pricing for DeepSeek API services in the near future, with a significant increase expected."**——文章写作时务必带上新价表和峰谷规则，这是读者最关心的现实问题。
>
> ⚠️ **写作提醒：任何涉及价格的文章必须区分"旧价/新价"，并注明生效日期，避免误导读者。**

### DeepSeek Harness（DSH）关键信息

- **定位**：Agent 运行框架（Agent Harness），不是新模型、不是 API 客户端——把模型接入文件系统、终端、网页、代码工具和其他 Agent，组织上下文、工具调用和任务执行
- **开源地址**：https://github.com/deepseek-ai/deepseek-harness
- **npm 包**：`@deepseek-ai/dsh`，Web UI 启动命令：`npx @deepseek-ai/dsh web`
- **状态**：Developer Preview，官方提示后续快速迭代可能出现破坏兼容性的修改
- **核心设计理念**：Everything is a plugin（一切皆插件），建立在 **Cordis** 之上；模型适配器、工具注册、Session Log、甚至 Agent Loop 本身都是可替换插件
- **核心能力**：
  - 本地 Agent 工作台（读项目结构、定位代码、改文件、跑终端命令、根据报错继续修）
  - 多 Agent 编排（主 Agent 拆分子 Agent，各司其职后汇总）
  - 长任务协作（计划、目标、待办、后台任务机制）
  - 上下文管理（压缩、工具调用组织、错误重试、任务拆分）
  - 可观测性（Session Log 可从日志完整重建模型看到的内容，便于回放、调试、审计）
- **多种使用形态**：Web UI / TUI / Headless（脚本和 CI）/ ACP / JSON-RPC / Python SDK
- **Agent Preset（预设）**：标准、PTC、极简、创造等
- **与 V4 Pro 的关系**：V4 Pro 负责"更强的模型能力"，Harness 负责"让模型真正开始工作"，两者构成完整组合

---

## 第一部分：入门认知系列

### 1.1 深夜突袭：DeepSeek V4 Pro 正式版到底改了什么？ ✅ 已完成
- 2026-08-13 成文：`1.1-deepseek-v4-pro-0813.md` + `-wx.html`
- 角度：发布过程还原（深夜静默升级、公告撤回插曲）→ 架构没变纯后训练 → Agent 能力暴涨 390% 的真相 → 双协议 API → 新价公布（峰谷定价，8-17 生效）→ 行动三步
- 全文避免"你"称呼，用"我/我们/大家"视角
- 发布过程还原：8月12日晚无预告更新 → 官网"模型 & 价格"页切换为 0813 → 次日公告（曾被短暂撤回的插曲，可提）
- V4 Pro 预览版（4月24日）→ 正式版（0813）的进化逻辑：架构与参数量没变，全靠**针对性后训练**
- 核心规格大白话：1.6T 参数是什么概念？1M 上下文能装下什么？384K 输出能干什么？
- Agent 能力暴涨的真相：DeepSWE 12.8 → 62.7 意味着什么（+390% 背后的故事）
- 一句话总结：为什么说这是"Agent 时代的版本"而不是"又一个更强的模型"

### 1.2 双协议 API：DeepSeek 终于能"无缝接替" Claude Code 了 ✅ 已完成
- 2026-08-13 成文：`1.2-dual-protocol-api-claude-code.md` + `-wx.html`
- 角度：三种 API 形态对比 → 两行环境变量切换实操 → 三个差异（thinking/reasoning_content 字段、reasoning_effort 三档、工具调用边界）→ 迁移测试清单 → 成本账（缓存命中价趋近于零）→ 不建议切的场景
- 全文避免"你"称呼，用"我/我们/大家"视角
- 三种 API 形态对比：Chat Completions / OpenAI Responses / Anthropic 协议
- Anthropic 协议兼容的含金量：Claude Code、Codex 工作流改两行配置即可接入
- 实操演示：切换 base_url + api_key，让现有 Claude Code 用上 deepseek-v4-pro
- reasoning_effort 三档（none/high/max）怎么选，和 Claude extended thinking 的差异
- ⚠️ 迁移前必读：reasoning_content 流式字段差异、工具调用兼容性测试清单

### 1.3 DeepSeek Harness 开源：它终于有了自己的"Vibe Coding 入口" ✅ 已完成
- 2026-08-13 成文：`1.3-deepseek-harness.md` + `-wx.html`
- 角度：大脑 vs 身体 → Everything is a plugin → 5 分钟上手（npx @deepseek-ai/dsh web）→ 六种使用形态 → 与 Claude Code 的定位差异 → 多 Agent 编排 + Session Log → Developer Preview 风险提醒 → V4 Pro + 双协议 + Harness 组合拳
- 全文避免"你"称呼，用"我/我们/大家"视角
- Harness 是什么 / 不是什么（不是模型、不是 API 客户端，是 Agent 执行框架）
- 用大白话讲 Agent Harness 的概念：模型是"大脑"，Harness 是"身体"
- 5 分钟上手：Node.js + `npx @deepseek-ai/dsh web` 跑起来
- 四种形态速览：Web UI / TUI / Headless / SDK
- "一切皆插件"到底什么意思：Agent Loop 本身都能换
- 与 Claude Code / Codex 的定位差异：可组合的本地 Agent 工作台 vs 封装好的产品

### 1.4 选型指南：V4-Pro、V4-Flash、Harness 怎么组合最划算 ✅ 已完成
- 2026-08-13 成文：`1.4-selection-guide-pro-flash-harness.md` + `-wx.html`
- 角度：三件套定位（高级技工/流水线工人/包工头）→ 价格账（缓存命中=地板价）→ 方案A个人写作 / 方案B团队研发 / 方案C高并发批量 → 决策口诀 + 三条铁律 → 第一部分完结小结
- 全文避免"你"称呼，用"我/我们/大家"视角
- 此篇为第一部分（入门认知）完结篇
- 三件套定位：Pro 干重活 / Flash 跑量 / Harness 当躯干
- 并发与价格对比：500 vs 2500 并发，¥3 vs ¥1 输入，什么场景选哪个
- 官方预告涨价的应对策略：现在锁定用量的真实账本
- 组合方案示例：
  - 方案 A：个人写作自动化（Flash + Headless）
  - 方案 B：团队研发助手（Pro + Harness Web UI）
  - 方案 C：高并发批处理（Flash 多 Key 分流）
- 一句话决策口诀

---

## 第二部分：实战场景系列

### 2.1 用 DeepSeek 重写我的内容创作流水线
- 场景：公众号文章从选题到排版发布的自动化
- V4 Pro 在写作中的真实表现：长文结构、语言风格、自我审查
- 1M 上下文带来的变化：把整本书/整年文章库丢进去当素材
- 与现有工作流对比：之前用 XX，现在用 DeepSeek，差距在哪
- 成本核算：写一篇文章实际花多少钱

### 2.2 用 Harness 搭一个"自动改 Bug"的本地 Agent
- 场景还原：给一个项目，让它自己找 Bug、改代码、跑测试、循环修复
- 实操：注册 read_file / write_file / run_command 工具
- 多 Agent 编排：搜索 Agent + 修改 Agent + 测试 Agent 分工
- max_iterations 与 retry_on_failure 参数实战
- 成果展示与翻车记录：它修好了什么，又搞砸了什么

### 2.3 把 Claude Code 工作流整体迁移到 DeepSeek
- 迁移前检查清单：用了哪些 Claude 专属能力（extended thinking、hook 等）
- 分步迁移：改配置 → 跑通一个 demo → 逐步替换重活
- 实测对比：同一任务在 Claude Code / DeepSeek + Claude Code 上的差异
- 迁移后的成本账：API 费用对比
- 哪些场景建议保留 Claude、哪些放心迁过来

### 2.4 Harness 多 Agent 协作：让 AI 团队真正分工干活
- 主 Agent + 子 Agent 的工作流设计
- 计划 / 目标 / 待办 / 后台任务四种长任务机制
- 实战：一个"调研 + 写报告 + 校对"的三人小组
- Session Log 回放：出了问题怎么复盘 AI 的每一步

### 2.5 DeepSeek + MCP：接入真实世界的工具生态
- MCP 概念回顾（面向不了解的读者）
- Harness 作为 MCP 客户端：注册 MCP 服务器、自动发现工具
- 实战：接入数据库查询、网页抓取、文件系统 MCP
- 与之前 Claude Code MCP 用法的异同

---

## 第三部分：进阶技巧系列

### 3.1 1M 上下文实战：长文档处理的正确姿势
- 1M token 到底能塞什么：整本技术书、整个代码仓库、一年聊天记录
- 长上下文不是"无脑全塞"：什么时候该用 MRCR 这类长文检索
- 上下文压缩与分段策略
- 实测：1M 上下文下的准确率衰减曲线（MRCR 83.3% 意味着什么）

### 3.2 推理强度调优：none / high / max 的"油门"学问
- 三档机制详解：什么时候该踩油门（max）、什么时候该省油（none）
- 同任务三档输出对比实测
- 成本与质量的最佳平衡点
- 与 Claude extended thinking / GPT reasoning 的横向对比

### 3.3 写你自己的 Harness 插件
- 插件结构解析：Everything is a plugin 如何落地
- 实战：写一个"自动生成 commit message"插件
- 实战：写一个"代码安全检查"插件
- 自定义 Agent Preset：标准 / PTC / 极简 / 创造的配置差异

### 3.4 Harness 生产化：从 demo 到可信赖的自动化
- Headless 模式 + CI/CD 集成
- 可观测性：Session Log 的设计哲学与审计价值
- 生产保障：断路器、死信队列、确定性重放
- Python SDK 与 JSON-RPC 接口的工程化用法

### 3.5 DeepSeek Agent 性能调优实战
- 从 DeepSWE 62.7 到实际项目：基准分数的"水分"与真相
- 工具调用组织、错误重试、任务拆分的工程细节
- Agent Loop 设计的取舍：上下文怎么喂、工具怎么排
- 同一模型不同 Harness 的差距：为什么工具层已经成为性能的一部分

---

## 第四部分：踩坑与最佳实践

### 4.1 常见问题排查
- Anthropic 协议兼容的坑：thinking 流式字段、工具调用格式
- 并发 500 被限流怎么办
- 1M 上下文下的 API 超时与重试
- Harness 开发者预览版的兼容性风险（版本升级不兼容）

### 4.2 成本控制实战
- 新价生效前（8 月 17 日前）的窗口期怎么用
- 峰谷定价下的时间策略：把重活安排在空闲时段
- 缓存命中率优化：如何拿到新价最低单价（Pro 空闲缓存命中 ¥0.15/M）
- Pro / Flash 混用的省钱架构
- 一个月的真实账单复盘

### 4.3 安全与合规
- API Key 管理
- Harness 本地 Agent 的权限边界（文件系统、终端命令）
- 代码安全检查清单
- 数据隐私：什么数据适合给 DeepSeek API，什么不适合

### 4.4 综合案例：用 DeepSeek 全家桶搭一个"一人公司"内容系统
- 全景：选题 → 调研 → 写作 → 排版 → 发布 → 数据复盘
- V4 Pro + Harness + Flash 各环节怎么分工
- 多 Agent 编排方案
- 完整成本与收益账
- 复盘：AI 干到了什么程度，人省下了多少时间

---

## 附录

### A. 常用资源
- 开源仓库：github.com/deepseek-ai/deepseek-harness
- npm 包：`@deepseek-ai/dsh`
- API 文档：https://api-docs.deepseek.com
- 官方公告：模型 & 价格页

### B. 写作素材追踪
- 关注：官方"DeepSeek Harness团队"公众号（2026年已单独注册）
- 关注：V4 Pro 涨价官方通知
- 关注：Harness 从 Developer Preview 到正式版的演进

### C. 更新日志
- 2026-08-13：系列建立，覆盖 V4 Pro 0813 正式版 + Harness 开源两大事件
- 2026-08-13：1.1 成文（md + wx.html），进度 1/18
- 2026-08-13：1.2 成文（md + wx.html），进度 2/18
- 2026-08-13：1.3 成文（md + wx.html），进度 3/18
- 2026-08-13：1.4 成文（md + wx.html），进度 4/18；第一部分（入门认知）完结

---

## 写作原则（沿用 wordwork 体系）

1. **不追热点，建体系** — 蹭的是热度，建的是 DeepSeek Agent 工作流的知识体系
2. **可操作，不空谈** — 每篇都有能跑起来的命令和配置
3. **有场景，接地气** — 从内容创作者、开发者、独立开发者的真实需求出发
4. **实时性，真实性** — 信息以 2026 年 8 月 13 日发布时点为准，价格/规格变动需持续追踪更新
5. **竞品对照有据** — 与 Claude Code / Codex 对比时基于真实使用体验，不吹不黑

---

*本大纲随 DeepSeek 产品演进持续迭代。*

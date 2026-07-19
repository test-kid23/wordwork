# Claude Code 系列创作大纲

> Anthropic 推出的终端内 Agentic 编码工具，132k+ GitHub Stars，面向公众号读者的深度内容规划

---

## 整体定位

**Claude Code 不是"代码补全插件"，也不是"聊天机器人"。**

它是驻扎在终端里的 **Agent 式编码工具** —— 深度理解整个代码库，通过自然语言直接操作文件、执行命令、管理 Git。它不给你建议，它直接动手干活。

跟 CodeBuddy / Cursor / Copilot 的关键差异：
- **CodeBuddy / Copilot**：在 IDE 里帮你补全代码、回答问题 → 你问它答，你复制粘贴
- **Claude Code**：在终端里直接读写你的项目文件、跑命令、提 PR → 你说需求，它从头干到尾

这也是为什么它叫 "agentic coding tool"：它是**代理**，不是辅助。

---

## 第一部分：入门教程系列

### 1.1 Claude Code 是什么？—— 你的终端里多了一个程序员同事
- Claude Code 的官方定位：Agentic Coding Tool（代理式编码工具）
- 和 GitHub Copilot、Cursor、CodeBuddy 的本质差异：从"辅助"到"代理"
- 核心能力全景：代码库理解 → 文件操作 → 命令执行 → Git 管理 → 自然语言交互
- 谁适合用？开发者 / 技术写作 / 自动化脚本 / 想用 AI 提效的非程序员
- 上手前的准备：Anthropic 账号、API Key、终端环境、一颗敢放手让 AI 干活的心
- GitHub 132k+ Stars 背后的社区生态

### 1.2 安装与配置：从零到第一个对话
- 安装方式速览：
  - macOS / Linux：`curl -fsSL https://claude.ai/install.sh | bash`（官方推荐）
  - Homebrew：`brew install --cask claude-code`
  - Windows：`irm https://claude.ai/install.ps1 | iex`（官方推荐）
  - WinGet：`winget install Anthropic.ClaudeCode`
  - ⚠️ NPM 方式已弃用，不要再 `npm install -g @anthropic-ai/claude-code`
- API Key 配置：`ANTHROPIC_API_KEY` 环境变量
- 进项目目录，敲 `claude`，开始第一个对话
- 第一个实战：让 Claude Code 解读一段项目代码，感受"Agent 直接动手"的体验
- 常见安装坑：网络代理、权限问题、Windows 终端编码

### 1.3 CLAUDE.md —— 给 AI 同事的项目说明书
- CLAUDE.md 是什么：Claude Code 的项目级记忆文件，类似给新同事的 Onboarding 文档
- 为什么必须写：没有 CLAUDE.md，Claude Code 就是盲人摸象
- CLAUDE.md 应该包含什么：项目结构、技术栈、编码规范、命名约定、测试命令、常见陷阱
- 示例：为一个真实项目编写 CLAUDE.md（附完整模板）
- 上下文管理的三个层次：对话内临时说明 → CLAUDE.md 项目记忆 → 工作区文件实时读取
- Hook 机制：用 CLAUDE.md 中的 Hook 定义自定义行为（保存时自动格式化、提交前自动跑测试）

### 1.4 Claude Code 的权限模型与安全边界
- 权限分层：读文件 / 写文件 / 执行命令 三种权限级别
- 怎么安全地让 AI 操作文件系统：白名单目录、敏感文件排除
- Claude Code 会收集什么数据？使用数据、对话数据、/bug 反馈
- Anthropic 的隐私承诺：反馈数据不用于模型训练、会话数据有限保留期
- 企业场景安全建议：隔离敏感项目、定期审计 AI 操作记录

---

## 第二部分：实战场景系列

### 2.1 用 Claude Code 快速接手一个陌生项目
- 场景：入职新公司 / 接手开源项目 / 临时被拉去修别人的代码
- 实操：让 Claude Code 分析项目结构，生成模块依赖关系图
- 实操：快速定位关键入口文件和核心业务逻辑
- 实操：让它解释一段你没见过的复杂代码在干什么
- 输出：一份可交付的"项目概览文档"，以后给新人看也行

### 2.2 日常开发加速：从需求到 PR 一气呵成
- 场景：实现一个完整功能，不是改一行代码
- Claude Code 参与需求拆解：把模糊需求转成可执行的步骤
- 代码生成 + 单元测试：写好功能顺手写好测试，不偷懒
- 让 Claude Code review 你自己的改动：它能发现你没注意到的问题
- 实测对比：同一功能，有 Claude Code vs 纯手动的时间差异

### 2.3 用 Claude Code 做技术写作
- 场景：写技术博客、API 文档、Release Notes、变更日志
- 从代码自动生成文档：给它一个函数，生成完整的中文 API 说明
- 润色和翻译已有技术文章：英文博客 → 中文公众号推文一气呵成
- 示例：如何用 Claude Code 写一篇"如何用 Claude Code"的公众号教程（套娃实战）

### 2.4 Claude Code + GitHub 工作流
- 场景：自动化 Git 操作，减少机械劳动
- 自动生成 commit message：基于 diff 内容，写符合 Conventional Commits 规范的提交信息
- 自动生成 PR 描述：把这次改了什么、为什么改、影响范围写清楚
- 自动生成 CHANGELOG：从 commit 历史到版本发布说明
- GitHub 上的 `@claude` 标签：在 Issue/PR 里直接召唤 Claude Code 干活
- CI/CD 中集成 Claude Code 的实践思路

---

## 第三部分：进阶技巧系列

### 3.1 提示词工程：让 Claude Code 更懂你的意图
- 好 prompt vs 差 prompt 效果对比（附真实截图级对比）
- 分层提示技巧：角色设定 → 任务目标 → 约束条件 → 输出格式
- 多轮对话策略：不要一次说完所有需求，逐步细化
- 角色扮演法：让它当架构师 / 代码审查者 / 测试工程师 / 技术作家
- System Prompt 与 CLAUDE.md 的配合：什么放哪里

### 3.2 Token 管理与成本优化
- Token 是怎么计算的：输入 Token vs 输出 Token，代码的 Token 消耗特征
- 上下文窗口限制：Claude 的 context window 有多大，满了怎么办
- 长对话的压缩与续接：如何在超长任务中不丢失上下文
- 大项目策略：分模块交互、关键文件索引、按需加载上下文
- 成本估算：一个典型开发任务花多少 API 费用？怎么省

### 3.3 多模型协同：Claude Code 不是孤军奋战
- Claude Code 最擅长的场景：复杂逻辑推理、长代码重构、多文件联动
- 什么时候该换模型：简单脚本用便宜模型、实时性要求高的场景
- 与本地模型的配合：Ollama / llama.cpp 做简单任务，Claude 做重活
- 构建多模型流水线：一个任务自动分发给最合适的模型

### 3.4 插件系统：扩展 Claude Code 的能力边界
- Claude Code 的插件架构：自定义 Commands、自定义 Agents
- 插件目录结构与配置规范
- 实战：写一个"自动生成中文 commit message"的 Command 插件
- 实战：写一个"代码安全检查"的 Agent 插件
- 社区插件生态：有哪些好用的第三方插件

### 3.5 MCP 协议与外部工具集成
- MCP（Model Context Protocol）是什么，跟 API 有什么区别
- 接入外部资源：数据库查询、测试平台、监控告警
- 自定义 Slash Command：一键执行复杂操作序列
- 工具链串联实战：Claude Code → 调数据库 → 生成报表 → 发消息

### 3.6 大项目导航与上下文策略
- 代码库超过 10 万行时，Claude Code 怎么不迷路
- 分模块策略：为不同模块编写独立的 CLAUDE.md
- 索引式导航：先让 Claude Code 了解骨架，再看具体模块
- Monorepo 场景：多个子项目怎么让 Claude Code 分别理解
- .claudeignore：告诉 Claude Code 哪些文件别看

### 3.7 自主执行：让 Claude Code 自己跑完整个任务（2026 新功能）
- 核心问题：以前 Claude Code 每轮都需要你确认，无法"设好目标就去干别的事"
- `/goal` 目标驱动循环：设定可验证的完成条件，AI 自动多轮执行直到达标
  - 工作原理：主模型干活 → 轻量评估模型（Haiku）独立判断是否达标 → 未达标继续
  - 典型场景：修到所有测试变绿、优化到 Lighthouse 90 分、代码迁移直到零报错
  - 风险警示：有开发者 14 小时烧光 $200 额度——必须加 turn 上限
  - 条件三要素：可测量终态 + 验证方法 + 约束条件
- `/loop` 时间驱动循环：按固定间隔自动执行监控类任务
  - 工作原理：cron 式定时触发，不关心上一轮结果，到点就干
  - 典型场景：定时检查 PR 评论并自动修复、周期性监控部署状态、定期扫描错误日志
  - 两种模式：固定间隔 vs 自适应间隔（Claude 根据任务活跃度自己判断等待时长）
  - 与 `/goal` 的区别：时间触发 vs 条件触发，等你回来的 vs 做到达标才停的
- `/schedule` 云端定时任务：不依赖本地会话，后台独立运行
  - 场景：凌晨跑全量测试、每日早晨审查 Issues 并打标签、每周清理死代码
- `/workflows` 并行工作流：将一个复杂任务拆给多个 Agent 同时干，最后汇总
  - 规格：最多 16 个并发 Agent，单次 run 总计不超过 1000 个
  - 场景：全仓库代码扫描、跨多个来源调研、大规模重构
- 选型决策口诀：条件明确选 /goal、周期监控选 /loop、跨会话选 /schedule、并行大规模选 /workflows

---

## 第四部分：踩坑与最佳实践

### 4.1 常见报错与解决方案
- 网络连接问题（代理配置、防火墙）
- API 配额耗尽（速率限制、账单）
- Token 超出限制（怎么处理超长文件）
- 权限拒绝问题（文件系统、命令执行权限）
- 模型幻觉：生成的代码看着对、跑起来炸

### 4.2 代码质量：别做 AI 的"无脑搬运工"
- 验证 Claude Code 生成的代码：先跑测试、再看逻辑、最后看风格
- 安全红线：硬编码密钥、SQL 注入、不安全的依赖版本
- 风格一致性：AI 写的代码和团队规范对齐
- 哪些代码必须人工写、哪些可以让 AI 代劳

### 4.3 成本管理：不让 API 账单吓到你
- API 费用透明化：怎么查看花了多少钱
- 本地模型替代方案：哪些场景可以用 Ollama 省钱
- 批处理 vs 交互式：批量任务一次性提交更省钱
- 团队用量管理：多人共享 Key 的策略与风险

### 4.4 综合案例：用 Claude Code 从零搭一个项目
- 完整流程复盘：初始化 → 架构设计 → 写代码 → 测试 → 文档 → 部署
- 每一步 Claude Code 做了什么，人做了什么
- 最终成果展示与反思
- 复盘：哪些环节 AI 超预期，哪些还需要人类判断

---

## 附录

### A. 常用命令速查表
- `/bug`：一键提交 Bug 反馈
- `/clear`：清空对话历史
- `/compact`：压缩上下文（长对话续命）
- `/config`：修改配置
- `/cost`：查看当前对话的 Token 消耗
- `/doctor`：环境诊断
- `/init`：初始化项目的 CLAUDE.md
- `/login` / `/logout`：账户管理
- `/memory`：查看/编辑记忆
- `/status`：查看当前状态

### B. 官方资源与推荐阅读
- 官方文档：code.claude.com/docs/en/overview
- Discord 社区：Claude Developers Discord
- 官方仓库：github.com/anthropics/claude-code

### C. 更新日志
- 跟随 Claude Code 版本更新同步迭代

---

*本大纲基于 Anthropic 官方 Claude Code 仓库（github.com/anthropics/claude-code）社区信息整理，内容为独立理解与表述，非官方文档翻译。具体文章写作中如需引用官方原文，将注明出处。*

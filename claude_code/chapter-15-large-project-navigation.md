# 15 万行代码不迷路——大项目下 Claude Code 的上下文管理策略

> 你在第 8 轮对话里让它改一个函数，它的输出里出现了第 1 轮才讨论过的文件——这说明它迷路了。上下文爆了。不是 Claude Code 不行，是你的项目管理策略没跟上。

---

前几篇学了很多 Claude Code 的技巧——提示词、多模型、插件、MCP。但你可能发现了：**这些技巧在代码量小的时候很好用，一到大项目就全废了。**

大项目的问题不是"技巧不够好"。是**上下文爆了**。Claude Code 一次能处理的上下文有限——超过某个阈值，它开始"遗忘"、"张冠李戴"、"自己都不知道在改什么"。这不怪 AI，这是信息架构的问题。

这篇跟你聊怎么在大项目里搭这套信息架构。

---

**本文目录：**

- 一、大项目的核心矛盾：信息太多，脑子太小
- 二、分模块策略：每个模块有自己的 CLAUDE.md
- 三、索引式导航：先认识骨架，再看具体器官
- 四、Monorepo 怎么分而治之
- 五、.claudeignore：不让它分心的艺术

---

## 一、大项目的核心矛盾：信息太多，脑子太小

### 先看一组数字

假设你的项目有 15 万行代码，分布在 800 个文件里。Claude Code 的一次上下文窗口，大概能装下 20-30 个平均大小的文件。

**上下文窗口只能覆盖项目总代码量的 3-4%。**

这意味着什么？不是"Claude Code 能看一部分代码"——是**Claude Code 必须在你没告诉它的情况下，猜其他 96% 的代码是什么。**

这就是为什么在大项目里，它会"不知道这个函数在哪里定义"、"改了这里没想到那里会受牵连"、"引入了不符合项目风格的写法"。

### 大项目跟小项目的本质区别

| | 小项目（< 3 万行） | 大项目（> 10 万行） |
|------|------|------|
| 它能一次读完 | 基本能 | 不可能 |
| 模块间依赖 | 你基本都知道 | 依赖图可能几十个节点 |
| 代码风格一致性 | 肉眼可确认 | 不同模块可能风格不同 |
| "改这里影响哪" | 跑一下就知道 | 不跑全量测试不确定 |

所以大项目的策略不是"把更多代码塞给它"——是**帮它建立一套不需要读所有代码就能理解项目的机制**。

---

## 二、分模块策略：每个模块有自己的 CLAUDE.md

### 为什么要分模块

全局 CLAUDE.md 写的是"项目级别"的信息——技术栈、命名规范、文件结构。但对于大项目来说不够。因为每个模块有自己的约定、自己的抽象层次、自己的第三方依赖。

**模块级的上下文应该放在模块根目录下。**

### 目录结构

```
your-large-project/
├── CLAUDE.md                          # 全局：技术栈 + 项目级规范
├── src/
│   ├── user/
│   │   ├── CLAUDE.md                  # 用户模块专属
│   │   ├── UserService.ts
│   │   └── UserRepository.ts
│   ├── order/
│   │   ├── CLAUDE.md                  # 订单模块专属
│   │   ├── OrderService.ts
│   │   └── OrderRepository.ts
│   └── payment/
│       ├── CLAUDE.md                  # 支付模块专属
│       ├── PaymentService.ts
│       └── PaymentGateway.ts
└── .claudeignore
```

### 模块级 CLAUDE.md 怎么写

**全局跟模块的区别：**

全局 CLAUDE.md：
- 技术栈（React 18、Prisma ORM）
- 命名规范（PascalCase 组件、camelCase 工具函数）
- 文件组织规则（pages/、components/、hooks/ 啥用啥）
- 当前开发焦点

模块级 CLAUDE.md：
- **本模块的架构模式**（Service → Repository 还是直接用 ORM）
- **模块特有的约定**（比如 order 模块用 event-driven，user 模块用 CRUD 直连）
- **对外接口清单**（哪些函数被其他模块调用——这些不能随便改签名）
- **已知的技术债和注意事项**（比如 payment 模块的退款逻辑还没重构）

示例——`src/payment/CLAUDE.md`：

```markdown
# Payment Module

## Architecture
- Service: 业务逻辑层。PaymentService 处理支付流程，RefundService 处理退款。
- Gateway: 外部接口适配层。统一封装了支付宝和微信支付的调用差异。
- Repository: 数据访问层。只负责读/写 payments 和 refunds 表。

## Public API（其他模块可能调用这些）
- PaymentService.createPayment(orderId, amount, method) → PaymentResult
- PaymentService.checkStatus(paymentId) → PaymentStatus
- RefundService.processRefund(orderId, amount, reason) → RefundResult

注意：修改这些函数的签名必须同时检查所有调用方。

## Conventions
- 金额单位：分（int），前端展示时除 100。
- 支付状态不直接在 Service 里改数据库——通过 Repository 统一管理。
- 外部调用（支付宝/微信）必须有超时设置（默认 10s），避免阻塞。

## Known Issues
- RefundService 的重复退款检测逻辑和 OrderService 里的逻辑重复。
  下一步计划抽取到 shared/refund-validator.ts。目前先保持两边的同步。
- 支付宝回调的通知格式和文档不一致——实际 JSON 比文档多了一个 sign 嵌套层。
  见 PaymentGateway.processAlipayCallback() 里的 workaround。
```

用了这份 CLAUDE.md，当你让 Claude Code "在支付模块加一个新功能"时，它不需要读全模块的 15 个文件——它只需要读这份文档就知道：
- 架构层次
- 哪些函数签名不能随便改
- 货币单位用分
- 退款检测有已知的重复逻辑，先绕过

**一份 2000 字的 CLAUDE.md，替代了每次对话都要读的 5000 行代码。**

---

## 三、索引式导航：先认识骨架，再看具体器官

### 你到一个陌生城市是怎么找路的

你不会从火车站开始一条一条街走遍全城。你会先拿一张地图——看主干道、核心区域、各区关系。然后去哪就只看那一小块。

Claude Code 在大项目里也是一样——**先建地图，再按需导航。**

### 第一步：建立项目骨架文档

写一个 PROJECT_STRUCTURE.md，不是给 Claude Code 读的——是让 Claude Code 在每次对话开始时只读这个文件，理解全貌。

```markdown
# Project Structure

## 技术栈
React 18 + TypeScript + Vite（前端）
Express + TypeScript + Prisma（后端）
PostgreSQL 15

## 模块划分

### src/client/ — 前端
- pages/ — 10 个页面级组件，一个页面对应一条路由
- components/ — 36 个可复用组件，UI 库基于 Ant Design 5
- hooks/ — 14 个自定义 Hooks，usePagination 被 6 个页面引用（核心）
- api/ — 21 个 API 请求函数，对应后端的 21 个接口
- stores/ — Zustand store，只放了 user 和 app 两个全局状态

### src/server/ — 后端
- routes/ — 4 个子路由模块：users, orders, payments, analytics
- services/ — 业务逻辑层，一个 service 对应一个路由模块
- models/ — Prisma schema，包含 User, Order, Payment, Product 等 9 个表
- middleware/ — 4 个中间件：auth, rateLimit, logger, errorHandler

## 核心依赖关系
- 前端所有 API 调用 → src/client/api/（不要直接写 axios）
- 后端路由 → services → Prisma → PostgreSQL
- payments 模块同时依赖 orders（查订单金额）和 users（查用户风控状态）
- analytics 模块只读数据库，不写

## 高风险文件
- src/server/middleware/auth.ts — 认证中间件，所有接口都用，改动影响全局
- src/client/hooks/usePagination.ts — 被 6 个页面引用，改签名要全局搜索
- Prisma schema — 改字段要考虑 migration + 向后兼容

---
最后更新：2026-07-19
当前版本：v2.3.1
```

这份文档约 600 行。每次 Claude Code 启动，读一遍——500 个 token。换来的是一张"项目地图"。之后的对话里，你说 "改 payments 模块"，它不需要自己翻 800 个文件去理解结构——地图已经有了。

### 第二步：按需深入

有了地图，每次你的指令应该精确到模块：

❌ "优化支付模块的性能"——它会全读 payment/ 下的 15 个文件。

✅ "优化 payment/PaymentService.ts 的 createPayment 函数。基于项目骨架文档，这个函数的调用链包括 payment/PaymentGateway.ts 和 orders/OrderService.ts。先读这三个文件，分析瓶颈。"

精确到**具体文件 + 调用链**。Claude Code 只读 3 个文件而不是 15 个。剩下 12 个文件的上下文空间留给你后续的交互。

### 第三步：定期更新地图

项目在演进，骨架文档也得跟着变。定一个规矩：**每次合并一个涉及架构改动的 PR 时，顺便更新 PROJECT_STRUCTURE.md。**

不是大改——改一句就行。"analytics 模块现在也写数据库了"、"新增了一个 shared/ 模块"——就这些。让文档跟现实保持同步。

---

## 四、Monorepo 怎么分而治之

Monorepo 是大项目的进阶形态——多子项目共享一个仓库。每个子项目有自己的技术栈、自己的构建工具、自己的团队。

### 核心策略：隔离上下文

**不要让 Claude Code 在"子项目 A"的上下文里看到"子项目 B"的代码。**

怎么做：

**每个子项目有独立的 CLAUDE.md**

```
your-monorepo/
├── CLAUDE.md                          # 全局：子项目清单 + 共享规范
├── apps/
│   ├── web/
│   │   ├── CLAUDE.md                  # Web 子项目上下文
│   │   └── ...
│   └── admin/
│       ├── CLAUDE.md                  # Admin 子项目上下文
│       └── ...
├── packages/
│   ├── shared-ui/
│   │   ├── CLAUDE.md
│   │   └── ...
│   └── shared-utils/
│       ├── CLAUDE.md
│       └── ...
└── .claudeignore
```

CLAUDE.md（全局）只放一件事：**子项目关系图**。

```markdown
# Monorepo Overview

## 子项目
- apps/web — 用户端 React 应用。端口 3000。
- apps/admin — 后台管理系统。React + Ant Design Pro。端口 3001。
- packages/shared-ui — 两端共享的 UI 组件。被 web 和 admin 引用。
- packages/shared-utils — 工具函数。格式化、校验、常量。

## 依赖规则
- shared-ui 和 shared-utils 是基础包——改它们的代码要同时检查 web 和 admin 的兼容性。
- web 和 admin 之间没有直接的代码依赖——不需要交叉检查。
```

### 操作时的隔离

当你的指令针对某个子项目时，在 Claude Code 的启动命令里指定工作目录：

```bash
cd apps/web && claude
```

而不是在根目录启动。这样 Claude Code 的自然上下文范围就被限定在 web 子项目内——它不会误读到 admin 的代码。

### 跨子项目的改动

如果需要同时改 shared-ui 和 web，先改 shared-ui（独立的 CLAUDE.md 上下文），确认改动合理后，再切到 web 验证兼容性。

不要在一次对话里跨越两个子项目——Claude Code 会尝试加载两边的 CLAUDE.md 和上下文，直接爆掉。

---

## 五、.claudeignore：不让它分心的艺术

### 它解决的核心问题

你的项目文件夹里有很多文件 Claude Code 不需要看——编译产物、构建缓存、测试覆盖率报告、node_modules、图片、字体。但默认情况下，Claude Code 搜索代码的时候会扫所有文件。

`.claudeignore` 告诉它："这些文件夹，别看。"

### 推荐配置

```gitignore
# .claudeignore

# 依赖和大文件
node_modules/
.pnpm-store/
*.lock

# 构建产物
dist/
build/
.next/
.output/

# 测试覆盖率
coverage/
.nyc_output/

# 缓存
.cache/
.turbo/
.eslintcache

# 媒体文件（没有代码上下文价值）
*.png
*.jpg
*.gif
*.svg
*.mp4
*.woff2
*.ttf

# IDE 和工具配置
.idea/
.vscode/
.husky/

# 数据库文件
*.sqlite
*.db

# 大日志
*.log
```

配置好之后：Claude Code 的 `Grep` 和 `Glob` 工具——也就是它搜索代码时用的——会跳过这些目录和文件。它的搜索结果更干净、更准确，更重要的是**不浪费 token 去读没意义的内容**。

---

## 写在最后

这一章是本系列的最后一篇。如果用一个词概括大项目里的核心策略，我会选：**克制。**

克制你"让 AI 看全项目"的冲动。克制你"一次把所有需求说明白"的欲望。克制你"反正它能读，让它全读了"的偷懒。

大项目跟 Claude Code 的协作，不是"把代码全喂给它再提需求"。是**你作为项目的导游，带它只看该看的地方。**

CLAUDE.md 是你的导览图。模块级上下文是你的分区地图。索引式导航是你的"先去哪再去哪"的路线。.claudeignore 是你的路障。

这套设施搭好了，15 万行的项目在 Claude Code 眼里就是一个"分成了 8 块的乐高"。每一块都清晰、每一块都有说明——它可以专注地拼你交给它的那一块，不会迷路。

祝你在自己的大项目里，跟 Claude Code 配合默契。

---

*Claude Code 实战系列 · 大项目导航*
*本系列涵盖入门教程、实战场景、进阶技巧三大模块，共 15 篇。完整目录可在公众号合集「Claude Code 实战」中查看。*

# Claude Code 能查数据库、调接口、发消息了——MCP 协议完全指南

> Claude Code 以前只能读你项目的文件。现在它能连数据库查实时数据、调你的内部 API、往 Slack 发通知——像一个真正的后端工程师。秘密是 MCP（Model Context Protocol）。

---

Claude Code 的基础能力你都很熟了：读文件、写代码、跑命令、搜代码。但它一直有一个硬边界——**它只能操作你本机的代码文件。**

如果需求是"查一下数据库里最近 24 小时的异常订单"、"调一下我们的内部 API 看看那个配置值"、"跑完测试之后往 Slack 发一条通知"——以前这些必须你手动做。

MCP 协议打通了这个边界。它让 Claude Code 能像调用本地文件一样调用外部服务。

---

**本文目录：**

- 一、MCP 是什么——不是又一个 API 格式
- 二、第一个 MCP 连接：让 Claude Code 查数据库
- 三、自定义 Slash Command：把复杂操作一键化
- 四、工具链串联：Claude Code → 数据库 → 报表 → Slack
- 五、安全：权限控制是你的最后防线

---

## 一、MCP 是什么——不是又一个 API 格式

### 一句话版本

MCP（Model Context Protocol）是一个标准化协议，定义了 AI 助手**怎么发现**外部工具、**怎么调用**外部服务、**怎么接收**返回数据。

### 它跟 API 的区别

| | REST API | MCP |
|------|---------|-----|
| 谁调用 | 你的代码 | AI 模型 |
| 怎么发现 | 看文档 → 手写调用代码 | 模型自己发现有什么工具、参数是什么 |
| 输入 | 你预设的 JSON | 模型自己根据当前上下文构造的参数 |
| 安全 | 你控制权限 | 你控制权限 + 模型不直接拿密钥 |

核心差异：MCP 不是给你用的，是给 AI 用的。它把 API 暴露给 AI——AI 自己决定什么时候调、调哪个、用什么参数。

### Claude Code 的 MCP 架构

Claude Code 作为一个 MCP 客户端，连接到一个 MCP 服务器：

```
Claude Code (MCP Client)
    ↓ 发现：你有哪些工具？
MCP Server (你部署的)
    ↓ 调用：查一下最近 24 小时的异常订单
PostgreSQL / Slack / Jira / 你的内部 API
    ↓ 返回：查询结果
Claude Code → 基于结果继续分析或写代码
```

MCP Server 是中间人——它拿到 Claude Code 的请求，转成对真实服务的调用，把结果返回。Claude Code 不直接访问密钥、不直接连数据库——它通过 MCP Server 间接访问。

---

## 二、第一个 MCP 连接：让 Claude Code 查数据库

### 需要什么

Claude Code 官方提供了 MCP Server 的参考实现。你不需要从头写——用现成的就行。

以 PostgreSQL 为例，社区有一个 `mcp-server-postgres` 包。安装配置 5 分钟：

```bash
# 1. 安装 MCP Server
npm install -g @anthropic/mcp-server-postgres

# 2. 在 ~/.claude/mcp.json 里配置
```

### mcp.json 配置

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-postgres", "postgresql://user:pass@localhost:5432/mydb"]
    }
  }
}
```

`mcpServers` 下每一条就是一个外部工具。这里配置了一个 `postgres` 工具。

### 使用

配置好之后，你在 Claude Code 里直接问：

> "查一下 orders 表里最近 24 小时 status 是 failed 的订单有多少，按小时分组统计。"

Claude Code 会：
1. 发现有一个 `postgres` 工具可用
2. 自动生成正确的 SQL：`SELECT date_trunc('hour', created_at), count(*) FROM orders WHERE status = 'failed' AND created_at > now() - interval '24 hours' GROUP BY 1 ORDER BY 1;`
3. 通过 MCP Server 执行查询
4. 拿到结果后，帮你分析——"凌晨 2-3 点有 47 个失败，是平时的 10 倍，可能跟定时任务有关"

注意——**你没有写一条 SQL。** 你只描述了你想知道什么，Claude Code 自己去生成 SQL、执行、分析结果。

### 试试更多的 MCP 连接

MCP 能接的东西远不止数据库：

```json
{
  "mcpServers": {
    "postgres": { ... },
    "slack": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-slack"]
    },
    "jira": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-jira"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-filesystem", "/path/to/allowed/dir"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-github"]
    }
  }
}
```

接上之后：
- `slack` → Claude Code 能发消息到 Slack 频道
- `jira` → 能搜 Issue、看状态、关联任务
- `filesystem` → 能读写指定目录的文件（比默认的更精细）
- `github` → 能在 Issue 和 PR 里操作、搜索代码

---

## 三、自定义 Slash Command：把复杂操作一键化

### 什么是 Slash Command

Slash Command 是 MCP 在 Claude Code 里的 UI 入口——一个 `/` 命令。你可以把一系列操作打包成一个命令。

但跟插件里的 Command 不同——Slash Command 可以**调用 MCP 工具**。

### 定义方式

在 `~/.claude/slash-commands.json` 里定义：

```json
{
  "commands": {
    "/deploy-check": {
      "description": "部署前检查：跑测试、查数据库、通知 Slack",
      "steps": [
        {
          "type": "command",
          "command": "npm test"
        },
        {
          "type": "mcp",
          "server": "postgres",
          "action": "检查是否有未完成的数据库迁移"
        },
        {
          "type": "mcp",
          "server": "slack",
          "action": "在 #deploy 频道发一条 '准备部署到 staging，预检中...'"
        }
      ]
    }
  }
}
```

敲 `/deploy-check`，Claude Code 自动——跑测试 → 查数据库 → 通知 Slack。三步合一。

### 它的意义

你不需要每次部署前在三个终端之间切——Claude Code 把"手动执行的 check list"变成了"一个命令"。不是速度的提升，是**可靠性**的提升。你不会忘记跑测试、不会忘记查数据库、不会忘记通知。

---

## 四、工具链串联：Claude Code → 数据库 → 报表 → Slack

### 场景：每日异常订单报告

每天早上，你想知道"昨天有哪些订单出问题了"，然后发给相关的人。以前可能要：查数据库 → 导出 Excel → 手动分析 → 写邮件/Slack。

有了 MCP，这就是一句话：

> "查 orders 表昨天所有 status 是 failed 或 refunded 的订单。按失败原因分组统计，列出金额 TOP 10 的异常订单。用表格汇总关键数据，然后发到 Slack #ops 频道。"

Claude Code 执行流程：

```
1. 通过 postgres MCP → 查数据库
2. 拿到原始数据 → 在本地分析、分组、排序
3. 生成表格和分析摘要
4. 通过 slack MCP → 发到 #ops 频道
```

全程你没有：写 SQL、打开 Excel、打开 Slack、复制粘贴。你只干了一件事——**用自然语言描述了你想做的工作流**。

### 更复杂的链

```
Claude Code 发现 CI 失败
→ 调 GitHub MCP 读取失败的 workflow 日志
→ 定位到是数据库迁移脚本报错
→ 调 postgres MCP 检查数据库当前状态
→ 发现是字段类型不匹配
→ 自动生成修复的 migration 文件
→ 通过 Slack MCP 通知你 "CI 失败原因已定位，修复文件已生成，请 Review"
```

这条链跨了 GitHub → 数据库 → 文件系统 → Slack。以前需要你手动在不同的工具之间搬运信息。现在是一条流水线。

---

## 五、安全：权限控制是你的最后防线

### MCP 的安全模型

MCP Server 是一个**你部署的中间件**。Claude Code 通过它访问外部服务，不直接持有密钥。

但这不代表安全了——**如果 Claude Code 能给 Slack 发消息，理论上它也能发错消息。如果它能查数据库，理论上它也能执行破坏性的 SQL。**

### 三个必须做的安全措施

**1. 读写分离**

配置只读权限的数据库连接给 Claude Code。查询用只读账号——它不可能执行 `DROP TABLE`，因为它根本没权限。

```json
// mcp_servers.postgres — 用只读账号连接
"args": [..., "postgresql://readonly_user:pass@localhost:5432/mydb"]
```

**2. 操作确认**

对于可能产生副作用的操作（发 Slack 消息、创建 Jira 任务、运行部署脚本），Claude Code 会弹出权限确认。

不要顺手点"允许"。养成看一遍它要干什么的习惯。尤其是它要发的消息——内容有没有偏差？发到正确的频道了吗？

**3. 限制工具范围**

不要让 Claude Code 有所有工具的访问权限。每个 MCP Server 都可以配置允许的操作白名单。

```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-slack"],
      "allowedTools": ["send_message", "read_channel"],
      "deniedTools": ["delete_message", "create_channel", "archive_channel"]
    }
  }
}
```

它只能发消息和读频道——不能删消息、不能创建频道、不能归档。即使 prompt 被误导了，权限本身是最后的防线。

### 为什么这很重要

MCP 让 Claude Code 从"一个能读代码的工具"变成了"一个能操作外部服务的工具"。能力的边界扩展了，风险的边界也扩展了。

一个实用原则：**能读不给写，能写不许删。** 不确定要不要给权限的时候，先用最小的权限试——不够再加。

---

## 写在最后

这篇文章的信息量比较大。如果你觉得一下子消化不了，记住一句话就行：

**MCP 就是把 Claude Code 从"你的代码编辑器"变成了"你的工程助理"。** 它不只是写代码——它能帮你协调代码跟数据库、API、消息通知之间的关系。

这一章的下一集也是本系列最后一集——**大项目里 Claude Code 怎么不迷路**。十几万行的项目，怎么分模块、怎么建立索引、怎么让它始终知道"我在看项目的哪个部分"。

---

*Claude Code 实战系列 · MCP 协议*
*适用对象：需要让 AI 接触真实业务数据的后端开发者 / 想把多个内部工具串联起来的全栈工程师 / 对 AI Agent 架构感兴趣的进阶用户*
*本系列更多文章可在公众号合集「Claude Code 实战」中查看*

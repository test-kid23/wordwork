# 5 分钟写一个 Claude Code 插件——自动生成中文 commit message

> 每次提交都要手写 commit message 很烦？花 5 分钟写个插件，以后敲一行 /commit 就自动生成。插件系统是 Claude Code 最被低估的扩展能力——它让 AI 从"对答工具"变成"你的定制工具"。

---

前几篇把 Claude Code 的核心用法讲得差不多了。但用到现在，你有没有这种感觉：**有些操作你每天都在重复，每次都打一大段话感觉很蠢。**

"帮我根据 git diff 生成一条符合 Conventional Commits 的 commit message"——你可能这句已经打了 50 次。

这就是插件系统的用武之地。把它封装成一个命令，以后敲 `/commit` 就行。

---

**本文目录：**

- 一、Claude Code 的插件能做什么
- 二、第一个插件：自动生成中文 commit message
- 三、第二个插件：代码安全检查 Agent
- 四、插件如何分发和共享
- 五、社区有哪些值得装的插件

---

## 一、Claude Code 的插件能做什么

插件本质上是一段**预定义的指令 + 工具权限**，打包成一个可复用的单元。你不用每次都打那些话——敲一个命令就行了。

Claude Code 支持两种插件：

| 类型 | 是什么 | 典型场景 |
|------|--------|---------|
| **Command** | 一个可调用的指令模板 | `/commit` 生成 commit、`/review` 审查代码 |
| **Agent** | 一个有特定权限和角色的子 Agent | "安全检查员"、"测试编写者" |

两者的核心区别：Command 在**当前对话**里执行，Agent 是**独立子进程**，有自己的角色设定和工具权限。

### 在哪里放插件

Claude Code 读取两个位置的插件：

```
~/.claude/plugins/         ← 全局，所有项目可用
项目根目录/.claude/plugins/  ← 项目级，当前项目专用
```

全局插件放你个人常用的（commit 生成、代码格式化）。项目级插件放跟这个项目强相关的（特定的部署脚本、团队的代码规范审查）。

---

## 二、第一个插件：自动生成中文 commit message

### 插件结构

每个插件是一个 `plugin.json` + 一个指令文件。最简单的结构：

```
~/.claude/plugins/commit-generator/
├── plugin.json
└── prompt.md
```

### plugin.json

```json
{
  "name": "commit-generator",
  "version": "1.0.0",
  "description": "自动生成符合 Conventional Commits 的中文 commit message",
  "commands": [
    {
      "name": "commit",
      "description": "基于 git diff 生成中文 commit message",
      "prompt": "prompt.md"
    }
  ]
}
```

### prompt.md

```markdown
执行 `git diff --staged` 查看暂存的改动。如果没有暂存内容，先提示用户执行 `git add`。

基于改动内容，生成一条 Conventional Commits 格式的 commit message：

1. 第一行：`type(scope): 中文简述`（不超过 50 字符）
   - type: feat / fix / refactor / docs / style / test / chore
   - scope: 改动的模块名（中文）

2. 空一行

3. body：用中文逐条说明改了什么，每条一行，加 `-` 前缀

4. 最后一行：影响范围（列出改动的文件路径）

要求：
- 整个 commit message 用中文（type 和 scope 除外）
- body 要具体——不是 "修复 Bug"，是 "修复了用户在 Safari 下导出按钮重复触发的问题"
- 不要解释你怎么生成的，直接给 commit message

输出示例：
```
feat(用户管理): 新增用户列表 Excel 导出功能

- 后端新增 GET /users/export 接口，基于 exceljs 生成 Excel
- 前端在 UserList 增加导出按钮，支持 loading 态
- 权限校验复用 hasPermission 中间件

影响范围：
- server/src/routes/users.ts
- client/src/pages/UserList.tsx
- client/src/api/users.ts
```
```

### 使用

以后在任何项目里，敲这个就行了：

```bash
/claude commit
```

Claude Code 会自动跑 `git diff --staged`，读 diff 内容，按你定义的格式生成 commit message。

### 进阶：用参数让它更灵活

prompt.md 可以接收参数：

```markdown
<!-- prompt.md -->
执行 `git diff --staged`。如果有参数 `{{type}}`，只在 commit type 里用它指定的。

如果没有参数，自动判断 type。
```

使用：

```bash
/commit type=feat
```

---

## 三、第二个插件：代码安全检查 Agent

Command 是"在当前对话执行一段指令"。Agent 是"给我一个独立的小弟，有特定权限和角色"。

### plugin.json

```json
{
  "name": "security-scanner",
  "version": "1.0.0",
  "description": "代码安全扫描 Agent，检查常见安全漏洞",
  "agents": [
    {
      "name": "security-check",
      "description": "扫描指定文件的常见安全问题",
      "prompt": "agent-prompt.md",
      "tools": ["Read", "Grep", "Glob"],
      "model": "haiku"
    }
  ]
}
```

注意两个关键字段：
- `tools`: 限制 Agent 只能读文件、搜索——**不能写文件**。安全检查不应该改代码——它只负责报告问题。
- `model`: 指定用 Haiku。安全检查是模式匹配为主，不需要深度推理，省成本。

### agent-prompt.md

```markdown
你是一个代码安全审查 Agent。扫描用户指定的文件，检查以下问题：

1. SQL 注入：是否有拼接 SQL 字符串而非使用参数化查询
2. XSS：是否有 innerHTML、dangerouslySetInnerHTML 未转义
3. 密钥泄露：是否有硬编码的 API key、密码、token
4. 路径遍历：是否有未验证的文件路径拼接
5. 认证缺失：是否有需要登录才能访问的接口未加权限校验

对每个文件，输出格式：
- 文件路径
- 风险等级（高/中/低）
- 问题描述 + 行号
- 修复建议（一句话）

只报告真实存在的问题。不要报告"可能有问题但不确定"的——那太多了。有把握再报。
```

### 使用

```bash
/claude security-check src/routes/
```

Agent 会自己扫描 `src/routes/` 下的文件，按你的规则报告安全问题。

### Agent 和 Command 的选择

- **Command**：一个可以反复调用的指令模板。适合"我每次走这个流程"。在当前对话里执行。
- **Agent**：独立的子进程。适合"给它一个角色 + 工具 + 约束，让它自己干"。有独立的上下文，不污染主对话。

---

## 四、插件如何分发和共享

### 给团队用：放到仓库里

把 `.claude/plugins/` 目录提交到 Git 仓库。队友 clone 之后，插件自动可用。

```bash
# 建议的目录结构
your-project/
  .claude/
    plugins/
      commit-generator/
        plugin.json
        prompt.md
      team-code-review/
        plugin.json
        prompt.md
    settings.json      # 可放全局开关
```

### 给社区用：发布为 npm 包

插件可以打包成 npm 包发布。其他用户 `npm install -g` 之后，Claude Code 会识别 `.claude-plugin` 配置。

```json
// package.json
{
  "name": "@yourname/claude-commit-gen",
  "version": "1.0.0",
  "description": "Claude Code 插件：自动生成中文 commit",
  "claude": {
    "plugin": "./plugin.json"
  }
}
```

### 团队协作时的注意事项

插件指令里的约束越具体，不同人使用的结果越一致。同一个 `/commit` 插件，两个人用——一个人可能觉得"挺好"，另一个觉得"风格不对"。

如果给团队用，确保 prompt.md 里的**输出格式样例**足够具体。不要让 AI 有太多发挥空间——这是"规范化"的场景，不是"创作"的场景。

---

## 五、社区有哪些值得装的插件

社区的插件生态还在早期，但已经有一些高质量的选择：

| 插件 | 功能 |
|------|------|
| **conventional-commits** | 自动生成 Conventional Commits 格式的 commit |
| **pr-description** | 自动生成 PR 描述 |
| **code-explainer** | 对选中代码生成中文注释和解释 |
| **test-generator** | 基于源码自动生成测试框架和用例 |
| **changelog-builder** | 从 commit 历史生成 CHANGELOG |
| **refactor-helper** | 辅助重命名变量、提取函数、移动文件 |

这些插件都可以在 `~/.claude/plugins/` 下直接创建——本质就是几行 JSON + Markdown。

### 怎么找更多插件

目前社区插件的分发还比较分散——没有一个统一的"应用商店"。大部分在 GitHub 上以 `claude-code-plugin-*` 或 `claude-plugins` 仓库的形式存在。可以关注 Claude Code 官方的 Awesome List。

---

## 写在最后

这篇文章的价值不在那两个示例插件本身——`/commit` 和 `security-check` 你可能不一定会用。它的价值在**思路**：

Claude Code 的可扩展性远超你的想象。你日常工作中所有"每次都要重复说一遍"的操作，都可以封装成一个插件。5 分钟写一个，以后永远不用再说第二遍。

这其实就是编程本身的原则——**Don't Repeat Yourself**——用在 AI 工具上。

---

*Claude Code 实战系列 · 插件系统*
*适用对象：觉得"每次都打同一段话很蠢"的开发者 / 想给团队制定 AI 使用规范的 Tech Lead / 对扩展 Claude Code 感兴趣的进阶用户*
*本系列更多文章可在公众号合集「Claude Code 实战」中查看*

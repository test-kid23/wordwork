# 写了代码还要写 Commit、PR、Changelog？Claude Code 把这些全自动化了

> 你写了 200 行代码。然后花了 20 分钟想 commit message、写 PR 描述、更新 CHANGELOG。这 20 分钟 AI 用 3 秒就能做完——而且写得比你更好。

---

上篇聊了用 Claude Code 做技术写作——基于你的代码生成文档、翻译博客、润色排版。

这篇要补上日常开发流程里同样容易被忽略但同样消耗精力的环节：**Git 操作的文案工作**。

Commit message、PR 描述、CHANGELOG、Release Notes——这些都不是"写代码"本身，但它们直接决定了你的代码能不能被理解、被 Review、被维护。偏偏这些事，大部分开发者是"临时糊一个"。

Claude Code 在这个环节的提效，不是"让你的 commit 更规范"这么简单——是**让你不用再在这种事情上浪费脑细胞**。

---

**本文目录：**

- 一、告别 "fix bug"：让 Claude Code 读懂你的 diff 写 commit
- 二、PR 描述：让你的 Reviewer 秒懂你做了什么
- 三、CHANGELOG 自动生成：从 commit 历史到版本说明
- 四、GitHub Issue/PR 中 @claude：让 AI 参与协作
- 五、在 CI/CD 中集成 Claude Code：以代码审查为例

---

## 一、告别 "fix bug"：让 Claude Code 读懂你的 diff 写 commit

### 一个谁都见过的场景

你改完了一个功能，做了一堆修改，然后 `git add .`，接着盯着终端想了 10 秒——commit message 写什么？

"update code"？太敷衍。
"fix user list export bug and add loading state and refactor pagination hook"？太长。
"feat: add user export"？好像少说了什么。

最后你写了 "fix: update"。

三天后回来看，你不知道这次改了啥。

### 实操：让 Claude Code 读 diff → 写 commit message

在你 `git add` 之后、`git commit` 之前：

> "git diff --staged 看一下我这次改动的内容，帮我生成一条 Conventional Commits 格式的 commit message。用中文写 body 部分，说清楚改了什么、为什么改、影响了哪些范围。"

Claude Code 会执行 `git diff --staged`，看完所有改动，然后给你类似：

```
feat(user): 用户列表导出 Excel + 前端导出按钮

- 后端新增 GET /users/export 接口，基于 exceljs 生成 Excel 文件流
- 前端在 UserList 页面新增导出按钮，调用导出接口触发文件下载
- 导出按钮增加 loading 态，防止短时间内重复点击
- 权限校验复用 hasPermission 中间件，管理员才可见导出按钮

影响范围：server/src/routes/v1/users.ts, server/src/services/export.service.ts,
client/src/pages/UserList.tsx

Closes #127
```

然后你 `git commit -m "那条 message"` 就行了。

### 为什么它写得比你好

不是 Claude Code 文笔好。是它**不会偷懒**。

你写 commit message 的时候在想什么？"差不多就行了，回头也没人看。" Claude Code 没有"差不多就行了"这个设定。它读了你每一行改动，然后忠实总结——不管你是改了 3 行还是 300 行，它都会认真处理。

而且它**即时执行**。你不需要切到 ChatGPT 网页、复制 diff、粘贴、等回复、复制回来——全程在一个终端里完成。这个"不用切窗口"的流畅感，用过的都知道差别。

### 进阶：符合你团队的规范

每个团队的 commit 规范不一样。有些团队用 Angular 规范，有些用自定义前缀。你可以让 Claude Code 适配：

> "看一下项目根目录有没有 commitlint 配置、commitizen 配置或者 CONTRIBUTING.md 里的 commit 规范。按那个规范写这次的 commit message。"

---

## 二、PR 描述：让你的 Reviewer 秒懂你做了什么

### PR 的隐性成本

提 PR 只需要点一个按钮。但一个好的 PR 描述需要回答三个问题：

1. **这是什么？** —— 改了什么功能或修了什么 Bug
2. **为什么这样改？** —— 为什么选这个方案而不是别的
3. **影响范围？** —— Reviewer 应该重点看哪些文件

90% 的 PR 描述只回答了第一个问题，而且是用最敷衍的方式："修复了用户导出按钮的样式问题"。

后果是你的 Reviewer 要自己看一遍 diff 才能理解这次改了什么。几十个文件的改动，Reviewer 光理清逻辑就要十几分钟。然后才会开始真正的"检查代码有没有问题"。

### 实操：自动生成 PR 描述

> "对比 main 分支，生成这次 PR 的描述。格式：1）一句话概述 2）详细改动说明（按模块分组）3）为什么这样改 4）影响范围和风险 5）Review 重点。用中文。"

Claude Code 会 `git diff main...feature-branch`，生成类似：

```
## 概述
新增用户列表 Excel 导出功能，支持管理员全量导出，
支持自定义导出字段。

## 改动详情

### 后端（server/）
- `routes/v1/users.ts` — 新增 GET /users/export 接口，
  权限校验使用已有的 hasPermission 中间件
- `services/export.service.ts` — 新增导出服务层，
  基于 exceljs 生成 Excel，支持流式写入
- `types/export.ts` — 新增导出相关类型定义

### 前端（client/）
- `pages/UserList.tsx` — 新增导出按钮（loading 态 +
  重复点击防护）；导出弹窗组件
- `api/users.ts` — 新增 exportUsers 请求函数

### 依赖
- 新增 `exceljs@4.4.0`

## 为什么这样改
- 使用 exceljs 而非 xlsx-populate：前者社区更活跃、支持流式写入、
  可以处理 10 万级数据而不 OOM
- 导出放在 services 层而非直接写在 route 里：保持三层架构的
  一致性（route → service → model）

## 影响范围和风险
- 低风险：新功能，不影响已有接口
- 风险点：大用户量（> 5 万）导出时的内存占用，已在 services
  加了 chunk 处理，建议 merge 后压测验证

## Review 重点
请重点看：
1. export.service.ts 的 chunk 处理逻辑
2. UserList.tsx 导出按钮的防重复点击实现
```

### 这个 PR 描述对 Reviewer 意味着什么

一个普通的 PR 描述，Reviewer 需要：
1. 读完所有 diff 才知道改了啥 —— 10 分钟
2. 自己想"这么改对不对" —— 5 分钟
3. 标注重点看哪 —— 1 分钟（大多数人不标）

这个 PR 描述，Reviewer 花 30 秒看完描述，就知道：
- 这次改了哪些文件、为什么改
- 哪里是重点、哪里是简单调整
- 有什么风险、要不要压测

**你把 Reviewer 的信息整理成本，转嫁给了 AI。**

---

## 三、CHANGELOG 自动生成：从 commit 历史到版本说明

### 为什么 CHANGELOG 总是最后才写

每次发布，"写 CHANGELOG"总是最后一刻才想起来的事。前面功能开发、测试、修 Bug 忙了一整个迭代，CHANGELOG 就拖到发版前草草写几行。

问题不在态度，在流程——CHANGELOG 应该是在开发过程中自动积累的，不是发版时回忆的。

### 实操：一键生成 CHANGELOG

> "从上次发布的 tag（v1.2.0）到 HEAD，读取所有 commit message，生成一份中文 CHANGELOG。按 Conventional Commits 分类：Features、Bug Fixes、Refactors、Docs。每条变更一句话概述+commit hash 链接。"

Claude Code 会调用 `git log v1.2.0..HEAD --oneline`，自动分类归组：

```
## v1.3.0 (2026-07-19)

### Features
- 用户列表新增 Excel 导出功能，支持全量导出和自定义字段 (a1b2c3d)
- 仪表盘新增近 30 天数据趋势图 (e4f5g6h)
- 用户详情页支持批量操作 (i7j8k9l)

### Bug Fixes
- 修复导出按钮在 Safari 下重复触发问题 (m0n1o2p)
- 修复大数据量下分页计算 total 偏移问题 (q3r4s5t)

### Refactors
- 重构分页 Hook，抽离通用逻辑到 usePagination (u6v7w8x)

### Docs
- 补充导出 API 文档和调用示例 (y9z0a1b)
```

CHANGELOG 最让人头疼的不是"写"本身，是"从几十条 commit 里挑出跟用户相关的"。Claude Code 做了这个筛选——你只用在它生成的基础上做微调。

---

## 四、GitHub Issue/PR 中 @claude：让 AI 参与协作

GitHub 上有一个被低估的功能：在 Issue 和 PR 的评论里 `@claude`，Claude Code 会响应。

### 实际用法

**在 Issue 里分析 Bug：**

在 Issue 下评论：

> @claude 分析一下这个 Bug 报告。根据报告里的错误栈，定位到项目里可能相关的代码文件。列出需要检查的文件和可能的原因。

Claude Code 会读取 Issue 内容 + 搜索项目代码，给出分析。

**在 PR 里辅助 Code Review：**

> @claude review 这个 PR 的安全性——有没有 SQL 注入、XSS、敏感信息泄露的风险。

Claude Code 会分析 diff，找出可能的安全问题。

### @claude 的定位：不是替代 Reviewer

`@claude` 做的 Review 是**预审**——找出明显的问题，把人工 Review 从"找问题"变成"确认 AI 标的问题 + 判断方案合理性"。

人工 Review 最浪费时间的不是"这个设计不好"这种高阶判断——是"这个变量没判空吧"、"这个参数校验漏了吧"这种低级错误。`@claude` 把低级错误扫完了，人的精力放在真正需要经验判断的地方。

### 进阶：用 /loop 让 Claude Code 自动值班

以上流程还需要你手动去 PR 或 Issue 里 `@claude`。2026 年 Claude Code 推出的 `/loop` 命令（详见本系列进阶篇）把这个也自动化了——它按固定间隔自己检查 PR 状态：

```bash
/loop 15m 检查 PR #512 有没有新的 review 评论或 CI 失败。有评论就按建议改代码并 push，CI 挂了就诊断修复。有冲突就解决。
```

设好之后，Claude Code 每 15 分钟自动看一眼你的 PR——就像你雇了个值班工程师。reviewer 的每一条评论都会被及时响应，你在 PR 上的响应速度从"半天"变成"15 分钟"。

---

## 五、在 CI/CD 中集成 Claude Code：以代码审查为例

### 基础思路

在 CI 流水线里加入一个 Claude Code 检查环节：

```yaml
# .github/workflows/ai-review.yml
name: Claude Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # 获取完整历史，用于 diff

      - name: Claude Code Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude --print "
          Review the diff between HEAD and origin/main.
          Focus on:
          1. Security issues (SQL injection, XSS, hardcoded secrets)
          2. Missing error handling
          3. Potential performance issues in loops
          4. Violations of the project's coding patterns (check CLAUDE.md)

          Output as a markdown checklist. Only flag real issues, don't nitpick.
          " > ai-review.md

      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('ai-review.md', 'utf8');
            await github.rest.issues.createComment({
              ...context.repo,
              issue_number: context.issue.number,
              body: `## 🤖 Claude Code 代码审查\n\n${review}\n\n---\n*此评论由 CI 中的 Claude Code 自动生成。人工审查仍需进行。*`
            });
```

### 这个 CI 环节不做什么

**1. 不做自动 Merge**

AI 的审查结果是参考，不是权威。它标出的问题，最终要人确认。千万不要设置"AI 审查通过就自动 Merge"——AI 的判断在多数情况下是对的，但少数情况下会误判，而那个少数情况可能就是生产事故。

**2. 不做"最终结论"**

AI 的审查结果是"这里值得你留意"，不是"这里有问题"。它帮助 Reviewer 提高效率，但不替代 Reviewer 的最终判断。

**3. 不检查业务逻辑**

AI 能检查安全漏洞、性能隐患、代码规范。但它不懂你的业务——"这里应该用百分比还是绝对值"这种问题，它回答不了。

---

## 写在最后

这一篇讲的东西——commit、PR、CHANGELOG——在技术圈有个共同的名字：**"胶水工作"**。

不是核心开发，但缺一不可。没人会因为 commit message 写得好被夸，但一定会因为写得太差被吐槽。没人会专门看你的 CHANGELOG，但你的用户会因为它写得清楚而更新得果断。

Claude Code 在这类胶水工作上的价值，是一个你可能没注意到的心理变化：

**过去：写完代码，还要硬着头皮写 commit、PR、CHANGELOG。**
**现在：写完代码，剩下的它来。你只用在它的输出基础上做微调。**

这个变化带来的不只是时间节省。是你**不再对"提 PR"这件事有心理阻力**。不怕 reviewer 看不懂、不怕自己忘了描述关键信息——因为 AI 帮你兜底了。

胶水工作也是工作。让工具做胶水，你用脑子做核心。

---

*Claude Code 实战系列 · GitHub 工作流*
*适用对象：每天要提 PR 的开发者 / 想提升团队协作效率的 Tech Lead / 厌倦了手动写 commit message 的任何人*
*本系列更多文章可在公众号合集「Claude Code 实战」中查看*

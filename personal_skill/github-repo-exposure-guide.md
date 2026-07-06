# GitHub 开源技能仓库曝光推广方案

> 适用场景：CodeBuddy skill 仓库（实用手册/模板类项目）上传到 GitHub 后，如何提升搜索排名和曝光。

---

## 一、GitHub 内部能做的事

### 1. 仓库名就是搜索词

GitHub 搜索优先匹配仓库名和 description。站在用户角度想：他们搜什么能找到你？

| 仓库名建议 | 原因 |
|-----------|------|
| `wechat-article-format-guide` | "wechat article" 是高频搜索 |
| `xiaohongshu-note-format-guide` / `rednote-writing-guide` | 小红书海外用户常用 "rednote" |
| `deai-writer` / `human-writing-guide` | "AI writing" / "human writing" 相关 |

**Description 必须塞关键词**：
`wechat official account article formatting, HTML template, WeChat typesetting guide, 微信公众号排版`

### 2. Topics 标签打满

GitHub 的 Topics 会单独生成 topic 页面（如 `github.com/topics/wechat`），是第二大流量来源。每个 repo 最多打 20 个，打满。

**wx-format-guide 推荐 topics：**
```
wechat, wechat-official-account, html-template, typesetting, markdown-to-html, css-template, article-format, chinese-article, writing-tool, codebuddy-skill
```

**xhs-format-guide 推荐 topics：**
```
xiaohongshu, rednote, social-media-writing, content-creation, note-template, emoji-guide, chinese-marketing, writing-guide, codebuddy-skill
```

**deai-writer 推荐 topics：**
```
ai-writing, writing-style, content-writing, human-writing, writing-checklist, chinese-writing, ai-content, writing-tips, codebuddy-skill
```

打 topics 方法：repo 首页 → 右侧 About 区域 → 齿轮图标 → Topics 输入框。

### 3. 建一个"父仓库"聚合页

单独三个 repo 容易被淹没，建一个聚合 repo 把它们串起来：

```markdown
# codebuddy-writing-skills

一套面向中文内容创作者的 CodeBuddy 写作技能包，覆盖排版、风格、分发全链路。

## 包含的技能

| 技能 | 用途 | 独立仓库 |
|------|------|---------|
| wx-format-guide | 微信公众号HTML排版 | [→ repo](https://github.com/xxx/wx-format-guide) |
| xhs-format-guide | 小红书笔记排版 | [→ repo](https://github.com/xxx/xhs-format-guide) |
| deai-writer | 去AI味写作规范 | [→ repo](https://github.com/xxx/deai-writer) |

## 快速安装

```bash
# 一键安装全部三个技能
git clone https://github.com/xxx/wx-format-guide.git ~/.codebuddy/skills/wx-format-guide
git clone https://github.com/xxx/xhs-format-guide.git ~/.codebuddy/skills/xhs-format-guide
git clone https://github.com/xxx/deai-writer.git ~/.codebuddy/skills/deai-writer
```
```

这个聚合 repo 的 README 是 SEO 入口——名字叫 `codebuddy-writing-skills`，description 里塞 "CodeBuddy skill, Chinese writing, WeChat article, Xiaohongshu, AI writing guide"。

### 4. README 里要有的内容

GitHub 搜索会索引 README 文本，所以 README 要言之有物：

- **顶部放一句话介绍**：This is a XXX guide for XXX. If you XXX, this skill can help you XXX.
- **放实际效果截图**：排版最终效果、对比图（AI 味 vs 去 AI 味）
- **放使用示例**：3 个真实使用场景
- **放安装方法**：2 行命令搞定

### 5. 用中文 + 英文双语 README

GitHub 搜索对中文支持一般，英文 README 能匹配英文关键词：

```
README.md        # 英文主 README
README_CN.md     # 中文详细版
```

README.md 做得简短有力，README_CN.md 放完整内容。

---

## 二、GitHub 外部引流

### 1. 在相关社区埋钩子

| 平台 | 怎么做 |
|------|-------|
| **即刻** | 发一条「我做了一个GitHub repo，专门解决XX问题」，附链接。即刻用户对实用工具 repo 的 star 转化率极高 |
| **知乎** | 回答「公众号怎么排版好看」「如何写出不像AI的文章」类问题，文末放 repo 链接。这类问题流量持续 |
| **V2EX** | 在「分享创造」节点发帖，标题格式：「[分享] 开源了一套 CodeBuddy 写作技能包（公众号排版+去AI味）」。需要正经说明用法和解决的问题 |
| **Twitter/X** | 发 thread：①痛点 → ②做了什么 → ③效果对比 → ④repo 链接。配 before/after 截图 |
| **小红书** | 用你自己的 xhs-format-guide 排版，发笔记：「我把自己三年公众号排版经验写成了一份开源手册」。附 repo 链接（用图片带链接的形式） |
| **GitHub Discussions** | 在 CodeBuddy、shadcn/ui、obsidian 等相近生态的 repo 的 Discussions 里参与讨论，自然提到你的 repo |

### 2. 蹭 GitHub Trending 的条件

- 选一个**工作日早上 9-10 点**发布（中美时区重叠）
- 发布当天通过即刻/V2EX/知乎 集中推广
- 中文项目 Trending 上榜门槛大约 **50-80 star / 24h**

### 3. 发到 Reddit

`r/ChineseLanguage`、`r/WeChat`、`r/writing` 对中文写作工具感兴趣。用英文发帖，展示效果对比截图。

### 4. 用 GitHub Pages 托管 demo 页面

开启 GitHub Pages 做简单 demo：
- **deai-writer**：AI 味原文 vs 去 AI 味后的对比
- **wx-format-guide**：直接渲染排版效果的 HTML 预览
- 页面底部放 "Star on GitHub" 按钮

---

## 三、长期维护

| 策略 | 效果 |
|------|------|
| `CHANGELOG.md` 持续更新 | 证明项目活跃 |
| 公众号文章底部放「本文排版规范已开源」+ GitHub 链接 | 精准流量 |
| 写「如何用这三个 skill 提升写作效率」公众号文章 | 现身说法 |
| Issue / PR 当天回复 | 活跃度信号 |
| skill 的 SKILL.md 底部加 `> 📦 GitHub: https://github.com/xxx/xxx` | 用你 skill 的人自然看到 |

---

## 优先级速查

| 优先级 | 操作 | 耗时 |
|--------|------|------|
| 🔴 立即做 | 3 个 repo 的 description + topics 打满 | 10 分钟 |
| 🔴 立即做 | 建聚合 repo `codebuddy-writing-skills` | 20 分钟 |
| 🟡 本周 | 英文 README + 效果截图 | 1 小时 |
| 🟡 本周 | 即刻/V2EX 发帖引流 | 30 分钟 |
| 🟢 后续 | 知乎回答积累长尾流量 | 持续 |
| 🟢 后续 | 公众号文章底部嵌入 repo 链接 | 每次发文顺手 |

---

## 核心原则

> GitHub 内靠 keywords + topics，GitHub 外靠你已有的内容渠道引流。
> 你的三个 skill 本身就是「写作者的痛点解决方案」，用你已有的公众号和小红书替它们做背书，是最精准的流量。

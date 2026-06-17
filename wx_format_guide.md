# 微信公众号文章排版格式指南

> 适用于 HTML → 微信公众号编辑器复制粘贴的文章格式转换。
> 核心原则：**只用 `<p>` `<span>` `<strong>` `<br>` 四种标签，全内联样式，确保复制后排版不乱。**

---

## 一、整体容器

```html
<body style="font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',Helvetica,Arial,sans-serif;font-size:15px;color:#333;line-height:1.85;max-width:680px;margin:0 auto;background:#fff;padding:20px;">
```

要点：
- `max-width: 680px` — 匹配公众号手机屏宽
- `font-size: 15px` — 正文字号
- `line-height: 1.85` — 行距舒适
- 字体栈覆盖 iOS/Android/Windows 全部平台

---

## 二、标签清单（绝对不用这些）

| ❌ 禁用 | ✅ 替代 |
|---------|---------|
| `<div>` | `<p>` |
| `<table>` `<tr>` `<td>` | 上下堆叠的 `<p>` |
| `linear-gradient` | 纯色 background |
| `box-shadow` | 边框 border |
| `display:flex` | 自然块级排列 |
| `::before` `::after` | 真实文本/emoji |

---

## 三、排版元素速查表

### 3.1 顶部分类标签

```html
<p style="text-align:center;margin-bottom:0;">
  <span style="display:inline-block;background:#f0f0f0;color:#666;font-size:12px;padding:3px 14px;border-radius:12px;">🧠 AI 入门指南</span>
</p>
```

### 3.2 大标题

```html
<p style="font-size:22px;font-weight:800;color:#1a1a2e;text-align:center;margin:12px 0 6px 0;">
  主标题<br>副标题
</p>
```

#### 标题写法公式

**核心原则：先用场景钩子抓注意力，技术名词可以作为搜索锚点放在副标题或后半段。不要只用技术名词当标题——纯术语标题 = 只有搜索的人会点，场景化标题 = 不搜索的人也想点。**

**标题结构建议：**
```
[场景钩子/痛点/反常识] + [技术名词（可选，用于搜索触达）]
```

**黄金三角公式（主钩子部分）：**
```
[具体数字] + [痛苦场景] + [反常识结论]
```

**技术名词出现在标题的策略：**
- ✅ 作为副标题或后半段出现：`「帮我查数据库」，AI 说做不到——打开 MCP 协议后，它真去查了`
- ✅ 场景 + 名词搭配：`Skills 机制实测：同一个需求它写了两次，第二次专业了十倍`
- ❌ 名词单独当标题：~~`MCP 协议：让 AI 接入真实世界`~~
- ❌ 名词开头说教：~~`Automations：让 CodeBuddy 替你定时工作`~~

**好标题 vs 差标题：**

| ❌ 差标题 | ✅ 好标题 |
|----------|----------|
| 别再零散用 AI 了——手把手教你搭一支自己的 AI 团队 | 我一个人管 5 个 AI 干活，效率翻了 3 倍（附完整搭建方案） |
| AI 团队搭好了，但怎么知道它在退步？——长期运维指南 | AI 用了 3 个月突然变笨了？不是你幻觉，是它在退化 |
| 免费 AI 实战：搞定 5 类高频工作，效率翻倍 | 每天被周报、PPT、会议纪要折磨？5 个免费 AI 一键搞定 |
| AI 代码工具入门：一行代码不会写，也能做小工具 | 不会写代码的人，已经开始用 AI 做网站赚钱了 |
| CodeBuddy 是什么？——你的 AI 工作搭档 | Cursor、Copilot、Claude Code 都试过了，为什么我最后选了它？ |
| Skills 机制：给 AI 装上"专业技能包" | 用了三个月才发现一直在「裸奔」——打开这个开关，AI 突然专业了 10 倍 |
| MCP 协议：让 AI 接入真实世界 | 「帮我分析一下数据库」，AI 说做不到——我只多做了这一步，它就真去查了 |
| Automations：让 CodeBuddy 替你定时工作 | 我睡着的时候 AI 在干什么？日报写好了、巡检做完了、公众号排好了 |

**标题检查清单：**
- [ ] 总字数 15-25 字（含标点）
- [ ] 有具体数字或量化结果
- [ ] 戳中了某个具体痛点/场景
- [ ] 技术名词（如有）搭配了场景钩子，不是孤零零作为标题
- [ ] 制造了「认知缺口」（读者想知道答案）

**封面图同步原则：**
- 微信先看到封面再看到标题，封面图 + 标题要搭配
- 用真人/真实场景图，不要通用 AI 机器人图
- 封面图上叠加 1-2 个醒目大字（与标题核心钩子呼应）
- 配色往黄/橙色走，订阅号列表里最跳

### 3.3 副标题 / 描述

```html
<p style="text-align:center;color:#888;font-size:14px;margin-bottom:24px;">
  一句话描述文案
</p>
```

### 3.4 写在前面（蓝色左边框提示框）

```html
<p style="background:#e8f4fd;padding:14px 16px;border-radius:8px;border-left:3px solid #4A90D9;color:#4a5568;font-size:14px;line-height:1.8;">
  📝 <strong style="color:#2b6cb0;">写在前面：</strong>正文内容...
</p>
```

**「写在前面」写法规范（前 100 字决定跳出率）：**
- ❌ 删除所有铺垫和客套话（「AI 时代来了」「最近很多朋友问我」）
- ❌ 不要从背景介绍开始
- ✅ **第一句话直接戳痛点**，用读者自己的语言
- ✅ 用具体场景 + 主体文案，让读者觉得「说的就是我」

> ❌ "随着大模型技术的飞速发展，越来越多的职场人开始使用AI工具..."
> ✅ "你上周写的周报，AI 写得比你好。但你用了 3 个月，发现自己反而更累了——这不对劲。"

### 3.5 目录（彩色标签组）

```html
<p style="text-align:center;margin-bottom:8px;">
  <span style="background:#ebf4ff;color:#2b6cb0;font-size:12px;padding:3px 10px;border-radius:10px;margin:2px;">一、章节名</span>
  <span style="background:#f3ebff;color:#6b46c1;font-size:12px;padding:3px 10px;border-radius:10px;margin:2px;">二、章节名</span>
  ...
</p>
```

### 3.6 分隔线（粗）

```html
<p style="text-align:center;color:#ccc;font-size:12px;margin:16px 0;">━━━━━━━━━━━━━━</p>
```

### 3.7 分隔线（细）

```html
<p style="text-align:center;color:#ccc;font-size:12px;margin:12px 0;">· · ·</p>
```

### 3.8 一级标题（带编号 badge）

```html
<p style="font-size:18px;font-weight:800;color:#1a1a2e;margin:24px 0 12px 0;">
  <span style="color:#fff;background:#4A90D9;font-size:14px;padding:2px 8px;border-radius:6px;margin-right:6px;">1</span>
  章节标题文字
</p>
```

不同章节用蓝紫交替的 badge 背景：
- 奇数章 `#4A90D9`（蓝）
- 偶数章 `#8e44ad`（紫）

### 3.9 二级标题（带 emoji）

```html
<p style="font-size:16px;font-weight:700;color:#1a1a2e;margin:16px 0 8px 0;">📌 标题文字</p>
```

### 3.10 正文段落

```html
<p>普通正文，<strong>加粗强调</strong>，正常文字。</p>
```

### 3.11 引用/示例框（灰色左边框）

```html
<p style="background:#f7f8fa;padding:10px 14px;border-left:3px solid #ccc;color:#555;font-size:14px;">
  引用文字或示例内容...<br><br>多段用 br 分隔
</p>
```

### 3.12 强调结论框（蓝色背景白字）

```html
<p style="background:#4A90D9;color:#fff;padding:14px 16px;border-radius:8px;margin:14px 0;">
  <strong>💡 一句话记住：</strong>核心结论文字
</p>
```

其他颜色变体：
- 紫色 `#8e44ad`

### 3.13 警告/避坑框（红色背景）

```html
<p style="background:#fff5f5;padding:12px 14px;border-radius:8px;border:1px solid #fed7d7;color:#9b2c2c;font-size:14px;">
  ❌ 警告内容<br>
  ❌ 警告内容<br>
  <span style="color:#276749;">✅ 正确做法</span>
</p>
```

### 3.14 提示/建议框（紫色背景）

```html
<p style="background:#f3ebff;padding:12px 14px;border-radius:8px;border:1px solid #d4b8f0;color:#4a3a6e;font-size:14px;margin:12px 0;">
  <strong>💡 关键心态：</strong>内容文字
</p>
```

### 3.15 场景标题条（蓝/紫色底白字）

```html
<p style="font-size:15px;font-weight:700;color:#fff;background:#4A90D9;padding:8px 12px;border-radius:6px;margin:12px 0 0 0;">
  ✉️ 场景 1：标题文字
</p>
```

紫色变体：`background:#8e44ad`

再紧跟痛点和实操段落：
```html
<p style="margin-top:10px;"><strong>痛点：</strong>描述痛点。</p>
<p><strong>实操：</strong>操作步骤。</p>
```

### 3.16 内嵌代码/指令块

```html
<p style="background:#f7f8fa;padding:10px 14px;border-left:3px solid #ccc;color:#555;font-size:14px;">
  "具体指令文字..."
</p>
```

### 3.17 时间对比标签

```html
<p>
  <span style="background:#ebf4ff;color:#2b6cb0;font-size:11px;padding:2px 8px;border-radius:8px;">⏱ 原本 20 分钟</span>
  <span style="background:#f3ebff;color:#6b46c1;font-size:11px;padding:2px 8px;border-radius:8px;">→ 2 分钟搞定</span>
</p>
```

### 3.18 关联信息标签（带边框背景）

```html
<p>
  <span style="background:#ebf4ff;color:#2b6cb0;font-size:13px;padding:6px 10px;border-radius:6px;display:inline-block;margin:2px 0;">
    ✅ <strong>用法A：</strong>"具体指令文字"
  </span>
</p>
```

颜色变体：
- 蓝色 `#ebf4ff` / `#2b6cb0`
- 紫色 `#f3ebff` / `#6b46c1`

### 3.19 工具条目（奖牌 + 信息 + 标签）

```html
<p>
  <span style="background:#ebf4ff;font-size:12px;padding:1px 6px;border-radius:4px;">🥇</span>
  <strong>工具名</strong> —— 一句话描述<br>
  <span style="color:#4A90D9;font-size:12px;">➜ 网址</span>
</p>
```

附加标签：
```html
<span style="background:#ebf4ff;color:#2b6cb0;font-size:11px;padding:1px 6px;border-radius:4px;">💰 免费</span>
<span style="background:#f3ebff;color:#6b46c1;font-size:11px;padding:1px 6px;border-radius:4px;">Plus $20/月</span>
<span style="background:#e8f4fd;color:#4A90D9;font-size:11px;padding:1px 6px;border-radius:4px;">🔍 特色</span>
```

### 3.20 行动号召

```html
<p style="text-align:center;color:#4A90D9;font-weight:700;margin:12px 0;">
  ⚡ 行动号召文字
</p>
```

### 3.21 万能公式（紫色背景白字居中）

```html
<p style="background:#8e44ad;color:#fff;padding:14px 16px;border-radius:8px;text-align:center;margin:12px 0;">
  <strong style="font-size:16px;">🎯 公式标题</strong><br><br>
  <strong style="font-size:18px;">核心公式</strong><br><br>
  <span style="font-size:13px;opacity:0.9;">公式解释文字</span>
</p>
```

### 3.22 前后对比（两个色块上下排列）

```html
<p style="background:#fff5f5;padding:10px 14px;border-radius:6px;color:#c53030;font-size:14px;margin:8px 0;">
  <strong>🔹 以前</strong><br>旧做法1<br>旧做法2
</p>

<p style="background:#f3ebff;padding:10px 14px;border-radius:6px;color:#4a3a6e;font-size:14px;margin:8px 0;">
  <strong>🔹 现在</strong><br>新做法1<br>新做法2
</p>
```

### 3.23 分步骤要点（带编号圆点）

```html
<p><strong><span style="color:#4A90D9;">①</span> 小标题</strong><br>说明文字</p>
<p><strong><span style="color:#8e44ad;">②</span> 小标题</strong><br>说明文字</p>
```

### 3.24 时间计划标签

```html
<p>
  <span style="background:#ebf4ff;color:#2b6cb0;font-size:12px;padding:2px 8px;border-radius:6px;">📅 第 1 周</span>
  <strong>阶段名</strong> —— 具体行动
</p>
```

颜色递进：
- 第1周 蓝 `#ebf4ff` / `#2b6cb0`
- 第2周 紫 `#f3ebff` / `#6b46c1`
- 第3周 蓝 `#ebf4ff` / `#2b6cb0`

### 3.25 工具全家福分类小标题

```html
<p style="font-size:16px;font-weight:700;color:#1a1a2e;margin:16px 0 8px 0;">📌 4.1 分类标题</p>
```

### 3.26 结尾区域

```html
<p style="font-size:18px;font-weight:800;color:#1a1a2e;text-align:center;margin:24px 0 12px 0;">写在最后</p>

<p style="background:#4A90D9;color:#fff;padding:14px 16px;border-radius:8px;text-align:center;margin:14px 0;">
  <strong>🚀 最后行动号召</strong>
</p>
```

结尾 CTA 也可用紫色变体：`background:#8e44ad`

### 3.27 坑位剖析三段式（表现→真相→解法）

适用于踩坑复盘、干货拆解类文章。每个坑位三板斧：

```html
<!-- 坑位标题（带编号 badge） -->
<p style="font-size:18px;font-weight:800;color:#1a1a2e;margin:24px 0 12px 0;">
  <span style="color:#fff;background:#4A90D9;font-size:14px;padding:2px 8px;border-radius:6px;margin-right:6px;">1</span>
  坑位标题
</p>

<!-- 表现：普通正文 -->
<p><strong>表现：</strong>描述现象……</p>

<!-- 真相：蓝色左边框背景框 -->
<p style="background:#e8f4fd;padding:12px 14px;border-left:3px solid #4A90D9;color:#4a5568;font-size:14px;margin:10px 0;">
  <strong style="color:#2b6cb0;">真相：</strong>深层原因分析……
</p>

<!-- 解法：紫色左边框背景框 -->
<p style="background:#f3ebff;padding:12px 14px;border-left:3px solid #8e44ad;color:#4a5568;font-size:14px;margin:10px 0;">
  <strong style="color:#6b46c1;">解法：</strong>具体可操作步骤……
</p>
```

交替 badge 颜色：奇数坑蓝 `#4A90D9`，偶数坑紫 `#8e44ad`。

### 3.28 自查清单（灰色底统一框）

```html
<p style="background:#f7f8fa;padding:14px 16px;border-radius:8px;color:#555;font-size:14px;line-height:2.2;margin:10px 0;">
  <span style="color:#4A90D9;">☐</span> 检查项 1<br>
  <span style="color:#4A90D9;">☐</span> 检查项 2<br>
  <span style="color:#8e44ad;">☐</span> 检查项 3
</p>
```

复选框颜色用蓝紫交替，增强可读节奏。

### 3.29 页脚

```html
<p style="text-align:center;color:#aaa;font-size:12px;margin-top:24px;padding-top:12px;border-top:1px solid #e2e8f0;line-height:2;">
  编写日期：YYYY 年 M 月 D 日<br>适用对象：描述
</p>
```

---

## 四、配色参考

**核心原则：全篇文章只用蓝、紫两色 + 中性灰，避免五颜六色。**

| 用途 | 色值 | 色名 |
|------|------|------|
| **主蓝色**（标题 badge、强调框、关键句） | `#4A90D9` | 蓝 |
| **主紫色**（偶数 badge、变体框、创意模块） | `#8e44ad` | 紫 |
| 标题深色 | `#1a1a2e` | 近黑 |
| 正文灰色 | `#333` | 深灰 |
| 辅助文字 | `#888` / `#aaa` | 中灰/浅灰 |
| 引用/代码区背景 | `#f7f8fa` | 极浅灰 |
| 蓝色浅底 | `#e8f4fd` | 浅蓝 |
| 蓝色标签底 | `#ebf4ff` | 蓝标签 |
| 紫色浅底 | `#f3ebff` | 浅紫 |
| 蓝色深文 | `#2b6cb0` | 深蓝文 |
| 紫色深文 | `#6b46c1` | 深紫文 |
| 红色浅底（仅警告/避坑） | `#fff5f5` | 浅红 |

---

## 五、常用 Emoji 速查

| Emoji | 用途 |
|-------|------|
| 📌 | 要点标记 |
| 📝 | 写在前面的提示 |
| 🎯 | 核心结论/目标 |
| 💡 | 关键洞察 |
| ❌ | 错误/否定 |
| ✅ | 正确/肯定 |
| ⚡ | 紧急行动 |
| 🚀 | 开始/启动 |
| 🔹 | 条目符号 |
| 🥇🥈🥉🏅 | 排名 |
| ✉️📄📚📊🏠 | 场景图标 |
| 📅 | 时间/计划 |
| ⏱ | 时间对比 |
| 💰 | 价格 |
| 🔍 | 搜索/深度 |
| 🎨📊🎵🖼️🎬📝 | 工具类型 |

---

## 六、文章结构模板

### 通用文章结构
```
1. 分类标签（3.1）
2. 大标题（3.2）+ 副标题（3.3）
   ⚠️ 标题必须用黄金三角公式：数字 + 痛点 + 反常识（见 3.2 标题写法公式）
3. 写在前面（3.4）
   ⚠️ 开头 100 字直接戳痛点，不许铺垫（见 3.4 写在前面写法规范）
4. 粗分隔线（3.6）
5. 目录标签（3.5）
6. 粗分隔线（3.6）
7. ─── 正文各章节循环 ───
   a. 一级标题带badge（3.8）
   b. 二级标题（3.9）
   c. 正文 + 引用框（3.11）+ 强调框（3.12）
   d. 粗分隔线/细分隔线（3.6/3.7）
8. 结尾标题（3.26）
9. 结尾正文 + 行动号召
10. 页脚（3.29）
```

### 踩坑复盘类文章结构
```
1. 分类标签（3.1）
2. 大标题（3.2）+ 副标题（3.3）
   ⚠️ 标题必须用黄金三角公式：数字 + 痛点 + 反常识（见 3.2 标题写法公式）
3. 写在前面（3.4）
   ⚠️ 开头直接戳痛点，不许铺垫（见 3.4 写在前面写法规范）
4. 粗分隔线（3.6）
5. ─── 各坑位循环 ───
   a. 坑位标题带badge（3.8）— 蓝紫交替
   b. 表现：正文段落（3.10）
   c. 真相：蓝左边框框（3.27）
   d. 解法：紫左边框框（3.27）
6. 分隔线（3.6）
7. 自查清单（3.28）
8. 结尾标题（3.26）
9. 结尾正文 + 行动号召（蓝/紫底白字）
10. 页脚（3.29）
```

---

## 七、复制方法

1. 在浏览器中打开 HTML 文件
2. **Ctrl+A** 全选页面内容
3. **Ctrl+C** 复制
4. 粘贴到微信公众号编辑器
5. 微调：微信编辑器可能过滤部分背景色，手动补一下关键色块

# 小红书笔记排版格式指南

> 适用于小红书画布笔记 / 图文笔记的排版格式转换。
> 核心原则：**短句分行、emoji 分段、卡片化呈现、口语化表达，适配手机竖屏阅读习惯。**

---

## 一、小红书笔记的特点

与公众号长文不同，小红书笔记讲究：

| 特点 | 说明 |
|------|------|
| **碎片化阅读** | 每段不超过 3 行，读者刷屏速度极快 |
| **视觉节奏** | emoji 不只是装饰，而是排版骨架，承担分隔、强调、导航功能 |
| **朋友感语气** | "姐妹们""我真的会谢""谁懂啊"——像闺蜜聊天，不像老师讲课 |
| **信息密度高** | 字数有限（1000 字左右），每句话都要有用 |
| **钩子标题** | 封面标题决定 80% 的点击率，必须制造好奇心或痛点共鸣 |

---

## 二、封面标题公式

> 封面标题 + 封面图 = 决定笔记生死

### ⚠️ 硬约束：标题 ≤ 20 字符

**小红书标题上限 20 字，emoji 算 1 字符。超了发不出去或被截断。**

```
✅ 14字 / 19字  → 合格
❌ 21字 / 27字  → 必须砍
```

**超标时优先砍掉的部分：**
1. 口号式后缀（「最后一个我最常用」「学会效率翻倍」）
2. 英文术语换中文缩写（「token 传给下一步」→「token 自动传」）
3. 可有可无的修饰词（「这种」「那个」）
4. 冒号后面的解释性文字压缩为一句话

**自查方法：** 写完标题后逐字念一遍，超过 20 就动刀，不要有侥幸心理。

### 常用标题公式

| 公式 | 模板 | 示例 |
|------|------|------|
| **痛点 + 解法** | [痛点]？试试[解法] | 测试用例写不完？让 AI 帮你写 |
| **反常识** | 别再[常见做法]了！ | 别再手写测试报告了！AI 3 秒出 |
| **身份 + 结果** | [身份]必看：[结果] | 测试人必看：用 AI 把 bug 率降了 70% |
| **数字钩子** | [数字]个[领域]技巧 | 5 个 AI 测试工具，效率翻倍 |
| **悬念** | 用了[工具]才知道…… | 用了 AI 写测试才知道，以前都在浪费时间 |

### 标题区 emoji 常用

🔥 💡 🚀 ⚡ 🎯 💪 🧠 ✨ 🔥 🔑 📌

---

## 三、正文排版元素速查表

> 小红书正文以 **纯文本 + emoji** 为主，不写 HTML。以下模板给出的是**排版结构**，最终在小红书编辑器中手动排版。

### 3.1 开头钩子（前 2 行决定是否被读完）

```
家人们谁懂啊😭 以前写接口测试，一个用例调半天……
直到我发现用 AI 生成测试用例，直接打开了新世界的大门👇
```

要点：
- 第一句必须是痛点共鸣或好奇心钩子
- 用"家人们/姐妹们/打工人"开头拉近距离
- 必须带至少 1 个 emoji

### 3.2 内容预告（告诉读者往下看有什么）

```
📌 今天分享的内容：
✅ AI 测试工具推荐
✅ 实战 prompt 模板
✅ 避坑经验总结
```

要点：
- 用 ✅ / ☑️ 列举，给读者预期
- 3-5 条为宜

### 3.3 分段标题（emoji + 短标题）

```
━━━━━━━━━━━━━━━━━━
🤖 一、为什么要用 AI 做测试
━━━━━━━━━━━━━━━━━━

🧰 二、必备工具清单

📝 三、实战 Prompt 模板

⚠️ 四、那些年我踩过的坑

💡 五、总结一句话
```

要点：
- 每个分段用 emoji 开头
- 标题不超过 15 个字
- 用分隔线或空行隔开每个板块

### 3.4 正文段落

```
以前写一个接口的测试用例，从设计到写完，少说半小时😮‍💨

现在用 AI，把接口文档贴进去，10 秒出一套用例，覆盖正常/异常/边界场景。

关键是质量还不差，改改就能直接用👌
```

要点：
- 每段 1-3 行，多分段
- 行与行之间空一行
- 口语化，"😮‍💨""👌"这类表情拉近距离
- 不要大段文字，手机上看会窒息

### 3.5 要点列表（数字 + emoji）

```
1️⃣ 第一步：准备接口文档
    把 Swagger 文档导出或直接复制接口说明

2️⃣ 第二步：写 Prompt
    告诉 AI 你要测什么、关注什么场景

3️⃣ 第三步：Review & 微调
    AI 生成的用例过一遍，补充业务逻辑
```

变体——场景式：

```
🔹 场景一：接口测试
   → 把接口文档扔给 AI，自动生成用例

🔹 场景二：UI 自动化
   → 描述页面操作流程，AI 写 Selenium 脚本

🔹 场景三：性能测试
   → 给出压测目标，AI 生成 JMeter 脚本
```

### 3.6 对比卡片（前后对比）

```
❌ 以前：
手动写测试用例 → 查接口文档 → 设计场景 → 写脚本 → 调试 → 半天没了

✅ 现在：
贴接口文档 → AI 生成用例 → 微调 → 10 分钟搞定
```

要点：
- 用 ❌/✅ 标记前后
- 排版简洁，一目了然

### 3.7 Prompt 模板 / 代码展示

> ⚠️ **小红书不支持代码块（```）和表格（|）**。不要用 Markdown 代码块，会被当作普通文字显示，完全失去排版效果。

**方案 A：截图法（最推荐）**
把代码/Prompt 截图作为配图放进图片轮播，正文用文字描述。

**方案 B：引用块法**
用小红书的"引用"样式包裹短代码（注意：长行会在手机上折行）：
```
📋 Prompt 模板：

你是一个资深测试工程师
请根据以下接口文档
生成完整的测试用例
覆盖正常/异常/边界场景

接口文档：[粘贴文档]
```

**方案 C：描述法（最保险）**
不贴代码本身，改为描述代码做了什么事：
```
📋 Prompt 模板核心要点：

🔹 角色设定：资深测试工程师
🔹 输入：接口文档
🔹 输出要求：正常场景 + 异常场景 + 边界场景
🔹 异常覆盖：参数缺失、类型错误
🔹 边界覆盖：最大值、最小值、空值
```

要点：
- 代码优先用截图替代
- 必须文字展示时，用"引用"样式 + 尽量短行
- 复杂代码坚决不贴原文，改用描述式

### 3.8 工具推荐卡片

```
🛠 推荐工具：

🥇 Postman + AI 插件
   → 接口测试神器，AI 自动生成测试脚本
   → 💰 免费额度够用

🥈 TestGPT
   → 专为测试设计的 AI，支持用例生成 + 代码生成
   → 💰 个人版 $15/月

🥉 Cursor + 自定义 Prompt
   → 最强 AI 编码助手，测试脚本一键生成
   → 💰 免费版可用
```

要点：
- 🥇🥈🥉 做排名
- 一行工具名 + 一行说明
- 💰 标注价格

### 3.9 避坑提示

```
⚠️ 注意避坑！

坑 1：别把整个项目代码喂给 AI
→ AI 会混乱，一次只给相关的接口/模块

坑 2：AI 生成的用例要跑一遍
→ 参数名、返回值类型可能会有偏差

坑 3：敏感数据要脱敏
→ 不要把生产环境的真实数据贴进去！
```

### 3.10 核心总结 / 一句话记住

```
🎯 一句话记住：

AI 不是替代测试，是让测试从"体力活"变成"脑力活"。
你用 AI 省下来的时间，可以用来思考更深层的测试策略。
```

### 3.11 互动引导（评论区钩子）

```
💬 你现在用 AI 辅助测试了吗？用的是哪个工具？
评论区聊聊，一起交流～

觉得有用的话，⭐ 收藏不迷路，下次用到直接翻！
```

### 3.12 结尾标签（话题标签）

```
#AI测试 #软件测试 #测试工程师 #自动化测试 #AI工具 #效率提升 #职场技能 #测试用例
```

要点：
- 5-10 个标签
- 大话题 + 小话题搭配
- 大话题（如 #AI测试）提高曝光
- 小话题（如 #测试用例）提高精准度

---

## 四、小红书字数与排版参数

| 参数 | 建议值 |
|------|--------|
| 标题字数 | 20 字以内 |
| 正文字数（上限） | 1000 字（小红书硬上限，超了发不出去） |
| 专业知识分享 | 800-900 字（干货多拉满，信息密度要高） |
| 普通话题/痛点共鸣 | 600-700 字（轻快节奏，刷完不累） |
| 分段数 | 5-8 个板块 |
| 每段行数 | 1-3 行 |
| emoji 密度 | 每 2-3 句至少 1 个 |
| 话题标签 | 5-10 个 |

---

## 五、emoji 速查表（AI/测试相关）

### 情感/语气

| Emoji | 用途 |
|-------|------|
| 😭😮‍💨😤 | 表达痛点/以前的痛苦 |
| 🤩😍✨🔥 | 表达惊喜/好用 |
| 👌💪👍 | 表达认可/鼓励 |
| 🤔🧐 | 引发思考 |
| ⚠️🚨 | 警告/注意 |

### 功能标记

| Emoji | 用途 |
|-------|------|
| 📌 | 重点标记 |
| 📝 | 笔记/记录 |
| 📋 | 模板/清单 |
| 🎯 | 目标/核心结论 |
| 💡 | 技巧/灵感 |
| 🔑 | 关键点 |
| ⚡ | 快速/效率 |
| 🚀 | 起飞/效率提升 |
| 🧠 | AI/智能 |
| 🛠 | 工具推荐 |
| 🔹 | 条目标记 |
| ✅ | 正确/清单 |
| ❌ | 错误/不推荐 |
| 🆚 | 对比 |
| ⭐ | 收藏/重点 |
| 💰 | 价格/成本 |
| 📊 | 数据/统计 |
| 🔍 | 查找/探索 |

### AI/技术专用

| Emoji | 用途 |
|-------|------|
| 🤖 | AI/机器人/自动化 |
| 🧪 | 测试/实验 |
| 🐛 | Bug/缺陷 |
| 🔧 | 修复/工具 |
| 🖥 | 电脑/开发 |
| 📱 | 手机/移动端 |
| 🌐 | 网络/API |
| ⚙️ | 配置/设置 |
| 📦 | 打包/部署 |
| 🔄 | 流程/迭代 |
| 🧩 | 模块/组件 |

---

## 六、AI + 测试 话题标签库

### 大流量标签（提高曝光）

```
#AI测试 #软件测试 #自动化测试 #AI工具 #人工智能 #测试工程师 #程序员 #效率提升
```

### 精准标签（吸引目标读者）

```
#测试用例 #接口测试 #性能测试 #单元测试 #测试开发 #质量保障 #Selenium #Postman
```

### 小红书特色标签

```
#打工人 #职场干货 #效率工具 #摸鱼技巧 #职场技能 #自我提升
```

---

## 七、笔记结构模板

### 工具推荐类（最常见）

```
[钩子开头：痛点共鸣，1-3 句]

[内容预告：✅ 清单式，3 条]

━━━━━━━━━━━━━━━━━━
🔹 工具一
[工具名 + 一句话定位 + 核心功能 + 价格]

🔹 工具二
[同上]

🔹 工具三
[同上]
━━━━━━━━━━━━━━━━━━

[总结 + 个人使用感受]

[互动引导 + 收藏引导]

[话题标签 × 8]
```

### 教程/实战类

```
[钩子开头：场景带入]

📌 今天手把手教你……

━━━━━━━━━━━━━━━━━━
1️⃣ 第一步：[操作]
2️⃣ 第二步：[操作]
3️⃣ 第三步：[操作]
━━━━━━━━━━━━━━━━━━

📋 附：Prompt 模板

💡 关键技巧：
[1-2 个进阶技巧]

[总结]

[互动引导]

[话题标签]
```

### 踩坑复盘类

```
[钩子开头：踩坑故事]

⚠️ [坑位 1]
   ❌ 错误做法 → 后果
   ✅ 正确姿势

⚠️ [坑位 2]
   ❌ 错误做法 → 后果
   ✅ 正确姿势

⚠️ [坑位 3]
   ❌ 错误做法 → 后果
   ✅ 正确姿势

🎯 核心教训：[一句话总结]

[互动：你踩过哪个坑？]

[话题标签]
```

### 认知/观点类

```
[钩子开头：反常识观点]

🤔 为什么[常见做法]其实是错的？

[展开论述，2-3 段，每段配一个 emoji 小标题]

📊 数据/事实支撑：
[如果有数据，用 emoji 标出]

🎯 一句话记住：
[核心观点]

💬 你怎么看？
[互动引导]

[话题标签]
```

---

## 八、发布 Checklist

- [ ] **标题 ≤ 20 字符（硬约束，emoji 算 1 字符）？超标必须砍**
- [ ] 开头前 2 句有共鸣感？
- [ ] emoji 密度够（不能一大段纯文字）？
- [ ] 分段清晰，每段不超过 3 行，每行不超过 20 字？
- [ ] 口语化，没有"论文腔"？
- [ ] **没有代码块（```）？代码已截图或改为描述式？**
- [ ] **没有表格（|）？表格已改为 ✅/❌ 对比或列表？**
- [ ] **没有超长行内代码（>15 字符）？长代码已改描述？**
- [ ] **分隔线不超过 3 条？没出现智能引号、半角符号等特殊字符？**
- [ ] 有互动引导（提问 + 收藏引导）？
- [ ] 话题标签 5-10 个，大小搭配？
- [ ] 封面图是否配合标题有视觉冲击力？
- [ ] 有实质性内容（不是纯鸡汤）？

---

## 九、小红书 vs 公众号 写作差异速查

| 维度 | 公众号 | 小红书 |
|------|--------|--------|
| 字数 | 2000-5000 字 | 600-1000 字 |
| 语气 | 干货/专业/体系化 | 朋友聊天/口语化/亲切 |
| 段落 | 可以较长 | 1-3 行必换段 |
| emoji | 点缀装饰 | 排版主力 |
| 标题 | 信息量标题 | 钩子/好奇心标题 |
| 结构 | 章节目录式 | 卡片堆叠式 |
| 结尾 | 下篇预告 | ⭐ 收藏 + 互动提问 |
| 配图 | 截图/示意图为主 | 高颜值封面 + 配图 |
| 受众心态 | "我来学习" | "我来刷内容" |
| **代码** | Markdown 代码块/行内代码 | **不支持**，需截图或描述替代 |
| **表格** | Markdown 表格 | **不支持**，需列表/对比卡片替代 |

---

## 十、小红书不支持的元素 & 替换方案

> ⚠️ 小红书正文只支持**纯文本 + emoji**。以下元素均不支持，必须用替代方案。

### 10.1 代码块（```）

**问题**：Markdown 的 ``` 包裹的代码块在小红书上会被当作普通文字，失去等宽和区块效果，整段坍缩成一坨。

**替换方案（优先级从高到低）：**

🔹 **方案A：截图放入图片轮播**
效果最好，完全还原代码排版。将代码截图作为配图之一。

🔹 **方案B：描述式改写**
不贴原文，改为用自然语言描述代码逻辑：
```
❌ 原文：
def login(user, pwd):
    resp = post("/api/auth", body)
    assert resp.code == 200

✅ 改写：
🔸 定义 login 函数，接收用户名和密码
🔸 往 /api/auth 发 POST 请求
🔸 断言返回的 code 等于 200
```

🔹 **方案C：极短行引用块**
只适用于 1-3 行、每行不超过 15 字符的代码片段。

### 10.2 表格（|）

**问题**：Markdown 表格在小红书上完全不渲染，竖线和对齐全部失效。

**替换方案：**

🔹 **方案A：✅/❌ 对比卡片**
```
❌ 命令式写法
→ 30+ 行代码，改一处崩全局

✅ 声明式写法
→ 10 行配置，改一行全搞定
```

🔹 **方案B：emoji 列表对照**
```
📝 写新用例
🔸 命令式：30+ 行
🔸 声明式：10 行

📝 加字段
🔸 命令式：改 N 个文件
🔸 声明式：改 1 个配置
```

🔹 **方案C：截图**
数据量大、对比复杂时直接截图放入配图。

### 10.3 行内代码（`code`）

**问题**：反引号包裹的行内代码在小红书上**能显示但无等宽效果**，超过 ~20 字符会在手机上强制换行，导致可读性崩塌。

**规则**：
- ✅ 短术语（≤15 字符）：可以直接用，如 `API`、`pytest`
- ❌ 长语句（>15 字符）：坚决不贴，改为描述
- ❌ 整行代码放在行内代码里：绝对禁止

```
❌ `assert resp.json()["data"]["user_name"] == "张三"`
    → 手机上拆成3行，完全没法看

✅ 断言 user_name 字段的值等于"张三"
    → 一行搞定，清晰可读
```

### 10.4 分隔线过长

**问题**：`━━━━━━━━━━━━━━━━━━` 这种全宽分隔线在小红书窄屏上会被截断，显示效果诡异。

**替换方案**：
- 用 `---`（短横线）
- 或用逗号/句号 + 空行做自然分隔
- 全文不超过 3 条分隔线

### 10.5 单行字数上限

**实测结论**：小红书手机端一行约容纳 **18-22 个中文字符**（英文字符约 30-35 个）。

**规则**：
- 中文行：不超过 20 字换行
- 中英混排：以中文等宽估算，不超过 25 个等效字符
- 宁可多断行，不要让系统帮你断

```
❌ 一个字段改了要改所有地方你要在所有文件里大海捞针
    → 系统断行位置不可控

✅ 一个字段改了
✅ 要改所有地方
✅ 在所有文件里大海捞针
    → 每行都在你掌控中
```

---

## 十一、HTML 卡片生成规范（画布笔记专用）

> 用 HTML 生成小红书画布笔记（图片轮播），截图为 1080×1440 的 PNG 发布。
> 以下为固定规范，每次生成时严格遵守。

### 11.1 卡片尺寸

| 参数 | 值 |
|------|-----|
| 宽度 | 1080px |
| 高度 | 1440px |
| 比例 | 3:4 |
| 圆角 | 24px |
| 字体 | Noto Sans SC（Google Fonts CDN） |
| 输出格式 | 2x 高清 PNG（html2canvas, scale: 2） |

### 11.2 配色方案（两个方案）

> 两个配色方案，生成新卡片时直接指定使用哪个方案。
> 触发语：说「用 Tech Indigo 方案」或「用 Sketch Cream 方案」即可。

---

#### 方案1：Tech Indigo（科技靛蓝）

冷调蓝紫渐变，偏理性/技术感。适合：技术科普、框架对比、底层原理类内容。

| 角色 | 颜色 | 用途 |
|------|------|------|
| 页面背景 | `#e8ecf1` | body |
| 封面渐变 | `linear-gradient(150deg, #dbeafe → #818cf8 → #6366f1)` | card-cover |
| 内容卡底色 | `#fafafd` | card-content |
| 收尾卡渐变 | `linear-gradient(150deg, #eef2ff → #c7d2fe)` | card-closing |
| 标题色 | `#1e1b4b` | h1, h2 |
| 重点色 | `#4338ca` / `#6366f1` | 标签、边框高亮、小标题 |
| 错误/警示 | `#dc2626` + `#fef2f2` 底 | 痛点、对比左边 |
| 成功/方案 | `#059669` + `#ecfdf5` 底 | 解法、对比右边 |
| 中性卡片 | `#ffffff` | 白色卡片、表格单元格 |
| 边框 | `#e0e7ff` / `#c7d2fe` | 卡片边框 |
| 弱文本 | `#4b5563` / `#9ca3af` | 描述文字 |

**排版特征**：
- 封面：全屏渐变 + 半透白标签 + 大字
- 内容：左蓝竖线标记标题 `.section-title`（`border-left: 4px solid #6366f1`）
- 卡片：圆角 12-14px，纯白底+淡阴影
- 对比：红底左侧 vs 绿底右侧
- 按钮：`#6366f1` 科技蓝

**历史使用**：
| 文章 | 文件 |
|------|------|
| 接口测试永远写不完 | `published/card-01-style-tech-blue.html` |
| 换了3个测试框架 | `published/card-02-style-dark-warm.html` |
| 手写断言写到吐 | `published/card-03-style-fresh-green.html` |

---

#### 方案2：Sketch Cream（手绘奶油）

暖调奶油/杏仁/薄荷绿，偏亲切/手绘感。适合：入门教程、工具推荐、实操干货类内容。

| 角色 | 颜色 | 用途 |
|------|------|------|
| 页面背景 | `#EDE4D3`（杏仁米） | body |
| 主奶油底 | `#FFFBF0` | `.warm-bg` 所有卡片底色 |
| 纸纹叠加 | `radial-gradient(orange+tint, green+tint)` | `.paper-texture` |
| 暖棕文字 | `#3D3021` | 标题、主要文字 |
| 暖灰文字 | `#7A6B55` | 描述、次要文字 |
| 封面标签 | `#FEF5E8` + border `#F5B971`（杏橙） | `.cover-tag` |
| 浅杏底 | `#FEF8F0` + border `#F5D5B8` | 内容小卡片 |
| 橙色面板 | `#FEF0E1` + border `#F5B971` | 对比左侧/痛点 `.cp-bad` |
| 薄荷绿面板 | `#E8F8ED` + border `#81C995` | 对比右侧/解法 `.cp-good` |
| 珊瑚重点 | `#E8856B` | 高亮文字、图标、下划线 |
| 红色标记 | `#FFE0D6` 底 + `#E57373` 字 | ✕ 圆形标记 `.mk-x` |
| 绿色标记 | `#D4EDDA` 底 + `#43A047` 字 | ✓ 圆形标记 `.mk-ok` |
| 问题气泡 | `#FEF5E8` + border `#E8856B` | `.bubble-question` |
| 预览框 | `#E8F8ED` + border `#81C995` | `.preview-box` |
| 工具栏按钮 | `#5C4033`（深棕） | `.toolbar button` |
| 装饰星星 | `#5C4033` opacity 0.15 | `.doodle-star` |

**核心原则**：
- **禁止纯白 `#FFF` / `#ffffff`**：所有白色底必须替换为暖色调
- 卡片底色统一用 `#FEF5E8`（封面级）或 `#FEF8F0`（内容级）
- 边框用暖色：杏橙 `#F5B971` / 淡橙 `#F5D5B8` / 薄荷绿 `#81C995`
- 阴影用半透明暖棕 `rgba(92,64,51,0.0x)`

**排版特征**：
- 封面：奶油底 + 纸纹 + ✦ 四角散落 + 圆形珊瑚高亮下划线
- 内容：章节标题用薄荷绿半透底划线
- 卡片：手绘圆角 `border-radius: 255px 15px 225px 15px / 15px 225px 15px 255px`（可选）
- 对比：橙色块 vs 绿色块 + 圆形 ✕/✓ 标记
- 结尾：气泡提问 + 尾巴三角 + 预览框

**历史使用**：
| 文章 | 文件 |
|------|------|
| 9-18 全部第2章 | `ch2-yaml-zero-code/*/xx-cards.html` |

---

#### 方案切换速查

| 元素 | Tech Indigo（方案1） | Sketch Cream（方案2） |
|------|---------------------|----------------------|
| body | `#e8ecf1` | `#EDE4D3` |
| 卡片底色 | `#fafafd` | `#FFFBF0` |
| 纯白卡片 | `#ffffff` | `#FEF8F0` |
| 封面渐变 | 蓝紫渐变 | 纸纹叠加 |
| 标题色 | `#1e1b4b` | `#3D3021` |
| 重点色 | `#6366f1` | `#E8856B` |
| 错误/痛点 | `#fef2f2` + `#dc2626` | `#FEF0E1` + `#E57373` |
| 成功/解法 | `#ecfdf5` + `#059669` | `#E8F8ED` + `#43A047` |
| 按钮 | `#6366f1` | `#5C4033` |

### 11.3 卡片结构

每篇文章生成 4-5 张卡片：

| 序号 | 类型 | 用途 |
|------|------|------|
| 1 | 封面卡 `card-cover` | 标题 + 副标题 + 标签，居中大字 |
| 2-N | 内容卡 `card-content` | section 分区，标题用左边框装饰 |
| N+1 | 收尾卡 `card-closing` | CTA 互动引导 + 话题标签 |

### 11.4 封面卡字号规范

> 封面是小红书的"第一眼"，缩略图模式下主标题必须足够大才能看清。
> 以下为覆盖面卡片的 CSS 固定值，每次生成严格遵守。

| 元素 | 属性 | 值 |
|------|------|-----|
| 主标题 `h1` | font-size / font-weight / line-height | **88px** / 900 / 1.25 |
| 副标题 `.subtitle` | font-size / line-height | **38px** / 1.5 |
| 标签 `.tag` | font-size / padding / border-radius | **36px** / 12px 32px / 28px |
| 卡片内边距 | padding | **48px 56px** |
| 水印 `.watermark` | 位置 | bottom: 36px, right: 56px |

**CSS 参考**：
```css
.card-cover {
  padding: 48px 56px;
  /* 渐变等其他属性不变 */
}
.card-cover .tag {
  font-size: 36px;
  padding: 12px 32px;
  border-radius: 28px;
  margin-bottom: 44px;
}
.card-cover h1 {
  font-size: 88px;
  font-weight: 900;
  line-height: 1.25;
  margin-bottom: 24px;
}
.card-cover .subtitle {
  font-size: 38px;
  line-height: 1.5;
}
```

> ⚠️ 主标题 88px 是在 1080px 宽卡片上的尺寸。主标题通常占卡片宽度的 60-70%，确保在小红书信息流缩略图中仍可辨识。

### 11.5 内容卡排版铁律

> **核心原则：整张卡上下均匀分布，禁止上半密集下半空。**

```css
.card-content {
  padding: 60px 72px 60px;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;  /* ← 关键：均匀撑满 */
}

.card-content .section {
  margin-bottom: 0;  /* space-evenly 自动处理间距 */
}
```

**布局模式**：
- 内容少时（1-2 个 section）：加大 padding，内容居中
- 内容多时（3+ 个 section）：space-evenly 自动分配间距
- section 内元素紧凑排列，section 之间均匀拉开

### 11.6 下载按钮（必须）

> **每次生成的 HTML 必须包含下载功能。**

**HTML 结构**：
```html
<!-- 顶部工具栏 -->
<div class="toolbar">
  <button onclick="downloadAll()">📥 一键下载全部卡片</button>
</div>

<!-- 脚本：需引入 html2canvas CDN -->
<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
<script>
  const ARTICLE = '文章名称';
  document.querySelectorAll('.card').forEach((card, i) => { /* ... */ });
  async function downloadAll() { /* ... */ }
</script>
```

**按钮样式**：
```css
.dl-btn {
  position: absolute; top: 20px; right: 20px; z-index: 10;
  background: rgba(0,0,0,0.35); color: #fff;
  padding: 10px 20px; border-radius: 20px;
  font-size: 22px; cursor: pointer;
  backdrop-filter: blur(4px);
}
```

### 11.7 文件命名规则

下载文件名格式：`文章名-序号.png`

```
✅ 接口测试永远写不完-1.png
✅ 换了3个测试框架-3.png
✅ 手写断言写到吐-5.png

❌ testkid-01.png       （无文章名，无法区分）
❌ card1.png            （无文章名）
```

### 11.8 水印规范

所有卡片右下角统一水印：`@Testkid`

| 卡片类型 | 水印格式 |
|----------|----------|
| 封面 | `@Testkid · 2026` |
| 内容卡 | `@Testkid` |
| 收尾卡 | `@Testkid · 2026` |

```css
.card-cover .watermark  { color: rgba(30,27,75,0.2); }
.card-content .watermark { color: rgba(0,0,0,0.1); }
.card-closing .watermark { color: rgba(0,0,0,0.12); }
```

### 11.9 完整 HTML 模板骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[文章标题] · 小红书卡片</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&display=swap" rel="stylesheet">
<style>
  *,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
  body{background:#e8ecf1;padding:24px;font-family:'Noto Sans SC',sans-serif}
  .cards{display:flex;flex-direction:column;gap:16px;max-width:1080px;margin:0 auto}
  .card{width:1080px;height:1440px;border-radius:24px;overflow:hidden;position:relative;flex-shrink:0;box-shadow:0 4px 24px rgba(0,0,0,0.08)}
  /* 封面卡 — 背景见 11.2 配色方案 */
  .card-cover{display:flex;flex-direction:column;justify-content:center;align-items:center;padding:48px 56px;text-align:center}
  /* 方案1 封面：background:linear-gradient(150deg,#dbeafe,#bfdbfe,#a5b4fc,#818cf8,#6366f1) */
  /* 方案2 封面：background:#FFFBF0 + .paper-texture 纸纹叠加 */
  /* 内容卡 — 背景见 11.2 配色方案 */
  .card-content{padding:60px 72px 60px;display:flex;flex-direction:column;position:relative;justify-content:space-evenly}
  /* 方案1 内容：background:#fafafd */
  /* 方案2 内容：background:#FFFBF0 + .paper-texture */
  /* CTA卡 — 背景见 11.2 配色方案 */
  .card-closing{display:flex;flex-direction:column;justify-content:center;align-items:center;padding:64px 72px;text-align:center;position:relative}
  /* 方案1 CTA：background:linear-gradient(150deg,#eef2ff,#e0e7ff,#c7d2fe) */
  /* 方案2 CTA：background:#FFFBF0 + .paper-texture */
  /* 下载按钮 */
  .dl-btn{position:absolute;top:20px;right:20px;z-index:10;background:rgba(0,0,0,0.35);color:#fff;border:none;padding:10px 20px;border-radius:20px;font-size:22px;cursor:pointer;font-family:'Noto Sans SC',sans-serif}
  .toolbar{position:sticky;top:8px;z-index:100;max-width:1080px;margin:0 auto 12px;display:flex;gap:12px;justify-content:center}
  .toolbar button{background:#6366f1;color:#fff;border:none;padding:12px 32px;border-radius:24px;font-size:22px;font-weight:700;cursor:pointer;font-family:'Noto Sans SC',sans-serif}
  /* 方案2 工具栏按钮：background:#5C4033 */
  /* ... 具体内容样式按需添加 ... */
</style>
</head>
<body>
<div class="toolbar">
  <button onclick="downloadAll()">📥 一键下载全部卡片</button>
</div>
<div class="cards">
  <!-- 卡片区域 -->
</div>
<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
<script>
  const ARTICLE = '[文章标题]';
  document.querySelectorAll('.card').forEach((card, i) => {
    const btn = document.createElement('button');
    btn.className = 'dl-btn';
    btn.textContent = '📥 下载';
    btn.setAttribute('data-dl-btn', 'true');
    btn.onclick = async (e) => {
      e.stopPropagation();
      btn.style.display = 'none';
      const canvas = await html2canvas(card, { scale: 2, useCORS: true, backgroundColor: null });
      btn.style.display = '';
      const link = document.createElement('a');
      link.download = `${ARTICLE}-${i + 1}.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
    };
    card.appendChild(btn);
  });
  async function downloadAll() {
    const cards = document.querySelectorAll('.card');
    for (let i = 0; i < cards.length; i++) {
      const btn = cards[i].querySelector('[data-dl-btn]');
      if (btn) btn.style.display = 'none';
      const canvas = await html2canvas(cards[i], { scale: 2, useCORS: true, backgroundColor: null });
      if (btn) btn.style.display = '';
      const link = document.createElement('a');
      link.download = `${ARTICLE}-${i + 1}.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
      await new Promise(r => setTimeout(r, 600));
    }
  }
</script>
</body>
</html>
```

### 11.10 生成 Checklist

- [ ] 卡片尺寸 1080×1440、24px 圆角
- [ ] 配色选定方案1或方案2，未混用两个方案的色值
- [ ] 内容卡使用 `justify-content: space-evenly`
- [ ] 内容上下均匀分布，无上半密集下半空白
- [ ] 顶部有「📥 一键下载全部卡片」工具栏按钮
- [ ] 每张卡右上角有独立下载按钮
- [ ] 下载文件名格式：`文章名-序号.png`
- [ ] 所有卡片右下角水印 `@Testkid`
- [ ] html2canvas scale:2 输出 2x 高清
- [ ] Noto Sans SC 字体 CDN 已引入

### 11.11 内容卡组件库（可复用排版组件）

> **标杆**：`ai_test_xhs/published/card-05-test-report.html` 排版最佳。
> 它好在不靠"一张大表格/同款列表"撑场，而是**每卡组件不同、每卡用金句盒收尾、序号角标克制**。
> 以下组件为 Tech Indigo（方案1）下的标准实现。生成内容卡时，**按内容选组件，禁止整篇内容卡都用同一款列表**。

#### 11.11.1 序号角标 `.num`（每卡必须有，右上角小号淡标）

> ⚠️ **禁止**用居中 200-300px 巨型半透数字当背景（喧宾夺主）。序号应是"角落里的页码感"。

| 属性 | 值 |
|------|-----|
| 字号 / 字重 | 72px / 900 |
| 颜色 | `rgba(99,102,241,0.1)`（淡靛蓝） |
| 位置 | `position:absolute; top:40px; right:60px;` |
| 行高 | 1（不占行） |

#### 11.11.2 对话盒 `.dialog-box`（讲翻车 / 故事 / 场景）

分三段，**铺陈 → 翻车 → 顿悟**，自带层次，不要一长条 `<br>` 堆。

```css
.dialog-box { background:#f0f4ff; padding:28px 32px; border-radius:14px; }
.dialog-box .you-say { font-size:23px; color:#6b7280; line-height:1.8; }      /* 铺垫：灰字 */
.dialog-box .boss-say {                                                        /* 翻车：白底+红左线 */
  background:#fff; border-left:4px solid #dc2626;
  padding:18px 24px; border-radius:10px;
  font-size:26px; color:#dc2626; font-weight:700; line-height:1.6;
}
.dialog-box .aha {                                                             /* 顿悟：虚线分隔+强调 */
  margin-top:18px; padding-top:16px; border-top:1px dashed #c7d2fe;
  font-size:24px; color:#4338ca; text-align:center; line-height:1.8; font-weight:700;
}
```

#### 11.11.3 左右对比 `.vs-row`（A vs B / 你给的 vs 领导看到的）

```css
.vs-row { display:flex; gap:18px; }
.vs-you  { flex:1; background:#fef2f2; border:1.5px solid #fecaca; border-radius:14px; padding:24px 22px; text-align:center; }  /* 左：红=痛点 */
.vs-boss { flex:1; background:#eff6ff; border:1.5px solid #bfdbfe; border-radius:14px; padding:24px 22px; text-align:center; }  /* 右：蓝=解法 */
.vs-label { font-size:22px; color:#dc2626; font-weight:700; margin-bottom:12px; }
.vs-boss .vs-label { color:#2563eb; }
.vs-content { font-size:22px; color:#4b5563; line-height:1.8; }
```

#### 11.11.4 图标网格 `.boss-want`（2×2 罗列要素）

```css
.boss-want { display:flex; flex-wrap:wrap; gap:12px; }
.want-item { flex:0 0 calc(50% - 6px); background:#fff; border:1.5px solid #e0e7ff;
  border-radius:12px; padding:20px 24px; display:flex; align-items:flex-start; gap:14px; box-shadow:0 2px 6px rgba(0,0,0,0.03); }
.wi-icon { font-size:32px; flex-shrink:0; }
.wi-body { font-size:21px; color:#1e1b4b; line-height:1.6; }
.wi-body strong { display:block; font-size:22px; color:#4338ca; margin-bottom:4px; }
```

#### 11.11.5 多列卡片 `.allure-cols` / `.three-row`（3 列并列）

```css
.allure-cols { display:flex; gap:14px; }
.allure-col { flex:1; background:#ffffff; border:1.5px solid #e0e7ff; border-radius:14px; padding:24px 18px; box-shadow:0 2px 8px rgba(0,0,0,0.03); }
.allure-col .ac-icon { font-size:36px; text-align:center; margin-bottom:10px; }
.allure-col .ac-title { font-size:23px; font-weight:700; color:#4338ca; text-align:center; margin-bottom:14px; }
.allure-col .ac-item { font-size:20px; color:#4b5563; line-height:1.8; }
.allure-col .ac-item::before { content:'• '; color:#818cf8; font-weight:700; }

.three-row { display:flex; gap:14px; }
.three-item { flex:1; background:linear-gradient(135deg,#eef2ff,#e0e7ff); border-radius:14px; padding:28px 20px; text-align:center; }
.three-item .tnum { font-size:52px; font-weight:900; color:rgba(99,102,241,0.15); margin-bottom:12px; line-height:1; }
.three-item .tlabel { font-size:22px; font-weight:700; color:#1e1b4b; margin-bottom:10px; }
.three-item .tdesc { font-size:19px; color:#6b7280; line-height:1.7; }
```

#### 11.11.6 金句盒 / 强调块（**每卡结尾必须有**，形成翻页节奏）

> 这是 card-05 排版好最关键的一点：每张内容卡结尾放一个居中强调盒，**不只是在收尾卡放**。

```css
.insight-box { background:rgba(239,68,68,0.06); border:1.5px dashed #fca5a5;      /* 警示型金句 */
  padding:16px 28px; border-radius:12px; font-size:23px; color:#991b1b; text-align:center; font-weight:700; line-height:1.8; }
.allure-tip { background:linear-gradient(135deg,#eff6ff,#eef2ff);                  /* 提示型金句 */
  padding:16px 28px; border-radius:12px; font-size:23px; color:#4338ca; text-align:center; font-weight:700; line-height:1.7; }
.sec-note { background:linear-gradient(135deg,#eff6ff,#eef2ff);                    /* 说明型强调块 */
  padding:28px 36px; border-radius:16px; }
```

### 11.12 排版最佳实践（对照 card-05 标准 · 铁律）

生成任何一篇内容卡，必须逐条对照：

| # | 铁律 | 错误做法 |
|---|------|----------|
| 1 | **每卡双 section**：一张内容卡放 2 个 section（密度优先，5 张卡搞定一篇） | 每卡 1 个 section，撑到 8 张、重复感强 |
| 2 | **组件多样化**：相邻卡片用不同组件（对话盒 / 对比 / 网格 / 多列 / 金句盒轮换） | 6 张内容卡全是同款 `def-list` |
| 3 | **金句盒收尾**：每张内容卡结尾放一个 `.insight-box`/`.allure-tip`/`.sec-note` 强调盒 | 只有收尾卡有 golden，中间卡干巴巴 |
| 4 | **序号角标克制**：右上角 72px 淡标，颜色 `rgba(99,102,241,0.1)` | 居中 300px 巨型半透数字当背景 |
| 5 | **封面 tag + 标题分行**：tag 用「emoji + 痛点/主题 · 副主题」格式；h1 用 `<br>` 主动分行，占卡片宽 60-70% | 只有一个干巴巴的栏目名；标题不分行堆一行 |
| 6 | **故事分层**：翻车/场景用对话盒三态（铺垫→红框翻车→虚线顿悟），不靠 `<br>` 平铺 | 一长条 `<br>` 堆叠，无视觉层次 |
| 7 | **收尾卡结构固定**：`h2 标题 + golden 金句盒 + cta-ask 提问 + save-tip 收藏引导 + hashtags + 水印` | 结构随意、缺互动或收藏引导 |

**收尾卡标准结构（参考值）**：
```css
.card-closing h2 { font-size:44px; font-weight:900; color:#1e1b4b; line-height:1.4; margin-bottom:24px; }
.card-closing .golden { background:rgba(255,255,255,0.65); padding:20px 44px; border-radius:18px;
  font-size:28px; color:#4338ca; font-weight:700; line-height:1.7; margin-bottom:24px; }
.card-closing .cta-ask { font-size:25px; color:#6366f1; line-height:1.9; margin-bottom:20px; }
.card-closing .save-tip { font-size:26px; color:#4f46e5; font-weight:700; margin-bottom:24px; }
.card-closing .hashtags { font-size:21px; color:rgba(67,56,202,0.4); line-height:2; }
```

### 11.13 内容卡底色交替（可选技巧）

当一篇有多张内容卡时，可让部分卡用纯白 `#ffffff` 与默认 `#fafafd` 交替，制造轻微视觉变化、避免连翻几张同色疲劳。

```html
<!-- 默认底色 -->
<div class="card card-content">…</div>
<!-- 交替底色 -->
<div class="card card-content" style="background:#ffffff;">…</div>
```

> ⚠️ 仅限 Tech Indigo（方案1）。Sketch Cream（方案2）已有纸纹差异，不需此技巧，且禁止出现纯白 `#ffffff`。

### 11.14 生成 Checklist（增强版）

在 §11.10 基础上追加：
- [ ] 每张内容卡右上角有克制序号角标（72px 淡标，非巨型背景数字）
- [ ] 相邻内容卡用了**不同**组件（对话盒/对比/网格/多列/金句盒轮换）
- [ ] 每张内容卡有 **2 个 section**，且结尾有金句/强调盒收尾
- [ ] 封面 tag 为「emoji + 痛点/主题 · 副主题」格式，h1 用 `<br>` 主动分行
- [ ] 翻车/故事类内容用了对话盒三态（铺垫→红框翻车→虚线顿悟），非平铺
- [ ] 收尾卡含：h2 + golden 金句 + cta-ask 提问 + save-tip 收藏 + hashtags

---

## 十二、从 Markdown 转换到小红书实操流程

1. **清代码**：所有 ``` 包裹的内容 → 截图或描述改写
2. **清表格**：所有 | 表格 → ✅/❌ 对比卡片或列表
3. **拆长句**：每行不超过 20 字，多断行
4. **删分隔线**：长 ━━━ 替换为 --- 或空行
5. **加空行**：每 2-3 行一个空行，制造呼吸感
6. **检查行内代码**：超过 15 字符的全部改为描述
7. **HTML 卡片**：如需画布笔记，按第十一章规范生成 1080×1440 HTML 卡片



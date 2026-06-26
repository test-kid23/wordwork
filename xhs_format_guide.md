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

- [ ] 标题在 20 字以内？有钩子？
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

### 11.2 配色方案（科技蓝）

> 统一配色，所有卡片使用此方案。

```
封面渐变：  #dbeafe → #bfdbfe → #a5b4fc → #818cf8 → #6366f1
内容卡底色： #fafafd
备用底色：   #ffffff
CTA卡渐变：  #eef2ff → #e0e7ff → #c7d2fe

标题色：     #1e1b4b
主题色：     #6366f1 / #4338ca
section标题：#4338ca + 左边框 4px solid #6366f1
链条按钮：   linear-gradient(135deg, #6366f1, #818cf8)

✅ 正确/优点：#ecfdf5 + #059669
❌ 错误/缺点：#fef2f2 + #dc2626
⚠️ 警告/根源：rgba(239,68,68,0.06) + 1.5px dashed #fca5a5

下载按钮：   background: rgba(0,0,0,0.35), 悬浮 rgba(0,0,0,0.55)
工具栏按钮： background: #6366f1, 悬浮 #4f46e5
```

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
  /* 封面卡 */
  .card-cover{background:linear-gradient(150deg,#dbeafe 0%,#bfdbfe 25%,#a5b4fc 55%,#818cf8 85%,#6366f1 100%);display:flex;flex-direction:column;justify-content:center;align-items:center;padding:48px 56px;text-align:center}
  /* 内容卡 */
  .card-content{background:#fafafd;padding:60px 72px 60px;display:flex;flex-direction:column;position:relative;justify-content:space-evenly}
  /* CTA卡 */
  .card-closing{background:linear-gradient(150deg,#eef2ff 0%,#e0e7ff 50%,#c7d2fe 100%);display:flex;flex-direction:column;justify-content:center;align-items:center;padding:64px 72px;text-align:center;position:relative}
  /* 下载按钮 */
  .dl-btn{position:absolute;top:20px;right:20px;z-index:10;background:rgba(0,0,0,0.35);color:#fff;border:none;padding:10px 20px;border-radius:20px;font-size:22px;cursor:pointer;font-family:'Noto Sans SC',sans-serif}
  .toolbar{position:sticky;top:8px;z-index:100;max-width:1080px;margin:0 auto 12px;display:flex;gap:12px;justify-content:center}
  .toolbar button{background:#6366f1;color:#fff;border:none;padding:12px 32px;border-radius:24px;font-size:22px;font-weight:700;cursor:pointer;font-family:'Noto Sans SC',sans-serif}
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
- [ ] 配色使用科技蓝渐变，未使用其他色系
- [ ] 内容卡使用 `justify-content: space-evenly`
- [ ] 内容上下均匀分布，无上半密集下半空白
- [ ] 顶部有「📥 一键下载全部卡片」工具栏按钮
- [ ] 每张卡右上角有独立下载按钮
- [ ] 下载文件名格式：`文章名-序号.png`
- [ ] 所有卡片右下角水印 `@Testkid`
- [ ] html2canvas scale:2 输出 2x 高清
- [ ] Noto Sans SC 字体 CDN 已引入

---

## 十二、从 Markdown 转换到小红书实操流程

1. **清代码**：所有 ``` 包裹的内容 → 截图或描述改写
2. **清表格**：所有 | 表格 → ✅/❌ 对比卡片或列表
3. **拆长句**：每行不超过 20 字，多断行
4. **删分隔线**：长 ━━━ 替换为 --- 或空行
5. **加空行**：每 2-3 行一个空行，制造呼吸感
6. **检查行内代码**：超过 15 字符的全部改为描述
7. **HTML 卡片**：如需画布笔记，按第十一章规范生成 1080×1440 HTML 卡片

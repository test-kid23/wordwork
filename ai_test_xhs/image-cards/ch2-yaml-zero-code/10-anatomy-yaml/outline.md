# 第10篇 · 小红书配图大纲

---
strategy: b
name: Information-Dense
style: notion
palette: default
image_count: 5
generated: 2026-07-06
render_mode: html
---

## Image 1 of 5

**Position**: Cover
**Layout**: sparse
**Hook**: 一个文件=整套测试？
**Filename**: 01-cover-anatomy

**Text Content**:
- Tag: 零代码测试
- Title: 一个YAML文件 = 整套测试？
- Subtitle: 解剖一个真实案例
- Insight: 四个结构 + 一行命令 = 完整测试套件

**Visual Concept**:
notion极简风 + 手绘线条感。白色背景，大标题居中，pastel蓝色(#A8D4F0)色块点缀，css不规则边框模拟手绘

**Swipe Hook**: 看看里面长啥样👇

---

## Image 2 of 5

**Position**: Content
**Layout**: flow
**Core Message**: YAML文件四大块结构
**Filename**: 02-content-structure

**Text Content**:
- Title: YAML 文件四大块
- Blocks (依次向下，箭头连接):
  1. name — 套件名称 "告诉团队测什么"
  2. base_url — 基础地址 "所有接口共用前缀"
  3. variables — 全局变量 "整个文件共享"
  4. cases — 用例列表 "一条case = 请求+断言"
- Insight: 不需要导入任何库 / 不需要写 class 和 def

**Visual Concept**:
notion flow布局，4个pastel色块垂直排列，CSS虚线箭头连接，手绘风格编号圆圈，color: notion内置pastel轮换(blue→mint→lavender→yellow)

**Swipe Hook**: 跟Python差多少？👇

---

## Image 3 of 5

**Position**: Content
**Layout**: comparison
**Core Message**: 同一个CRUD，Python vs YAML 文件数对比
**Filename**: 03-content-comparison

**Text Content**:
- Title: 同样的 CRUD，两种写法
- Left (Python): 5个文件 | 150行代码 | import + conftest + 4个test文件
- Right (YAML): 1个文件 | 50行配置 | 4个case排好队
- Conclusion: 不是代码行数的差距 / 是管理复杂度的差距

**Visual Concept**:
notion comparison，左右分栏+虚线分隔。左侧pastel pink底色(带✕)，右侧pastel mint底色(带✓)，文件图标数量对比

**Swipe Hook**: 里面什么结构？👇

---

## Image 4 of 5

**Position**: Content
**Layout**: dense
**Core Message**: 解剖一个真实用例（创建用户）
**Filename**: 04-content-anatomy

**Text Content**:
- Title: 解剖 "创建新用户"
- Four sections (带hand-drawn bracket):
  1. 名称 "描述用例做什么" → 创建新用户
  2. 请求 "POST到指定地址" → POST /api/v1/users
  3. 提取 "从响应抠user_id" → 给后续用例用
  4. 断言 "验状态码+用户名" → 201 + 用户名一致
- Insight: 没有一句代码 / 但该做的事都做了

**Visual Concept**:
notion dense，文件注解风格。中心一个"文档"卡片，四边手绘括号标注，pastel色块做分区标记

**Swipe Hook**: 总结一下👇

---

## Image 5 of 5

**Position**: Ending
**Layout**: sparse
**Core Message**: CTA + 下篇预告
**Filename**: 05-ending-cta

**Text Content**:
- Question: YAML 和 Python 哪种更容易看懂？
- CTA: 评论区聊聊你的选择
- Hashtag: YAML测试 接口自动化 零代码 测试用例
- Preview: 下篇 · 十分钟写完整套CRUD

**Visual Concept**:
notion sparse，大留白。对话气泡(notion hand-drawn风格)，@Testkid水印在右下，整体干净利落

---

## Style Spec Summary (notion → CSS)

| Element | Value |
|---------|-------|
| Background | #FAFAFA (off-white) |
| Text | #1A1A1A (primary), #4A4A4A (secondary) |
| Accent | #A8D4F0 blue, #F9E79F yellow, #FADBD8 pink, #B5E5CF mint, #D5C6E0 lavender |
| Font | Noto Sans SC, light/regular/bold |
| Border | 1.5px solid #E0E0E0, slight CSS dither (filter or box-shadow irregular trick) |
| Card corners | 12px, subtle shadow 0 2px 8px rgba(0,0,0,0.04) |
| Whitespace | 40-50% for sparse, 30% for dense |

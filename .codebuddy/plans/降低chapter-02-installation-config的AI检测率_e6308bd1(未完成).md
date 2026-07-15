---
name: 降低chapter-02-installation-config的AI检测率
overview: 针对 claude_code/chapter-02-installation-config.md 文件，通过打散文档结构、加入更多口语化表达和个人立场、删除部分过于规整的格式、增加翻车细节等手段，将AI检测率从68.84%降到合理范围。
todos:
  - id: diagnose-ai-patterns
    content: 使用 [skill:deai-writer] 对全文做 AI 味逐段诊断，输出具体问题清单（标注到行号）
    status: pending
  - id: rewrite-structure
    content: 使用 [skill:deai-writer] 执行第一优先级改造：打散目录/步骤编号/坑的三段式模板/减少表格
    status: pending
    dependencies:
      - diagnose-ai-patterns
  - id: rewrite-language
    content: 使用 [skill:deai-writer] 执行第二优先级改造：注入口语转折词/代词切换/立场表达/重写结尾
    status: pending
    dependencies:
      - rewrite-structure
  - id: rewrite-content
    content: 使用 [skill:deai-writer] 执行第三优先级改造：展开翻车场景/删减过度解释/增加留白和不推荐板块
    status: pending
    dependencies:
      - rewrite-language
  - id: humanizer-polish
    content: 使用 [skill:humanizer] 对改写后全文做最终过筛，修复残留的 AI 细节特征（被动语态/规则之三/AI词汇等）
    status: pending
    dependencies:
      - rewrite-content
---

## 产品概述

对 `claude_code/chapter-02-installation-config.md` 进行去 AI 味改写，将 AI 检测工具判定的高 AI 特征占比（68.84%）降到合理范围。

## 核心问题诊断

文章被判定为高 AI 含量的核心原因：

**结构层面（最严重）：**

1. 完美的5章目录索引（第15-22行）——教科书式目录，真人写作极少这么工整
2. 第三章 API 配置用"第一步/第二步/第三步/第四步/第五步"编号（第107-179行）——典型 AI 教程模板
3. 第五章每个坑都严格遵循"表现/真相/解法"三段式（第239-311行）——高度模板化
4. 大量表格嵌套（准备清单表格、坑的统一格式）——过度结构化

**语言层面：**

1. 中间技术步骤段落缺乏口语化转折词，全程"教学腔"
2. 部分表述偏客观中立（"推荐官方脚本"、"最简单"）
3. 结尾"写在最后"有 AI 金句味道（第319-323行）

**内容层面：**

1. 解释过于详尽、面面俱到，缺少留白
2. 翻车经历只在开头一笔带过（第9行），未展开具体故事场景
3. 缺乏足够的个人立场和主观判断

## 改写目标

- 打散教科书结构，让排版看起来像真人随笔
- 加入更多口语化表达和情绪波动
- 把部分"教学步骤"改成叙事性描述
- 增加具体翻车场景和心理活动
- 删减过度详细的技术解释，留白给读者自己探索

## 技术方案

纯内容改写任务，不涉及代码实现。核心依据是 PROJECT_CONTEXT.md 第243-292行的「写作风格指引」硬风格约束。

## 改写策略

按照以下优先级逐项改造：

### 第一优先级：结构打散（影响最大）

- 删除或大幅简化开头的5章完美目录
- 将"第一步/第二步..."的编号步骤改成段落叙述
- 将5个坑的统一三段式模板打破——每个坑用不同的叙述方式
- 减少表格使用，能文字说清的不用表格

### 第二优先级：语言人味化

- 在技术段落间插入口语化转折词（说实话/你猜怎么着/这就很操蛋了/不过话说回来）
- 代词检查：确保"我/我们/大家/你"按关系切换，不要全篇"你"说教腔
- 加入明确的主观判断和立场表达
- 结尾去掉金句式收尾，换成大白话或戛然而止

### 第三优先级：内容调整

- 开头提到的踩坑经历展开至少一个具体场景（有时间、有操作、有报错、有当时心理活动）
- 技术解释适度删减，加入"这个细节不展开了"类的留白
- 增加1-2个"网上有人教你XX，别学"类的不推荐板块

## Agent Extensions

### Skill: deai-writer

- **Purpose**: 专门用于减少 AI 写作味道，基于项目 PROJECT_CONTEXT.md 中定义的8类必须避开的 AI 味写法和6种必须加入的人味元素进行逐项检视和改写
- **Expected output**: 对 chapter-02-installation-config.md 进行全面去 AI 味改写，覆盖结构打散、语言人味化、内容调整三个维度

### Skill: humanizer

- **Purpose**: 基于 Wikipedia 的 AI 写作特征指南，检测并修复包括夸张象征语、推销语言、破折号滥用、规则之三、AI 词汇、被动语态等具体模式
- **Expected output**: 作为 deai-writer 的补充，对改写后的文本进行二次过筛，消除残留的细微 AI 写作特征
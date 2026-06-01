# 不想把代码喂给云端 AI？教你搭一套全本地的开发团队

我在咖啡馆写代码，旁边坐了个做金融 SaaS 的兄弟。他看我屏幕上一堆 PR 自动 Review，问我用什么工具。

我说："Ollama + Qwen，全跑本地。"

他愣了两秒："本地？不是都用 Claude 或者 Copilot 吗？"

"金融系统的代码，你敢往云端扔？"

他沉默了一会儿，要了我的配置清单。

这篇就是写给他的，也写给所有"想让 AI 替你写码，但不想把代码送出去"的人。

---

## 本地 AI 开发团队能干什么

先说结果。我现在的开发流程：

早上 9 点，在 GitHub Issue 写需求描述，打上 `ai-dev` 标签。

9 点 15，编码 AI 自动生成了代码，创建了 PR。PR 创建后，三个 Agent 同时干活：审查 AI 在 Review 代码（标志出安全漏洞、性能问题、风格不一致），测试 AI 自动生成测试用例，文档 AI 等合并后自动更新 API 文档。

我只需做一件事：看代码逻辑、看审查报告、看测试覆盖、看安全报告——5 分钟，决定合并还是打回。

**全程代码不出本地。一次 API 费用都没有。**

---

## 你需要什么硬件

不是非要很贵的显卡。三个档位，按预算来：

| 方案 | 配置 | 能跑什么 | 投入 |
|------|------|---------|------|
| **入门** | Mac Mini M4 Pro 48GB | Qwen2.5-Coder-14B / DeepSeek-Coder 7B | ¥12,000 |
| **进阶** | 单卡 RTX 4090 24GB | Qwen2.5-32B / DeepSeek-Coder 33B（量化） | ¥18,000 |
| **专业** | 双卡 RTX 4090 / Mac Studio 192GB | Qwen2.5-72B / DeepSeek-V3（量化） | ¥35,000-55,000 |

**入门级就够了。** Mac Mini 跑 Qwen2.5-Coder-14B Q4 量化版，延迟 10-15 秒/响应，日常编码辅助完全够。不需要一上来就上显卡。我自己就是从 Mac Mini 起步的。

---

## 四个 Developer Agent，各自干什么

### 编码 Agent：你的主力程序员

角色设定很简单：你是全栈工程师，精通 TypeScript/Python/Go。每次写代码前，先去本地向量库（ChromaDB）检索项目里相关的代码片段，自动遵循已有的命名规范和架构模式。

不确定的设计决策标注为 `// TODO: DECISION -` 留给你做选择。

用 Qwen2.5-Coder-14B（Q4 量化），本地跑，零成本。

### 审查 Agent：你的 Code Reviewer

自动 Review 每一个 PR。检查清单：SQL 注入、XSS 漏洞、空指针、N+1 查询、硬编码密钥。输出分三档：🔴 必须修改 / 🟡 建议优化 / 🟢 仅供参考。

它不能替代你的判断。但有了这份清单，你看代码的时间从 20 分钟降到 5 分钟——因为不需要逐行找问题，只需要确认它找到的问题是否属实。

### 测试 Agent：自动补测试

根据 PR 的代码变更，自动生成单元测试。每个测试标注设计意图——"测试边界：空数组输入""测试异常：网络超时"——不是 `assert 1+1==2` 这种垃圾用例。

### 文档 Agent：再也不用手写 API 文档

代码合并后自动更新 API 文档、追加 CHANGELOG、生成架构决策记录。你只管写码，文档它能自己跟上。

---

## 怎么让它们跑起来：GitHub Actions + Ollama

整个 Pipeline 靠 GitHub Actions 的 Webhook 驱动。配置不复杂：

```yaml
# .github/workflows/ai-dev-pipeline.yml
name: AI Development Pipeline

on:
  issues:
    types: [opened, labeled]

jobs:
  ai-coding:
    if: contains(github.event.issue.labels.*.name, 'ai-dev')
    runs-on: self-hosted  # 有 GPU 的本地机器上跑
    steps:
      - name: Coding Agent
        run: |
          curl -X POST http://localhost:11434/api/generate \
            -H "Content-Type: application/json" \
            -d '{
              "model": "qwen2.5-coder:14b",
              "prompt": "${{ github.event.issue.body }}",
              "stream": false
            }' > /tmp/output.json

      - name: Create PR
        run: python3 .github/scripts/create_pr.py /tmp/output.json
```

PR 创建后，三个 Agent（审查+测试+安全）并行自动触发，各自输出报告挂到 PR 底下。你打开 PR 的时候，四份参考材料已经齐了。

---

## 两个新手最容易踩的硬件坑

### 坑一：显存不够硬跑

公式很简单：**模型大小 × 量化系数 + 上下文开销 ≈ 显存需求**

- Qwen2.5-14B @ Q4 → 14B × 0.5 = 7GB + 上下文 ~2GB = **~9GB**
- Qwen2.5-32B @ Q4 → 32B × 0.5 = 16GB + 上下文 ~4GB = **~20GB**

一条铁律：**模型显存占用不超过总显存的 70%**。剩下 30% 是给上下文和系统的。

别在 24GB 显卡上跑 70B 模型——量化到 Q2 质量变成傻子，不如用 32B 的 Q5。

### 坑二：上下文无限拉满

PR diff 塞 10000 行进去 → OOM。解法：截断到 8000 字符，或分层摘要——先用小模型（7B）提取变更摘要+5 个关键片段，再送给大模型（14B）。

---

## 这套方案的真正价值

不是省钱。Cloud API 一个月也就几百块。

是**控制感**。

- 金融、医疗、政府项目的代码，合规要求不允许出本地
- 高铁上、客户内网、断网环境，AI 照常干活
- 代码审查 Agent 看多了你的 Review 意见，你甚至可以微调它——它越来越像你的判断
- 没人拿你的代码库去训练模型

---

## 如果你现在就想试

三件事，今晚就能干：

1. `brew install ollama` → `ollama pull qwen2.5-coder:14b` → 五分钟装好第一个本地编码模型
2. 在 Cursor 里把 Model 切到 `ollama/qwen2.5-coder:14b`，感受一下本地推理的速度
3. 随便写个需求描述，看它能出什么

如果感觉不错，下周搭 GitHub Actions Pipeline，再下周上 ChromaDB 做代码库 RAG。一步一个脚印，别一上来就追集群方案。

---

*下一篇见。AI 团队搭起来之后才是真正的开始——怎么监控它有没有退步？什么时候该换模型？Prompt 怎么管才不乱？下一篇写长期运维。*

*你现在本地跑什么模型？遇到过 OOM 吗？评论区聊聊。*

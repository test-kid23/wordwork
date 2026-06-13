# AI 时代进阶指南：从零搭建专属 AI 团队

> **面向读者**：具备基础开发能力，已熟悉主流 AI 工具的使用，希望进一步构建私有化、定制化的 AI 模型体系。
> **你会得到什么**：一套完整的实操路径——从单模型部署到多模型协同的 AI 团队架构，覆盖数据处理、微调、评估、部署全链路。

---

## 目录

1. [问题定义：为什么你的业务需要"AI 团队"而非"一个 AI"](#一问题定义为什么你的业务需要ai-团队而非一个-ai)
2. [第一层：模型选型与本地部署](#二第一层模型选型与本地部署)
3. [第二层：复杂场景的需求拆解](#三第二层复杂场景的需求拆解)
4. [第三层：数据处理与微调策略](#四第三层数据处理与微调策略)
5. [第四层：模型评估与迭代优化](#五第四层模型评估与迭代优化)
6. [第五层：多模型协同架构设计](#六第五层多模型协同架构设计)
7. [实施路线图：从 0 到 1 的四周计划](#七实施路线图从-0-到-1-的四周计划)
8. [附录：工具链与资源索引](#八附录工具链与资源索引)

---

## 一、问题定义：为什么你的业务需要"AI 团队"而非"一个 AI"

### 一个真实场景

你运营一个电商 SaaS 平台。你试过用 ChatGPT API 处理所有事情——客服回复、商品描述生成、评论分析、数据报表解读。

问题来了：
- 客服需要**即时响应**（延迟 < 500ms），GPT-4 太慢也太贵
- 商品描述需要**品牌调性一致**，通用模型写出来像淘宝模板
- 评论分析涉及**用户隐私**，不能上传到第三方 API
- 数据报表解读需要理解**你的业务口径**，"GMV 环比下降 12%" 这句话通用模型不知道你在说什么

**一个模型解决不了所有问题。你需要一支 AI 团队。**

### 核心认知

```
┌─────────────────────────────────────────────────────┐
│                  你的 AI 团队架构                      │
│                                                       │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │ 路由层   │  │ 路由层   │  │ 路由层   │  │ 路由层   │ │
│  │ (网关)   │──│ (网关)   │──│ (网关)   │──│ (网关)   │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘ │
│       │              │              │              │      │
│  ┌────▼─────┐  ┌────▼─────┐  ┌────▼─────┐  ┌────▼─────┐ │
│  │ 客服模型  │  │ 写作模型  │  │ 分析模型  │  │ 审核模型  │ │
│  │ (3B 微调) │  │ (7B 微调) │  │ (14B+RAG)│  │ (1B 分类) │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
│                                                       │
│  共享层：向量数据库 / 提示词模板 / 评估框架 / 监控      │
└─────────────────────────────────────────────────────┘
```

每个模型只做一件事，但做到极致。它们通过一个**智能路由层**协同工作——请求进来，路由层判断意图，分发给最合适的模型。

---

## 二、第一层：模型选型与本地部署

在你开始微调之前，先把"能用"的模型跑起来。这一步建立你的基础设施。

### 2.1 按场景选模型：一张决策表

| 场景 | 推荐模型规模 | 推理框架 | 硬件要求 | 量化建议 |
|------|-------------|----------|----------|----------|
| 文本分类/情感分析 | 0.5B-3B | llama.cpp / vLLM | 4GB RAM | Q4_K_M |
| 客服对话/FAQ | 3B-8B | llama.cpp / Ollama | 8GB RAM / 6GB VRAM | Q4_K_M |
| 内容生成/写作 | 7B-14B | vLLM / TGI | 16GB RAM / 12GB VRAM | Q5_K_M |
| 代码生成/审查 | 7B-33B | vLLM / TGI | 24GB VRAM | Q4_K_M |
| 复杂推理/数据分析 | 14B-72B | vLLM (多 GPU) | 48GB+ VRAM | Q4_K_M |
| 多模态（图+文） | 7B-11B VL | llama.cpp | 12GB VRAM | Q4_K_M |
| 嵌入/语义检索 | 0.1B-0.5B Emb | TEI / llama.cpp | 2GB RAM | 无需量化 |
| 语音转文字 | Whisper 模型 | faster-whisper | 4GB VRAM | int8 |

### 2.2 推理框架选型

**核心问题：选 llama.cpp 还是 vLLM？**

| 维度 | llama.cpp | vLLM |
|------|-----------|------|
| 适用场景 | 单用户 / 低并发 | 高并发 / 生产环境 |
| 吞吐量（并发） | 低，单请求串行 | 高，PagedAttention 连续批处理 |
| GPU 利用率 | 中等 | 高（90%+） |
| 部署复杂度 | 低，单二进制 | 中等，需 Python 环境 |
| CPU 推理 | 优秀 | 不支持 |
| 量化支持 | GGUF（极丰富） | AWQ / GPTQ |
| 最佳搭配 | 边缘设备 / 本地开发 | 服务器 / API 服务 |

**结论**：
- 开发调试阶段用 llama.cpp（快速迭代，本地跑）
- 生产环境用 vLLM（高并发，低延迟）
- 边缘设备 / 消费级显卡用 llama.cpp

### 2.3 实战：用 llama.cpp 同时跑 3 个模型

```bash
# 终端 1：客服模型（小模型，快速响应）
./build/bin/llama-server \
  -m ./models/qwen2.5-3b-instruct-Q4_K_M.gguf \
  --port 8081 \
  --n-gpu-layers 33 \
  --ctx-size 4096 \
  --threads 4 \
  --host 127.0.0.1

# 终端 2：写作模型（中等模型，质量优先）
./build/bin/llama-server \
  -m ./models/qwen2.5-7b-instruct-Q5_K_M.gguf \
  --port 8082 \
  --n-gpu-layers -1 \
  --ctx-size 8192 \
  --threads 8 \
  --host 127.0.0.1

# 终端 3：嵌入模型（语义检索专用）
./build/bin/llama-server \
  -m ./models/bge-small-zh-1.5-Q4_K_M.gguf \
  --port 8083 \
  --embeddings \
  --n-gpu-layers -1 \
  --ctx-size 512 \
  --host 127.0.0.1
```

现在你有了三个独立的 API 端点，分别对应不同的能力。这是 AI 团队的雏形。

### 2.4 关键参数调优

不要用默认参数上生产。以下是经过验证的配置：

```bash
# 生产级配置模板
--ctx-size 16384        # 根据业务确定，不是越大越好
--batch-size 2048       # prompt 处理批大小，显存充足可到 4096
--ubatch-size 512       # 解码批大小，通常保持 512
--flash-attn            # 必须开启，节省 30-50% KV Cache 显存
--threads <物理核数>     # 不是超线程数
--threads-batch <核数×2> # 批处理可用更多线程
--temp 0.7              # 对话/创作场景
--temp 0.1              # 分类/提取场景
--top-p 0.9             # 配合温度使用
--repeat-penalty 1.1    # 防重复输出
```

---

## 三、第二层：复杂场景的需求拆解

部署了模型只是第一步。真正拉开差距的是**你能不能把业务需求翻译成模型能理解的任务**。

### 3.1 需求拆解框架

面对一个复杂需求，按以下步骤拆解：

```
原始需求
    │
    ▼
┌─────────────────┐
│ 1. 识别子任务     │  ← 这个需求包含几个独立的能力单元？
├─────────────────┤
│ 2. 匹配模型能力   │  ← 每个子任务最适合什么类型/规模的模型？
├─────────────────┤
│ 3. 定义输入输出   │  ← 每个子任务的输入格式、输出格式、约束条件？
├─────────────────┤
│ 4. 设计串联逻辑   │  ← 子任务之间有依赖关系吗？并行还是串行？
├─────────────────┤
│ 5. 评估与容错     │  ← 每个环节出错了怎么办？降级策略是什么？
└─────────────────┘
```

### 3.2 案例拆解：智能客服系统

**原始需求**："搭建一个智能客服，能自动回复用户问题，处理退款申请，并在必要时转人工。"

**拆解结果**：

```
用户消息
    │
    ▼
┌──────────────┐
│ 意图分类模型   │  ← 3B 微调分类器，判断：咨询/投诉/退款/闲聊
│ (本地部署)    │     延迟 < 100ms
└──────┬───────┘
       │
   ┌───┼───┬──────────┐
   ▼   ▼   ▼          ▼
 咨询  投诉 退款      闲聊
   │   │   │          │
   ▼   ▼   ▼          ▼
┌────┐┌────┐┌──────┐┌──────┐
│FAQ ││安抚││退款流││闲聊  │
│检索││+升 ││程引  ││模型  │
│+   ││级  ││导模  ││      │
│生成││路由││型    ││      │
└────┘└────┘└──────┘└──────┘
   │   │   │          │
   └───┴───┴──────────┘
            │
            ▼
    ┌──────────────┐
    │ 输出格式化    │  ← 统一输出格式，添加工单编号、时间戳
    │ + 敏感词过滤  │
    └──────────────┘
```

**关键决策**：
- 意图分类用专用小模型（3B），不用大模型——快、便宜、准确率高
- 退款走**确定性流程**而非生成式——涉及金钱不能靠概率
- 投诉自动升级到人工——AI 只做初步安抚和信息收集
- 每个模型独立部署，互不影响——一个挂了不影响其他

### 3.3 需求拆解检查清单

面对任何新需求，逐项确认：

- [ ] 这个需求是否有**确定性**的部分（规则引擎 > 模型）？
- [ ] 是否有**延迟敏感**的子任务（< 200ms 用分类模型，> 1s 可用大模型）？
- [ ] 是否有**隐私/合规**约束（必须本地处理的数据）？
- [ ] 子任务之间是**串行依赖**还是**可并行**？
- [ ] 每个子任务的**失败影响**是什么？降级策略是什么？
- [ ] 是否可以利用**已有模型**而非新建？

---

## 四、第三层：数据处理与微调策略

通用模型是毛坯房，微调是精装修。但 90% 的微调失败是因为数据问题，不是技术问题。

### 4.1 数据策略：质量 >> 数量

一个反直觉的事实：**500 条高质量微调数据的效果，往往好过 5000 条低质量数据。**

```
数据质量金字塔
        ┌──────┐
        │ 专家  │  ← 业务专家标注，100-500 条
        │ 标注  │     覆盖率最高的 20% 场景
        ├──────┤
        │ 用户  │  ← 从真实日志中清洗抽取，500-2000 条
        │ 反馈  │     覆盖长尾场景
        ├──────┤
        │ 自动  │  ← 用大模型生成 + 人工抽检，2000-10000 条
        │ 生成  │     快速扩充训练集
        ├──────┤
        │ 公开  │  ← 开源数据集，提供基础能力
        │ 数据  │     不包含你的业务知识
        └──────┘
```

### 4.2 数据构造实战

以"电商客服回复"微调为例：

**Step 1：收集真实对话**

从客服系统中导出最近 3 个月的优质对话记录（客户评分 ≥ 4 星的会话）。

**Step 2：清洗与标准化**

```python
# 数据清洗脚本示例
import json
import re

def clean_conversation(raw):
    """清洗一条客服对话记录"""
    # 去除敏感信息
    text = re.sub(r'\b1[3-9]\d{9}\b', '[PHONE]', raw['content'])
    text = re.sub(r'\b\d{15,19}\b', '[CARD]', text)
    text = re.sub(r'[\w.-]+@[\w.-]+\.\w+', '[EMAIL]', text)

    # 去除系统自动消息
    if any(kw in text for kw in ['系统消息', '自动回复', '正在输入']):
        return None

    return text

# 转换为微调格式（ChatML）
def to_chatml(conversation):
    messages = []
    for turn in conversation['turns']:
        role = "assistant" if turn['speaker'] == 'agent' else "user"
        messages.append({"role": role, "content": turn['text']})
    return {"messages": messages}
```

**Step 3：数据格式选择**

| 格式 | 适用框架 | 特点 |
|------|---------|------|
| ChatML / ShareGPT | llama.cpp, vLLM, Axolotl | 通用对话格式，推荐 |
| Alpaca (instruction/input/output) | 传统微调 | 简单但能力有限 |
| Conversation (JSONL) | Axolotl, LLaMA-Factory | 灵活，支持 system prompt |

### 4.3 微调策略决策树

```
需要微调吗？
├── 只需要注入知识 → RAG（检索增强生成），不需要微调
├── 需要改变输出风格/格式 → 微调（全量或 LoRA）
├── 需要学习新任务能力 → 微调（全量优先）
├── 只需要调整行为偏好 → DPO/RLHF 对齐微调
└── 只是偶尔用 → Prompt Engineering 就够了
```

### 4.4 LoRA 微调实战

LoRA（Low-Rank Adaptation）是最经济的微调方式——只训练少量参数（通常 < 1%），效果接近全量微调。

**工具选型**：

| 工具 | 适用场景 | 硬件要求 |
|------|---------|----------|
| **LLaMA-Factory** | 新手首选，Web UI，中文友好 | 7B: 16GB VRAM |
| **Axolotl** | 进阶用户，配置灵活，社区活跃 | 7B: 16GB VRAM |
| **Unsloth** | 追求速度，2-5x 训练加速 | 7B: 8GB VRAM |
| **transformers + PEFT** | 需要最大控制力 | 7B: 16GB VRAM |

**LLaMA-Factory 微调命令示例**：

```bash
# 安装
git clone https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e ".[torch,metrics]"

# LoRA 微调（7B 模型，单卡 16GB VRAM）
llamafactory-cli train \
    --model_name_or_path Qwen/Qwen2.5-7B-Instruct \
    --dataset_dir data \
    --dataset customer_service_qa \
    --template qwen \
    --finetuning_type lora \
    --lora_rank 16 \
    --lora_alpha 32 \
    --lora_target q_proj,v_proj,k_proj,o_proj \
    --output_dir ./output/cs-lora \
    --per_device_train_batch_size 4 \
    --gradient_accumulation_steps 4 \
    --lr_scheduler_type cosine \
    --logging_steps 10 \
    --save_steps 500 \
    --learning_rate 2e-4 \
    --num_train_epochs 3 \
    --bf16
```

**关键参数说明**：

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| `lora_rank` | 8-32 | 越大效果越好，但训练越慢。16 是甜点 |
| `lora_alpha` | rank × 2 | LoRA 缩放系数，通常是 rank 的 2 倍 |
| `lora_target` | q_proj,v_proj,k_proj,o_proj | 注意力投影层，覆盖这些就够了 |
| `learning_rate` | 1e-4 ~ 5e-4 | LoRA 可以比全量微调稍高 |
| `num_train_epochs` | 2-5 | 小数据集 3-5 轮，大数据集 1-2 轮 |

### 4.5 合并与导出

微调完成后，将 LoRA 权重合并到基座模型并量化为 GGUF：

```bash
# 步骤 1：合并 LoRA 权重
llamafactory-cli export \
    --model_name_or_path Qwen/Qwen2.5-7B-Instruct \
    --adapter_name_or_path ./output/cs-lora \
    --template qwen \
    --finetuning_type lora \
    --export_dir ./output/cs-merged \
    --export_size 2 \
    --export_legacy_format False

# 步骤 2：转换为 GGUF 格式
python llama.cpp/convert_hf_to_gguf.py ./output/cs-merged \
    --outfile ./models/cs-agent-Q4_K_M.gguf \
    --outtype q4_k_m
```

---

## 五、第四层：模型评估与迭代优化

部署不是终点。模型在实际业务中的表现，和你在测试集上看到的是两回事。

### 5.1 评估体系设计

**三层评估金字塔**：

```
        ┌──────────┐
        │ 业务指标  │  ← 用户满意度、解决率、转化率（最重要）
        ├──────────┤
        │ 功能指标  │  ← 准确率、召回率、BLEU/ROUGE、幻觉率
        ├──────────┤
        │ 技术指标  │  ← 延迟(P50/P95/P99)、吞吐量、显存占用
        └──────────┘
```

### 5.2 功能指标评估方法

**不要只依赖自动指标。LLM-as-Judge 是目前最实用的评估方式。**

```python
# 用 GPT-4 作为评判者的评估脚本
import json
from openai import OpenAI

EVAL_PROMPT = """你是一个严格的评估者。请对比模型输出和参考答案，给出评分。

评分维度（1-5分）：
1. 准确性：回答是否事实正确
2. 完整性：是否涵盖了所有关键信息
3. 风格一致性：是否符合要求的语气和格式
4. 安全性：是否包含不当内容

输入问题：{question}
模型输出：{response}
参考答案：{reference}

请输出 JSON 格式：
{{"accuracy": int, "completeness": int, "style": int, "safety": int, "comment": str}}
"""

def evaluate_response(question, response, reference):
    client = OpenAI()
    result = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": EVAL_PROMPT.format(
            question=question, response=response, reference=reference
        )}],
        response_format={"type": "json_object"}
    )
    return json.loads(result.choices[0].message.content)
```

**必须建立的评估集**：
- **回归测试集**（50-100 条）：每次更新必须通过的底线用例
- **边界测试集**（30-50 条）：极端输入、对抗样本、空输入等
- **盲测集**（100-200 条）：模型没见过的真实业务数据，用于最终评估

### 5.3 在线评估：A/B 测试框架

```python
# 简单的 A/B 测试路由中间件
import random

class ABRouter:
    def __init__(self, model_a, model_b, traffic_split=0.5):
        self.model_a = model_a  # 对照组（当前版本）
        self.model_b = model_b  # 实验组（新版本）
        self.split = traffic_split

    def route(self, request):
        if random.random() < self.split:
            response = self.model_b.generate(request)
            self._log("experiment", request, response)
        else:
            response = self.model_a.generate(request)
            self._log("control", request, response)
        return response

    def _log(self, group, request, response):
        # 记录到数据库：组别、请求内容、响应、延迟、用户后续行为
        pass
```

**A/B 测试关注的核心指标**：

| 指标 | 计算方式 | 目标 |
|------|---------|------|
| 用户采纳率 | 用户未修改/复制/点赞的比例 | 提升 > 5% |
| 任务完成率 | 对话后用户目标达成的比例 | 提升 > 3% |
| 平均对话轮次 | 解决问题所需的对话轮数 | 降低 > 10% |
| 转人工率 | 对话中触发转人工的比例 | 降低 > 15% |

### 5.4 迭代优化闭环

```
                  ┌──────────────┐
                  │  线上运行     │
                  └──────┬───────┘
                         │
            ┌────────────┼────────────┐
            ▼            ▼            ▼
      ┌──────────┐ ┌──────────┐ ┌──────────┐
      │ 用户反馈  │ │ 错误日志  │ │ 性能指标  │
      │ (点赞/踩) │ │ (分类统计)│ │ (延迟/QPS)│
      └────┬─────┘ └────┬─────┘ └────┬─────┘
           │            │            │
           └────────────┼────────────┘
                        ▼
              ┌─────────────────┐
              │ 问题聚类与分析    │  ← 每周 Review
              │ Top N 错误类型   │
              └────────┬────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │ 补充训练  │ │ 调整 Prompt│ │ 规则兜底  │
    │ 数据      │ │ /参数     │ │          │
    └──────────┘ └──────────┘ └──────────┘
          │            │            │
          └────────────┼────────────┘
                       ▼
              ┌─────────────────┐
              │ 评估 → A/B测试   │
              │ → 上线/回滚      │
              └─────────────────┘
```

**迭代节奏建议**：
- **每周**：Review 线上 bad case Top 10，快速修复（Prompt 调整 / 规则补丁）
- **每月**：更新训练数据（加入上月 bad case 的修正版本），重新微调
- **每季度**：评估是否需要升级基座模型（如从 7B 升到 14B）

---

## 六、第五层：多模型协同架构设计

### 6.1 整体架构

```
                          ┌──────────────────┐
                          │   负载均衡/网关    │
                          │  (Nginx / Traefik)│
                          └────────┬─────────┘
                                   │
                          ┌────────▼─────────┐
                          │   智能路由层       │
                          │  (意图识别 + 分发) │
                          └────────┬─────────┘
                                   │
          ┌────────────┬───────────┼───────────┬────────────┐
          ▼            ▼           ▼           ▼            ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
    │ 分类模型  │ │ 对话模型  │ │ 生成模型  │ │ 嵌入模型  │ │ 审核模型  │
    │ (Router) │ │ (Chat)   │ │ (Writer) │ │ (Embed)  │ │ (Guard)  │
    │ 0.5-3B   │ │ 7-14B    │ │ 7-14B    │ │ 0.1-0.5B │ │ 0.5-3B   │
    │ CPU 即可 │ │ GPU      │ │ GPU      │ │ CPU 即可 │ │ CPU 即可 │
    └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
                                   │
                          ┌────────▼─────────┐
                          │   共享基础设施     │
                          │ ┌──────────────┐ │
                          │ │ 向量数据库    │ │  ← Qdrant / Milvus / Chroma
                          │ │ 提示词模板库  │ │  ← 版本化管理
                          │ │ 评估框架      │ │  ← 统一评估标准
                          │ │ 日志 & 监控   │ │  ← Prometheus + Grafana
                          │ └──────────────┘ │
                          └──────────────────┘
```

### 6.2 智能路由层实现

路由层是整个架构的大脑，负责判断每个请求应该交给哪个模型处理。

```python
# 智能路由层核心实现
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
import httpx

class TaskType(Enum):
    CLASSIFICATION = "classification"   # 意图分类/情感分析
    CHAT = "chat"                       # 对话/客服
    GENERATION = "generation"           # 内容生成/写作
    EMBEDDING = "embedding"             # 向量化/语义检索
    GUARD = "guard"                     # 安全审核/敏感词

@dataclass
class RouteDecision:
    task_type: TaskType
    model_endpoint: str
    priority: int           # 优先级，用于降级
    timeout_ms: int
    retry_count: int

class IntelligentRouter:
    def __init__(self):
        # 模型注册表：每个任务类型对应多个候选模型
        self.registry = {
            TaskType.CLASSIFICATION: [
                RouteDecision(TaskType.CLASSIFICATION, "http://127.0.0.1:8081", 1, 200, 1),
            ],
            TaskType.CHAT: [
                RouteDecision(TaskType.CHAT, "http://127.0.0.1:8082", 1, 5000, 2),
                RouteDecision(TaskType.CHAT, "http://127.0.0.1:8084", 2, 8000, 1),  # 降级模型
            ],
            TaskType.GENERATION: [
                RouteDecision(TaskType.GENERATION, "http://127.0.0.1:8083", 1, 15000, 1),
            ],
            TaskType.EMBEDDING: [
                RouteDecision(TaskType.EMBEDDING, "http://127.0.0.1:8085", 1, 1000, 2),
            ],
            TaskType.GUARD: [
                RouteDecision(TaskType.GUARD, "http://127.0.0.1:8086", 1, 500, 2),
            ],
        }
        self.client = httpx.AsyncClient(timeout=30.0)

    async def classify_intent(self, text: str) -> TaskType:
        """用轻量分类模型判断请求意图"""
        # 先用规则快速过滤
        if any(kw in text for kw in ["写", "生成", "创作", "帮我写"]):
            return TaskType.GENERATION
        if len(text) < 20 and any(kw in text for kw in ["?", "？", "什么", "怎么"]):
            return TaskType.CHAT

        # 调用分类模型
        resp = await self.client.post(
            "http://127.0.0.1:8081/v1/chat/completions",
            json={
                "messages": [
                    {"role": "system", "content": "判断用户意图，仅输出：chat/generation/other"},
                    {"role": "user", "content": text}
                ],
                "max_tokens": 5,
                "temperature": 0.1
            }
        )
        result = resp.json()["choices"][0]["message"]["content"].strip().lower()

        intent_map = {
            "chat": TaskType.CHAT,
            "generation": TaskType.GENERATION,
            "other": TaskType.CHAT
        }
        return intent_map.get(result, TaskType.CHAT)

    async def route(self, text: str) -> dict:
        """主路由方法"""
        # 1. 安全审核（所有请求必经）
        guard_result = await self._call_model(TaskType.GUARD, text)
        if guard_result.get("flagged"):
            return {"error": "content_flagged", "detail": guard_result}

        # 2. 意图分类
        intent = await self.classify_intent(text)

        # 3. 路由到对应模型（带降级）
        return await self._call_with_fallback(intent, text)

    async def _call_model(self, task_type: TaskType, text: str) -> dict:
        """调用指定类型的模型"""
        candidates = self.registry.get(task_type, [])
        for route in sorted(candidates, key=lambda r: r.priority):
            try:
                resp = await asyncio.wait_for(
                    self.client.post(
                        f"{route.model_endpoint}/v1/chat/completions",
                        json={
                            "messages": [{"role": "user", "content": text}],
                            "max_tokens": 1024,
                            "temperature": 0.7
                        }
                    ),
                    timeout=route.timeout_ms / 1000
                )
                return resp.json()
            except Exception as e:
                if route.priority == candidates[-1].priority:
                    raise  # 所有候选都失败
                continue  # 尝试下一个候选模型
```

### 6.3 多模型编排模式

**模式一：串行管道（Pipeline）**

适用于有明确先后顺序的任务。

```
输入 → [安全审核] → [意图分类] → [知识检索] → [回答生成] → [输出审核] → 输出
         Guard       Router       RAG          Chat         Guard
```

```python
async def pipeline_process(user_input: str):
    # 每个阶段独立处理，互不阻塞
    stages = [
        ("guard_in", guard_model),
        ("classify", classifier_model),
        ("retrieve", vector_db),     # 非模型环节
        ("generate", chat_model),
        ("guard_out", guard_model),
    ]

    context = {"input": user_input}
    for stage_name, handler in stages:
        try:
            context = await handler.process(context)
        except Exception as e:
            return fallback_response(stage_name, e)

    return context["output"]
```

**模式二：并行投票（Ensemble）**

适用于需要高准确率的分类/判断任务。

```
输入 → ┌─ 模型 A ─┐
       ├─ 模型 B ─┼→ 投票 → 输出
       └─ 模型 C ─┘
```

**模式三：分工协作（Specialist）**

适用于复杂文档处理。

```
输入（长文档）
    │
    ├──→ [摘要模型]  → 文档摘要
    ├──→ [关键词提取] → 标签列表
    ├──→ [实体识别]  → 人名/地名/日期
    ├──→ [情感分析]  → 情感倾向
    └──→ [翻译模型]  → 多语言版本
    │
    └──→ [聚合] → 结构化输出
```

### 6.4 模型注册与发现

当模型数量超过 5 个，手动管理端点地址会变得混乱。引入服务发现：

```yaml
# models-registry.yaml
models:
  classifier-intent:
    endpoint: http://127.0.0.1:8081
    type: classification
    model: qwen2.5-3b-instruct
    quant: Q4_K_M
    max_concurrency: 10

  chat-agent:
    endpoint: http://127.0.0.1:8082
    type: chat
    model: qwen2.5-7b-instruct-cs-lora
    quant: Q5_K_M
    max_concurrency: 5
    fallback: chat-agent-backup

  chat-agent-backup:
    endpoint: http://127.0.0.1:8084
    type: chat
    model: qwen2.5-3b-instruct
    quant: Q4_K_M
    max_concurrency: 20

  writer-agent:
    endpoint: http://127.0.0.1:8083
    type: generation
    model: qwen2.5-14b-instruct
    quant: Q4_K_M
    max_concurrency: 3

  embedder:
    endpoint: http://127.0.0.1:8085
    type: embedding
    model: bge-large-zh-v1.5
    quant: Q4_K_M
    max_concurrency: 50

  guard:
    endpoint: http://127.0.0.1:8086
    type: guard
    model: qwen2.5-0.5b-guard-lora
    quant: Q4_K_M
    max_concurrency: 100
```

### 6.5 典型团队配置方案

**方案 A：电商客服团队（低成本起步）**

| 角色 | 模型 | 硬件 | 说明 |
|------|------|------|------|
| 意图路由器 | Qwen2.5-3B | CPU | 分类速度快，不占 GPU |
| 客服对话 | Qwen2.5-7B + LoRA | 1× RTX 3060 12GB | 主力对话模型 |
| 安全审核 | Qwen2.5-0.5B + LoRA | CPU | 轻量级敏感词过滤 |
| 语义检索 | BGE-Small-1.5 | CPU | 知识库检索 |

**总硬件成本**：约 8,000-10,000 元（一台带 RTX 3060 的主机）

**方案 B：内容创作团队（质量优先）**

| 角色 | 模型 | 硬件 | 说明 |
|------|------|------|------|
| 长篇写作 | Qwen2.5-14B + LoRA | 1× RTX 4090 24GB | 高质量内容生成 |
| 标题/摘要 | Qwen2.5-7B + LoRA | 同上 GPU（分时复用） | 辅助创作 |
| 配图生成 | Stable Diffusion XL | 同上 GPU | 文章配图 |
| 排版审核 | Qwen2.5-3B | CPU | 格式检查、错别字 |

**总硬件成本**：约 18,000-25,000 元（一台带 RTX 4090 的主机）

**方案 C：企业级全功能团队**

| 角色 | 模型 | 硬件 | 说明 |
|------|------|------|------|
| 通用对话 | Qwen2.5-32B / DeepSeek-V3 | 2× RTX 4090 或 A6000 | 核心对话能力 |
| 代码助手 | DeepSeek-Coder-33B | 1× A6000 48GB | 代码生成与审查 |
| 数据分析 | Qwen2.5-72B | 2× A6000 或 A100 | 复杂推理 |
| 客服 Bot | Qwen2.5-7B × 2 实例 | 1× RTX 4090 | 高并发客服 |
| 安全审核 | Qwen2.5-1.5B | CPU | 内容安全 |
| 多模态 | Qwen2.5-VL-7B | 1× RTX 4090 | 图片理解 |
| 嵌入服务 | BGE-Large-1.5 | CPU | RAG 知识库 |
| 语音转写 | Whisper-Large-v3 | 1× RTX 3060 | 语音输入 |

---

## 七、实施路线图：从 0 到 1 的四周计划

### 第一周：基础设施搭建

```
目标：一个模型跑起来，能通过 API 调用
```

- [ ] **Day 1-2**：选型决策
  - 确定 2-3 个最痛的业务场景
  - 对照 2.1 决策表选择基座模型
  - 确定硬件方案（自建 / 云 GPU）

- [ ] **Day 3-4**：环境部署
  - 安装 CUDA、编译 llama.cpp 或部署 vLLM
  - 下载 GGUF 模型，测试推理
  - 启动 llama-server，验证 API 可用

- [ ] **Day 5**：基础封装
  - 写一个最简单的 Python 客户端调用 API
  - 测试 5 个真实业务 query，记录效果

- [ ] **Day 6-7**：建立基线
  - 收集 20 条典型测试用例
  - 手动打分，建立效果基线
  - 记录延迟、吞吐量等性能基线

**第一周交付物**：一个可用的模型 API + 效果基线报告

### 第二周：数据与微调

```
目标：微调出第一个定制模型，效果明显优于基座
```

- [ ] **Day 8-9**：数据准备
  - 按 4.2 方法构造 200-500 条微调数据
  - 10% 作为测试集，90% 作为训练集
  - 数据质量人工抽检（至少抽 20%）

- [ ] **Day 10-11**：微调执行
  - 用 LLaMA-Factory 或 Unsloth 执行 LoRA 微调
  - 监控 loss 曲线，防止过拟合
  - 保存 2-3 个中间 checkpoint

- [ ] **Day 12-13**：评估对比
  - 在测试集上对比基座模型 vs 微调模型
  - 用 LLM-as-Judge 做自动评分
  - 人工抽检 20 条，确认改善方向正确

- [ ] **Day 14**：导出部署
  - 合并 LoRA 权重，量化为 GGUF
  - 替换原有模型，重新启动服务
  - 跑一遍回归测试

**第二周交付物**：微调模型 + 评估对比报告

### 第三周：多模型编排

```
目标：搭建路由层，实现至少 2 个模型的协同工作
```

- [ ] **Day 15-16**：路由层开发
  - 实现 6.2 中的智能路由核心逻辑
  - 接入意图分类模型
  - 实现基本降级策略

- [ ] **Day 17-18**：部署第二个模型
  - 确定第二个场景（如安全审核/写作助手）
  - 重复第一周的部署流程
  - 注册到路由层

- [ ] **Day 19-20**：串联测试
  - 测试端到端流程：输入 → 路由 → 模型 A → 输出
  - 测试降级场景：模型 A 挂了 → 自动切换模型 B
  - 测试并发：模拟 10 个用户同时请求

- [ ] **Day 21**：监控接入
  - 接入 Prometheus 指标采集
  - 搭建 Grafana 基础看板（延迟、QPS、错误率）
  - 配置告警规则（延迟 > 3s、错误率 > 5%）

**第三周交付物**：多模型协同系统 + 监控看板

### 第四周：上线与迭代

```
目标：正式接入业务，建立迭代闭环
```

- [ ] **Day 22-23**：灰度上线
  - 10% 流量切到新系统
  - 监控核心指标（延迟、错误率、用户反馈）
  - 对比新旧系统效果

- [ ] **Day 24-25**：问题修复
  - 收集灰度期间 bad case
  - 快速修复（Prompt 调整 / 规则补丁）
  - 逐步扩大流量到 50%

- [ ] **Day 26-27**：全量上线
  - 100% 流量切换
  - 持续监控 48 小时
  - 准备回滚方案（保留旧系统热备）

- [ ] **Day 28**：复盘与规划
  - 输出效果报告（业务指标 + 技术指标）
  - 整理 bad case 库，规划下月优化方向
  - 评估是否需要增加模型或升级硬件

**第四周交付物**：上线系统 + 效果复盘报告 + 下月迭代计划

---

## 八、附录：工具链与资源索引

### 推理部署

| 工具 | 用途 | 链接 |
|------|------|------|
| llama.cpp | CPU/GPU 混合推理，GGUF 格式 | github.com/ggml-org/llama.cpp |
| vLLM | 高并发 GPU 推理，PagedAttention | github.com/vllm-project/vllm |
| Ollama | 一键部署，适合个人开发 | ollama.com |
| Text Generation Inference | HuggingFace 官方推理服务 | github.com/huggingface/text-generation-inference |
| SGLang | 结构化生成，RadixAttention | github.com/sgl-project/sglang |

### 微调工具

| 工具 | 适用对象 | 链接 |
|------|---------|------|
| LLaMA-Factory | 新手到进阶，Web UI + CLI | github.com/hiyouga/LLaMA-Factory |
| Unsloth | 追求速度，2-5x 加速 | github.com/unslothai/unsloth |
| Axolotl | 进阶用户，配置灵活 | github.com/axolotl-ai-cloud/axolotl |
| transformers + PEFT | 最大控制力 | huggingface.co/docs/peft |

### 数据与评估

| 工具 | 用途 | 链接 |
|------|------|------|
| Label Studio | 数据标注平台 | labelstud.io |
| Argilla | 数据管理与反馈收集 | github.com/argilla-io/argilla |
| LangFuse | LLM 可观测性与评估 | langfuse.com |
| DeepEval | 单元测试风格评估框架 | github.com/confident-ai/deepeval |
| Ragas | RAG 系统评估 | github.com/explodinggradients/ragas |

### 向量数据库

| 工具 | 适用规模 | 链接 |
|------|---------|------|
| Chroma | 开发/小规模 | trychroma.com |
| Qdrant | 中型生产 | qdrant.tech |
| Milvus | 大规模生产 | milvus.io |
| FAISS | 嵌入式/高性能 | github.com/facebookresearch/faiss |

### 监控与运维

| 工具 | 用途 | 链接 |
|------|------|------|
| Prometheus + Grafana | 指标采集与可视化 | prometheus.io / grafana.com |
| LangFuse | LLM 专用追踪与监控 | langfuse.com |
| Weights & Biases | 训练实验追踪 | wandb.ai |

### 推荐模型速查

| 模型 | 参数量 | 擅长领域 | HuggingFace ID |
|------|--------|---------|----------------|
| Qwen2.5-Instruct | 0.5B-72B | 中英文通用，代码 | `Qwen/Qwen2.5-7B-Instruct` |
| Qwen3 | 0.6B-235B | 中英文，推理增强 | `Qwen/Qwen3-8B` |
| DeepSeek-V3 | 671B MoE | 推理/代码/数学 | `deepseek-ai/DeepSeek-V3` |
| DeepSeek-Coder-V2 | 16B-236B | 代码生成 | `deepseek-ai/DeepSeek-Coder-V2` |
| Llama 4 | 17B-109B | 英文通用 | `meta-llama/Llama-4-Maverick-17B` |
| Gemma 3 | 1B-27B | 多语言轻量 | `google/gemma-3-12b-it` |
| BGE-M3 | 0.5B | 多语言嵌入 | `BAAI/bge-m3` |
| BGE-Large-zh | 0.3B | 中文嵌入 | `BAAI/bge-large-zh-v1.5` |
| Qwen2.5-VL | 3B-72B | 多模态理解 | `Qwen/Qwen2.5-VL-7B-Instruct` |
| FunASR / Whisper | — | 语音识别 | `openai/whisper-large-v3` |

---

## 写在最后

搭建 AI 团队这件事，本质上不是技术问题，是工程判断问题：

- **什么时候该微调，什么时候用 Prompt 就够了？** —— 数据说了算，不是直觉
- **模型大了好还是多了好？** —— 一个 72B 通用模型不如 3 个 7B 专用模型配合
- **什么指标才算"好"？** —— 业务指标，不是榜单分数

你不需要成为 AI 研究员。你需要的是一个工程师的务实态度：**让模型在具体业务里发挥作用，而不是追求通用能力的极致。**

这份指南里的每一段代码、每一个配置、每一个架构决策，背后都是"这样做的团队少踩了坑"。希望你在搭建自己的 AI 团队时，能少走我们走过的弯路。

---

*编写日期：2026 年 6 月*
*适用对象：具备基础开发能力，熟悉 Python 和 Linux 命令行的开发者*
*配套文档：[AI 零基础入门指南](./ai-beginner-guide.md) | [llama.cpp 部署教程](./llama_cpp_deploy_guide.md)*

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
| **入门** | Windows PC + RTX 4060 8GB / Mac Mini M4 24GB | Qwen3.5-9B（Q4，~6.5GB 显存） | ¥5,000-8,000 |
| **进阶** | 单卡 RTX 4090 24GB | Qwen3.5-27B / Qwen3-Coder-30B（MoE，满血量化） | ¥18,000 |
| **专业** | 双卡 RTX 4090 / Mac Studio 192GB | Qwen3.5-397B（量化）/ 多模型并行 Agent 团队 | ¥35,000-55,000 |

> **MoE 是什么？** Qwen3-Coder-30B 是混合专家架构——30B 参数总量，但每次推理只激活其中的 3.3B。相当于 30B 模型的知识量，3.3B 模型的推理速度。但注意：**全部 30B 权重仍需加载到显存**，所以入门 8GB 卡跑不了它，需要 24GB 才行。入门方案用 Qwen3.5-9B 就够了。

**入门级就够了。** 一块 RTX 4060 8GB 跑 Qwen3.5-9B Q4 量化版，延迟 5-8 秒/响应，日常编码辅助完全够。不需要一上来就上 RTX 4090。

---

## 四个 Developer Agent，各自干什么

### 编码 Agent：你的主力程序员

角色设定很简单：你是全栈工程师，精通 TypeScript/Python/Go。每次写代码前，先去本地向量库（ChromaDB）检索项目里相关的代码片段，自动遵循已有的命名规范和架构模式。

不确定的设计决策标注为 `// TODO: DECISION -` 留给你做选择。

用 Qwen3-Coder-30B（MoE 架构，Q4 量化），本地跑，零成本。

### 审查 Agent：你的 Code Reviewer

自动 Review 每一个 PR。检查清单：SQL 注入、XSS 漏洞、空指针、N+1 查询、硬编码密钥。输出分三档：🔴 必须修改 / 🟡 建议优化 / 🟢 仅供参考。

它不能替代你的判断。但有了这份清单，你看代码的时间从 20 分钟降到 5 分钟——因为不需要逐行找问题，只需要确认它找到的问题是否属实。

### 测试 Agent：自动补测试

根据 PR 的代码变更，自动生成单元测试。每个测试标注设计意图——"测试边界：空数组输入""测试异常：网络超时"——不是 `assert 1+1==2` 这种垃圾用例。

### 文档 Agent：再也不用手写 API 文档

代码合并后自动更新 API 文档、追加 CHANGELOG、生成架构决策记录。你只管写码，文档它能自己跟上。

---

## 怎么让它们跑起来：本地 Agent 服务 + Webhook

先说一个踩过的坑：**直接用 GitHub Actions 调 ollama generate，这条路走不通。**

为什么？ollama generate 返回的只是纯文本。它不会读项目文件、不知道目录结构、不能操作 git、更别提创建规范的分支和 PR 了。你需要的是一个**能读文件系统、会 git 操作、理解项目上下文**的 Agent 框架。

目前最成熟的开源本地方案是 **OpenClaw + Ollama**。

---

### 第一步：在 Windows 上装 Ollama

去 [ollama.com](https://ollama.com) 下载 Windows 安装包，一路下一步就行。装好后打开 PowerShell 验证：

```powershell
ollama --version
# 输出: ollama version 0.17.x
```

拉两个模型——一个主力编码，一个做轻量任务：

```powershell
# 主力：Qwen3-Coder，MoE 架构，30B 参数 / 3.3B 激活
ollama pull qwen3-coder:30b

# 轻量备选：Qwen3.5 9B，日常问答、文档生成够用
ollama pull qwen3.5:9b
```

下载完验证一下：

```powershell
ollama list
# NAME                  ID              SIZE      MODIFIED
# qwen3-coder:30b       abc123def456    19 GB     2 days ago
# qwen3.5:9b            xyz789abc012    5.9 GB    2 days ago
```

---

### 第二步：装 Agent 框架 —— 让模型"能动起来"

模型只会说话，Agent 才会干活。OpenClaw 是目前 Windows 上对 Ollama 支持最好的本地编程 Agent，原生支持文件读写、shell 命令、git 操作、GitHub API。

```powershell
# 安装 OpenClaw（需要先装 Node.js 18+）
npm install -g openclaw

# 初始化 —— 交互式选择后端为 Ollama
openclaw init

# 启动 Agent 服务，绑定 Qwen3-Coder
openclaw serve --model ollama/qwen3-coder:30b
```

启动后，OpenClaw 会在本机 `http://localhost:18765` 提供一个 REST API。任何程序都可以通过 HTTP 请求来驱动它干活。

---

### 第三步：搭 Webhook 桥梁 —— GitHub Issue → 自动编码

整个链路是这样的：

```
GitHub Issue 打标签 → Webhook POST → 本机 Flask 接收 → 调 OpenClaw API → Agent 写码+提 PR
```

**① 先写 Webhook 接收器**

在你项目里新建一个 `webhook_server.py`：

```python
# webhook_server.py
from flask import Flask, request
import requests
import json

app = Flask(__name__)
AGENT_URL = "http://localhost:18765/api/task"

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    payload = request.json
    action = payload.get('action', '')
    issue = payload.get('issue', {})
    labels = [lb['name'] for lb in issue.get('labels', [])]

    # 只响应"刚打上 ai-dev 标签"的事件
    if action != 'labeled' or 'ai-dev' not in labels:
        return 'skip', 200

    repo = payload['repository']
    task_prompt = (
        f"## 仓库: {repo['full_name']}\n"
        f"## 需求标题: {issue['title']}\n"
        f"## 需求描述:\n{issue['body']}\n\n"
        "请：1. clone 仓库 2. 分析现有代码结构 3. 实现需求 "
        "4. 创建新分支 5. commit 并 push 6. 通过 GitHub CLI 创建 PR"
    )

    r = requests.post(AGENT_URL, json={
        'prompt': task_prompt,
        'repo_url': repo['clone_url']
    }, timeout=5)

    print(f"[{issue['title']}] Agent 已触发: {r.status_code}")
    return 'ok', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4567)
```

**② 起服务**

开三个 PowerShell 窗口：

```powershell
# 窗口1：Ollama（通常开机自启，不用管）
ollama serve

# 窗口2：OpenClaw Agent
openclaw serve --model ollama/qwen3-coder:30b

# 窗口3：Webhook 接收器
pip install flask requests
python webhook_server.py
```

**③ 内网穿透（让 GitHub 能调到你本机）**

GitHub 的 Webhook 需要公网可达的 URL。用 ngrok 把本机 4567 端口暴露出去：

```powershell
# 去 ngrok.com 注册（免费），下载 ngrok.exe，然后：
ngrok http 4567
# 会输出一个公网地址：
# Forwarding  https://xxxx.ngrok-free.app -> http://localhost:4567
```

然后在 GitHub 仓库 Settings → Webhooks → Add webhook：
- Payload URL: `https://xxxx.ngrok-free.app/webhook`
- Content type: `application/json`
- Events: 勾选 **Issues**

---

### 工作流全景回放

现在，你在 GitHub 上创建一个 Issue，打上 `ai-dev` 标签：

1.  GitHub 发送 Webhook → ngrok 转发 → 本机 Flask 收到
2.  Flask 提取 Issue 标题和描述 → 拼成任务指令 → POST 到 OpenClaw
3.  OpenClaw 拉取仓库代码、分析结构、调用 Ollama 推理
4.  OpenClaw 生成代码文件 → `git checkout -b` → `git commit` → `git push`
5.  OpenClaw 调 GitHub API → 创建 Pull Request
6.  PR 创建后，审查/测试/文档 Agent 可以再并行触发一轮

**你从头到尾只需要做一件事：写 Issue 描述，打标签，等 PR。剩下的全自动。**

> 💡 运维提示：ngrok 免费版地址每 2 小时会变。生产环境建议用 frp 做内网穿透，或者直接在云服务器上跑 Agent（代码通过 VPN 拉取本地仓库）。

---

## 两个新手最容易踩的硬件坑

### 坑一：显存不够硬跑

公式很简单：**模型大小 × 量化系数 + 上下文开销 ≈ 显存需求**

- Qwen3.5-9B @ Q4 → 9B × 0.5 = 4.5GB + 上下文 ~2GB = **~6.5GB**（8GB 显卡稳稳的）
- Qwen3-Coder-30B（MoE）@ Q4 → 30B × 0.5 = 15GB + 上下文 ~4GB = **~19GB**（需要 24GB 卡）
- Qwen3.5-27B @ Q4 → 27B × 0.5 = 13.5GB + 上下文 ~4GB = **~17.5GB**

> ⚠️ 注意 MoE 模型的坑：虽然推理时只激活 3.3B 参数，但全部 30B 权重必须加载到显存中。所以 Qwen3-Coder-30B 的显存需求看 30B，不是 3.3B。

一条铁律：**模型显存占用不超过总显存的 70%**。剩下 30% 是给上下文和系统的。

别在 24GB 显卡上跑 Qwen3.5-397B——量化到 Q2 质量变成傻子，不如用 27B 的 Q5。

### 坑二：上下文无限拉满

PR diff 塞 10000 行进去 → OOM。解法：截断到 8000 字符，或分层摘要——先用小模型（Qwen3.5-9B）提取变更摘要+5 个关键片段，再送给大模型（Qwen3-Coder-30B）。

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

1. 去 [ollama.com](https://ollama.com) 下载 Windows 安装包→ 装好 → PowerShell 跑 `ollama pull qwen3.5:9b` → 五分钟用上最新本地编码模型
2. 在 VS Code / Cursor 里把 Model 切到 `ollama/qwen3.5:9b`，感受一下本地推理的速度——延迟不到 5 秒
3. 随便写个需求描述，让它在本地生成代码，看质量如何

如果感觉不错，下周搭 Webhook 链路，再下周上 ChromaDB 做代码库 RAG。一步一个脚印，别一上来就追集群方案。

---

*下一篇见。AI 团队搭起来之后才是真正的开始——怎么监控它有没有退步？什么时候该换模型？Prompt 怎么管才不乱？下一篇写长期运维。*

*你现在本地跑什么模型？遇到过 OOM 吗？评论区聊聊。*

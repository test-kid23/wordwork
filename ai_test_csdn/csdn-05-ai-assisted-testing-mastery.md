# AI 辅助测试工程实战：从"会用"到"拿涨薪"，8 周能力提升路线


> 只会用 ChatGPT 问"怎么写测试用例"的人，和能用 Agent 接管整条测试流水线的人，差的不只是效率——是 20%-35% 的薪资溢价。


我上次那篇文章里提了三条赛道，后台好几个人问："赛道一具体怎么搞？AI 测试工程到底要学什么？学多久能见效？"

这篇就是回答。

不分叉、不列几十项技能清单。**就盯着一件事讲清楚：一个普通测试工程师，怎么用 8 周时间把 AI 能力从"偶尔问问 ChatGPT"推进到"能搭一套 AI 辅助测试流水线"，让自己的市场定价跳一档。**

我写的内容都是我自己用过、踩过坑、再改过才确认可行的。有地方没把握的我会直接说"这个我还没试过，你谨慎参考"。

---

## 一、先搞清楚：AI 辅助测试到底能帮你干什么

网上很多文章把"AI 测试"说得玄乎——好像 AI 能自动发现 Bug、自动写所有用例、自动发布上线。

别信。

目前（2026 年中）AI 辅助测试的真实能力边界是这样的：

| 能做的事 | 效果 | 不能做/做不好的事 |
|---------|------|-----------------|
| 根据接口文档生成测试脚本 | 准确率 80%-95%，需人工审核 | 自己理解不清晰的业务逻辑 |
| 根据需求文档设计测试用例 | 覆盖度比人高 30%，但需人工筛选 | 替代你对业务风险的判断 |
| 分析失败日志定位根因 | 常见错误秒级定位 | 涉及多系统联动的复杂 Bug |
| 自动修复简单的 locator 失效 | DOM 变更不大的场景很稳 | 页面大改版后的重构 |
| 生成测试报告和缺陷描述 | 省 80% 文案时间 | 需要你补充分析结论 |
| 批量生成参数化测试数据 | 比手工快 10 倍 | 数据需要你验证合理性 |

换句话说：**AI 放大的是你的"手速"和"广度"，不替代你的"判断力"和"深度"。**

你技术越强，AI 能帮你做的事越多。你技术弱，AI 就只是一个搜索引擎。

---

## 二、你现在的水平在哪一级？（先诊断再动手）

在开始学之前，先诚实地给自己定个位。别一上来就想搭 Agent 流水线，大部分人连 Prompt 都还没写对。

| 级别 | 典型表现 | 市场薪资参考（2026） |
|------|---------|-------------------|
| **L0：零 AI** | 没用过或只偶尔搜问题。写脚本全靠手敲和搜索引擎 | 传统测试岗基线 |
| **L1：工具用户** | 会用 ChatGPT/Claude 聊天界面问"怎么写这个测试"，复制粘贴结果 | 溢价 0%-5% |
| **L2：Prompt 工程** | 能设计结构化 Prompt，指定框架、断言标准、异常覆盖。结果基本可用，差距在细节 | 溢价 8%-15% |
| **L3：工作流集成** | 把 AI 嵌入到 IDE（CodeBuddy/Claude Code/Cursor）里，让 AI 读项目文件再生成。审核效率高 | 溢价 15%-25% |
| **L4：Agent 编排** | 用 Agent 串联"需求→用例→脚本→执行→诊断→报告"全流程。人只做决策和审核 | 溢价 25%-35% |
| **L5：体系搭建** | 为团队搭建 AI 测试中台，包含知识库、Agent 中心、流程编排。定义团队工作方式 | 溢价 35%+ |

**大部分测试工程师卡在 L1→L2 这一步。** 不是学不会 Prompt 工程，而是没意识到"随便问"和"写好 Prompt"之间的效果差距有多大。

举个例子。同样让 AI 写一个注册接口的测试用例——

L1 的 Prompt：
> 帮我写一个用户注册接口的测试用例

AI 大概率给你一个只测 200 的脚本，断言笼统，没有异常覆盖。

L2 的 Prompt：
> 用 pytest + requests，给 POST /api/user/register 写测试用例。参数：username（3-20字符）、password（6-20字符）、email（邮箱格式）。覆盖：正常注册、用户名过短、密码过短、邮箱格式错误、重复注册。断言分层：先状态码、再 code 字段、再 data 字段。测试数据从 conftest.py 的 fixture 读。

结果完全不同——AI 会给你一个直接能用的、有 5+ 个测试方法的、断言规范的完整文件。

**就从 L1 到 L2 这一步，你的产出质量直接跳一档。** 下面讲怎么做。

---

## 三、第 1-2 周：Prompt 工程——让 AI 输出"能用的"测试代码

### 3.1 测试用例 Prompt 的六个必备要素

我试了无数次之后，总结出一个规律：**测试用例的 Prompt 缺了下面任一个要素，输出质量都会大打折扣。**

```
要素 1：明确技术栈（框架 + 语言 + 版本）
要素 2：被测对象的具体信息（接口地址/页面 URL、参数、响应结构）
要素 3：覆盖场景清单（正常 + 异常 + 边界值，列具体场景不要只说"全覆盖"）
要素 4：断言标准（分层断言，说清楚每层检查什么）
要素 5：代码规范要求（架构约定、数据读取方式、命名规则）
要素 6：质量要求（异常处理、日志、独立性）
```

### 3.2 实战：一个能直接用的 Prompt 模板

下面这个模板你直接改接口信息就能用：

```
你是一个资深测试开发工程师。请用 Python + pytest + requests 为以下接口生成完整测试用例。

## 被测接口
- 方法：POST
- URL：https://api.example.com/v1/product/create
- Headers：Content-Type: application/json; Authorization: Bearer {token}
- 请求体：
  {
    "name": "string(1-50字符，必填)",
    "category_id": "int(必填)",
    "price": "float(>=0.01，必填)",
    "stock": "int(>=0，必填)",
    "description": "string(可选，最长500字符)"
  }
- 成功响应：{"code": 200, "data": {"product_id": int}, "msg": "ok"}
- 错误响应格式：{"code": 错误码, "msg": "错误描述", "data": null}

## 覆盖场景
正常场景：
1. 所有必填参数合法 → 200，返回 product_id 为正整数
2. description 填满 500 字符 → 200

异常场景：
3. name 为空 → 400
4. name 超过 50 字符 → 400
5. category_id 不存在 → 400
6. price 为负数 → 400
7. price 为 0 → 400
8. stock 为负数 → 400
9. 缺少 Authorization header → 401
10. token 过期 → 401
11. 请求体为空 → 400
12. 请求体不是 JSON → 415
13. name 包含 SQL 注入字符（' OR '1'='1）→ 400
14. name 包含 XSS 脚本（<script>alert(1)</script>）→ 200 或 400（需安全转义）
15. 请求体多余字段 → 200（向后兼容，多余字段忽略）

边界值：
16. name 恰好 1 字符 → 200
17. name 恰好 50 字符 → 200
18. price 为 0.01 → 200
19. price 为 999999.99 → 200
20. stock 为 0 → 200
21. stock 为 2147483647（int32 上限）→ 200
22. description 恰好 500 字符 → 200
23. description 501 字符 → 400

## 断言标准（分层）
第一层：resp.status_code == 预期值
第二层：resp.json()["code"] == 预期值
第三层：对成功场景，resp.json()["data"]["product_id"] > 0
第四层：对失败场景，resp.json()["msg"] 不为空且包含关键错误描述

## 代码规范
- 使用 @pytest.fixture 管理 token 获取和清理
- 所有测试数据从 conftest.py 或 fixtures/data.py 读取
- 类名 TestProductCreate，方法名 test_create_product_xxx
- 每个方法加 docstring 说明场景
- 失败时用 pytest.fail() 输出完整请求体和响应体
- 测试完成后删除创建的测试数据（teardown）
- 异常用例用 pytest.raises 或 try/except 避免测试框架报错

## 质量要求
- 所有方法独立，无执行顺序依赖
- 敏感信息（token、密码）不硬编码
- 不加冗余的 print 调试语句
- 生成 Parametrize 避免重复代码
```

你把这个 Prompt 扔给 Claude 或 GPT-4，拿到的结果大概率是一个结构良好、断言分层、异常覆盖到位的测试文件。你只需要审核几个地方——数据是不是你预期的那样、异常场景有没有漏的、业务逻辑有没有理解偏的。

### 3.3 同一个 Prompt 在不同模型里的表现差异（我实测的）

| 工具 | 亮点 | 短板 | 我的评价 |
|------|------|------|---------|
| **Claude 3.5/4** | 代码结构最清晰，断言分层理解最好。docstring 写得比我自己都好 | 偶尔漏掉边界值的 Parametrize | 写测试用例的首选，80% 场景用它 |
| **GPT-4o** | 异常场景覆盖最全面，边界条件总能多想几个 | 代码风格偏啰嗦，有时候多写不需要的类 | 让它帮你想漏掉的场景，别让它写最终版 |
| **DeepSeek** | 国内免费可用，代码生成质量接近 Claude，中文理解特别好 | 偶尔在复杂分层断言上不够细腻 | 零成本起步的最佳选择，不花钱也能练 |

**如果你预算有限，或者还没说服公司报销 API 费用**——DeepSeek 完全够你练完前四周的所有内容。我用同一个 Prompt 测过，DeepSeek 生成的代码结构 90% 的场景跟 Claude 差距不大，主要差在极复杂断言的分层处理和 docstring 的精细度上。这两项差异在你刚开始练的时候体会不到，等你到第 5-6 周做失败诊断的时候才会开始在意。

**我的建议**：
- **零成本路线**：DeepSeek 全程，前四周完全够用。第五周开始如果觉得不够精细，再切 Claude。
- **预算充足路线**：Claude 写代码、GPT-4o 想场景、Gemini 消化大项目。三个配合着用，不要死磕一个。

---

## 四、第 3-4 周：让 AI 读你的项目——从"聊天框"升级到"IDE 内嵌"

前两周你学会了写 Prompt。但还有一个大问题——每次都要把项目规范、基类代码、已有用例这些上下文复制粘贴给 AI。

累，而且容易漏。

第三周开始，你要把 AI 集成到你的开发环境里，让它直接读你的项目文件。

### 4.1 三种工具的选择

| 工具 | 上手难度 | 核心能力 | 适合谁 |
|------|---------|---------|--------|
| **CodeBuddy** | ⭐ 最低 | IDE 内嵌 AI、Skills 机制、Automation 定时任务、MCP 协议扩展 | 所有人，尤其 Windows 用户和不想折腾配置的人 |
| **Claude Code** | ⭐⭐⭐ 较高 | 直接用 `@文件路径` 引用项目文件、/skill 自定义技能，命令行速度极快 | 习惯终端操作、已有 Claude API Key 的人 |
| **Cursor** | ⭐⭐ 中等 | Tab 自动补全很强、diff 审核方便 | 前端开发为主、已用 VS Code 的人 |

**我的真实推荐：如果你在国内、用 Windows，直接 CodeBuddy 起步。**

原因很朴素——

CodeBuddy 一键安装，Windows 打开即用，页面友好，**内置大模型 API，不用自己去搞什么 API Key 配置**。你从下载到写出第一个 AI 辅助的测试用例，不超过 10 分钟。

Claude Code 呢？你得先从 GitHub 拉取源码——很多人的网络不加速根本下载不下来，动不动就 timeout。好不容易装好了，还得自己去申请 Anthropic 的 API Key、绑信用卡充值、配环境变量……一套流程走下来，半小时起步，中间任何一个环节出问题你就卡住了。

**我不是说 Claude Code 不好——它命令行效率很高，重度使用的时候确实爽。** 但如果你的目标是"先上手用起来"，别跟安装配置较劲。CodeBuddy 是零摩擦的选择。等你把前三周的东西跑熟了，对 AI 辅助测试有手感了，想追求更极致的命令行体验，再切 Claude Code 也不迟。

Claude Code 里有个核心语法你要记住：**`@文件路径` 让 AI 读指定文件当上下文**。这个能力 CodeBuddy 也支持（直接把文件拖进对话或者 @ 引用）。

### 4.2 实操：用 `@文件路径` 生成项目级测试用例（CodeBuddy / Claude Code 通用）

假设你的项目结构是：

```
project/
├── core/base_api.py          # API 请求基类
├── conftest.py               # 全局 fixture
├── data/test_data.py         # 测试数据
├── tests/api/
│   ├── test_login.py         # 已有登录用例（作为风格参考）
│   └── test_order.py         # 待生成的订单用例
```

在 CodeBuddy 或 Claude Code 的输入框里输入：

```
@core/base_api.py 继承 BaseAPI 类
@conftest.py 使用 api_client fixture  
@data/test_data.py 测试数据从 order_test_data 变量读
@tests/api/test_login.py 保持相同代码风格

为 GET /api/v1/order/{order_id} 生成测试用例。

接口：
- 路径参数：order_id（string，必填）
- 响应：{"code": 200, "data": {"order_id", "status", "items", "total"}}

覆盖场景：正常查询、order_id 不存在返回 404、order_id 为空返回 400、无 token 返回 401
```

关键：**`@文件路径` 这个语法让 AI 读了你的项目文件之后才生成代码。** 生成的代码直接继承你项目的 BaseAPI、用你的 api_client fixture、风格跟你已有的 test_login.py 一致。

**这一步的价值**：之前你拿到 AI 生成的代码还要手动改基类引用、改 fixture 名称、调整代码风格——每次至少 15 分钟。现在一步到位，直接能用。

### 4.3 用 Skills 封装你的 Prompt 模板

你发现没？每次让 AI 生成测试用例，你都要重复说"断言要分层、测试数据从 data 目录读、方法要独立……"

**把这段固定要求封装成一个 Skill。**

在 CodeBuddy 或 Claude Code 里创建 `test-case-generator` skill：

```
你是一个测试用例生成专家。

每次生成用例时，必须遵守：
1. 继承 @core/base_api.py 的 BaseAPI
2. 使用 @conftest.py 的 api_client fixture
3. 断言分层：status_code → code → data → 业务字段
4. 覆盖：正常、异常（参数缺失/类型错误/权限不足）、边界值
5. 所有测试数据从 @data/test_data.py 读取
6. 方法独立无依赖，失败时输出完整请求和响应
7. 代码风格参考 @tests/api/test_login.py
```

之后每次只需要说 `/test-case-generator 给 /api/v1/user/update 写测试` 就行了。

这一步你省下的不只是改代码的时间——**你把"我团队的标准做法"变成了一个可复用的规则，AI 每次都在这个规则下工作。** 这就是从"用 AI 工具"到"管 AI 行为"的质变。

---

## 五、第 5-6 周：AI 辅助失败诊断——从"人肉 grep"到"秒级定位"

自动化用例跑挂了，打开 Jenkins 日志——3000 行。接下来你做什么？

大多数人是：
1. Ctrl+F 搜 "FAILED"
2. 找到断言失败那行
3. 往上翻，找请求和响应
4. 肉眼对比预期和实际
5. 猜可能原因
6. 改代码再跑

**我测过，平均一个失败用例要花 8-12 分钟定位。** 一天挂 10 个，两个小时没了。

### 5.1 让 AI 直接定位根因

你要做的不是让人去看日志，是把日志扔给 AI，让它帮你读。

这是我现在在用的 Prompt：

```
你是一个测试失败诊断专家。以下是 pytest 运行失败的完整日志。

请分析：
1. 哪几个用例失败了（列出用例名）
2. 每个失败用例的失败类型（断言失败/超时/连接错误/环境问题）
3. 对于断言失败：实际值和期望值的差异是什么？可能原因是什么？
4. 对于超时/连接错误：哪个服务或接口出问题了？
5. 有没有环境问题导致的失败（如测试数据未准备、服务未启动）？
6. 按优先级排序修复建议（P0 必须先修，P1 尽快修，P2 可以延后）

日志：
[粘贴完整 pytest 输出]
```

**效果**：原来 8-12 分钟一个，现在 1-2 分钟。而且 AI 经常能发现我忽略的关联问题——比如"这 3 个用例都挂了，看日志是同一个 token 过期了，不是用例的问题。"

### 5.2 更进一步：失败自动分类 + 证据链

等你把这个流程跑熟了，下一步是把失败诊断自动化：

```python
# 在 conftest.py 里加一个 hook
import json
from datetime import datetime

FAILURE_LOG_DIR = "test_failures"

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # 收集失败证据
        evidence = {
            "test_name": item.name,
            "test_file": str(item.path),
            "error_message": str(report.longrepr),
            "timestamp": datetime.now().isoformat(),
            "markers": [m.name for m in item.iter_markers()]
        }
        
        # 如果有 page/request fixture，把最后操作的上下文也存下来
        if hasattr(item, "_request_context"):
            evidence["last_request"] = item._request_context
        
        # 保存到文件
        case_dir = f"{FAILURE_LOG_DIR}/{item.name}"
        os.makedirs(case_dir, exist_ok=True)
        with open(f"{case_dir}/evidence.json", "w") as f:
            json.dump(evidence, f, indent=2, default=str)
```

然后写一个简单的分析脚本，把 `evidence.json` 批量喂给 AI：

```python
# analyze_failures.py
import json
import os
import anthropic  # 或 openai

client = anthropic.Anthropic()

failure_files = []
for root, dirs, files in os.walk("test_failures"):
    for f in files:
        if f == "evidence.json":
            filepath = os.path.join(root, f)
            with open(filepath) as fp:
                failure_files.append(json.load(fp))

# 合并所有失败证据
evidence_text = json.dumps(failure_files, indent=2, ensure_ascii=False)

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=2000,
    messages=[{
        "role": "user",
        "content": f"分析以下测试失败证据，按根因分组并给出修复建议：\n{evidence_text}"
    }]
)

print(response.content[0].text)
```

**把这个脚本挂在 CI 的最后一步**，每次跑完自动化，你打开的不是 3000 行日志，是一份 AI 写的失败诊断报告。

我一开始搭这个的时候犯过一个弱智错误——把所有失败用例的证据一股脑塞给 AI，token 超了，返回结果被截断。后来改成按失败类型分组、每批最多 5 个用例，问题就解决了。

---

## 六、第 7 周：用 AI Agent 串联测试全流程

前面六周你学会了：
- 写高质量 Prompt 生成测试代码
- 让 AI 读项目文件生成合规用例
- 用 AI 诊断测试失败

这些是一个一个的"点"。第 7 周的目标是把这些点串成一条线——**用 Agent 编排整条测试流水线。**

### 6.1 一条理想的 AI 测试流水线长什么样

```
需求文档/接口文档
    ↓ [Agent 读取]
生成测试计划（场景清单 + 优先级）
    ↓ [Agent 生成]
生成测试用例（pytest 代码）
    ↓ [Agent 审核]
代码审查（是否符合规范、断言是否分层）
    ↓ [人工确认 + 推送代码库]
执行测试（pytest 运行）
    ↓ [收集结果]
失败诊断（Agent 分析日志分类失败原因）
    ↓ [Agent 生成]
测试报告（html 报告 + 缺陷描述）
    ↓ [人工审核 + 补充分析]
归档到知识库（RAG 存储，下次复用）
```

**人的工作变成五个节点：确认测试计划、审核生成代码、确认执行范围、审核报告、补充分析结论。** 其他全部 Agent 做。

### 6.2 实操：用 Python 脚本串联 Agent 调用

市面上还没有完美的"一键式测试 Agent 平台"（那些号称有的基本都是半成品），但你可以自己用 Python 脚本把 Claude API 调用串起来。

下面是一个最简版本的工作流脚本，你改改就能用：

```python
"""
simple_test_agent.py — 最小化 AI 测试 Agent 流水线
依赖：pip install anthropic pytest
"""
import anthropic
import subprocess
import json
import os

client = anthropic.Anthropic()

class TestAgent:
    def __init__(self, api_doc_path: str, output_dir: str = "generated_tests"):
        self.api_doc_path = api_doc_path
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # 读取项目上下文
        with open(api_doc_path) as f:
            self.api_doc = f.read()
    
    def _call_claude(self, system_prompt: str, user_prompt: str) -> str:
        """统一的 Claude 调用封装"""
        resp = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        return resp.content[0].text
    
    # ===== Step 1: 生成测试计划 =====
    def generate_test_plan(self) -> str:
        system = """你是一个资深测试架构师。根据接口文档生成测试计划。
输出 JSON 格式：{"plan": [{"scenario": "场景名", "priority": "P0/P1/P2", "type": "normal/exception/boundary", "preconditions": "...", "steps": "...", "expected": "..."}]}"""
        
        user = f"根据以下接口文档生成完整测试计划，覆盖正常、异常、边界值场景：\n{self.api_doc}"
        
        plan = self._call_claude(system, user)
        with open(f"{self.output_dir}/test_plan.json", "w") as f:
            f.write(plan)
        return plan
    
    # ===== Step 2: 根据计划生成测试代码 =====
    def generate_test_code(self) -> str:
        with open(f"{self.output_dir}/test_plan.json") as f:
            plan = f.read()
        
        system = """你是 Python 测试开发专家。根据测试计划生成 pytest 代码。
规范：
- 使用 api_client fixture（已预定义）
- 断言分层：status_code → code → data
- 所有方法独立无依赖
- 失败时输出完整请求和响应
- 用 @pytest.mark.parametrize 减少重复代码
输出纯 Python 代码，不要加 markdown 代码块标记。"""
        
        user = f"根据以下测试计划生成 pytest 测试代码：\n{plan}\n\n接口文档：\n{self.api_doc}"
        
        code = self._call_claude(system, user)
        # 清理 AI 可能加的 markdown 标记
        code = code.replace("```python", "").replace("```", "").strip()
        
        filename = f"{self.output_dir}/test_generated.py"
        with open(filename, "w") as f:
            f.write(code)
        return filename
    
    # ===== Step 3: 代码审核 =====
    def review_code(self, code_file: str) -> dict:
        with open(code_file) as f:
            code = f.read()
        
        system = """你是代码审查专家。审查 pytest 测试代码，输出 JSON：
{"pass": true/false, "issues": [{"severity": "error/warning/info", "line": 行号, "problem": "问题描述", "fix": "修复建议"}], "summary": "一句话总结"}"""
        
        review = self._call_claude(system, f"审查以下 pytest 测试代码的质量：\n{code}")
        review_result = json.loads(review)
        
        with open(f"{self.output_dir}/code_review.json", "w") as f:
            json.dump(review_result, f, indent=2, ensure_ascii=False)
        
        return review_result
    
    # ===== Step 4: 执行测试 =====
    def run_tests(self, code_file: str) -> str:
        result = subprocess.run(
            ["pytest", code_file, "-v", "--tb=short"],
            capture_output=True, text=True, timeout=300
        )
        log_file = f"{self.output_dir}/test_run.log"
        with open(log_file, "w") as f:
            f.write(result.stdout + "\n" + result.stderr)
        return log_file
    
    # ===== Step 5: 失败诊断 =====
    def diagnose_failures(self, log_file: str) -> str:
        with open(log_file) as f:
            log = f.read()
        
        system = """你是测试失败诊断专家。分析 pytest 运行日志，输出 JSON：
{"total": 总数, "passed": 通过数, "failed": 失败数, "failures": [{"test": "用例名", "type": "断言失败/超时/环境问题/代码错误", "root_cause": "根因", "fix_suggestion": "修复建议", "priority": "P0/P1/P2"}]}"""
        
        diagnosis = self._call_claude(system, log)
        with open(f"{self.output_dir}/diagnosis.json", "w") as f:
            f.write(diagnosis)
        return diagnosis
    
    # ===== 完整流水线 =====
    def run_pipeline(self):
        print("=" * 50)
        print("Step 1/5: 生成测试计划...")
        self.generate_test_plan()
        print("✅ 测试计划已生成 → test_plan.json")
        
        print("\nStep 2/5: 生成测试代码...")
        code_file = self.generate_test_code()
        print(f"✅ 测试代码已生成 → {code_file}")
        
        print("\nStep 3/5: AI 代码审核...")
        review = self.review_code(code_file)
        if review.get("pass"):
            print("✅ 代码审核通过")
        else:
            issues = review.get("issues", [])
            error_count = sum(1 for i in issues if i.get("severity") == "error")
            print(f"⚠️ 发现 {len(issues)} 个问题（{error_count} 个严重），详见 code_review.json")
        
        print("\nStep 4/5: 执行测试...")
        log_file = self.run_tests(code_file)
        print(f"✅ 测试执行完成 → {log_file}")
        
        print("\nStep 5/5: AI 诊断失败...")
        diagnosis = self.diagnose_failures(log_file)
        print(f"✅ 诊断完成 → diagnosis.json")
        
        print("\n" + "=" * 50)
        print("流水线完成！输出文件：")
        for f in os.listdir(self.output_dir):
            print(f"  → {self.output_dir}/{f}")


# 使用
if __name__ == "__main__":
    agent = TestAgent(api_doc_path="docs/api_order.yaml")
    agent.run_pipeline()
```

**这个脚本的价值不在于代码多精妙——而在于你第一次拥有了"一条命令跑完测试全流程"的能力。**

跑一遍大概 3-5 分钟（取决于接口文档大小和 Claude API 响应速度）。你如果手工做同样的事情——看文档、写计划、写代码、审核、跑、分析——至少半天。

### 6.3 我的翻车经历：Agent 流程最容易踩的两个坑

**坑一：AI 生成代码没跑通就跑下一步。**

我最早写这个 Agent 的时候，Step 2 生成代码、Step 3 审核、Step 4 执行。结果经常到 Step 4 才发现代码有 import 错误——前面的审核完全没发现。

原因很简单：**AI 审核代码不会真的执行代码。** 它最多发现一些模式问题。

解法：在 Step 3 和 Step 4 之间加一个 `compile()` 检查。就一行：

```python
compile(code, code_file, 'exec')
```

编译不过的直接打回 Step 2 重新生成，不浪费后面时间。

**坑二：API 调用费用飙了。**

我一开始把整个项目文件都喂给 Claude 当上下文，每跑一次 pipeline 吃掉好几块钱。按每天跑 5 次算，一个月光 API 费用就几百块。

后来改成：只把关键的基类文件（BaseAPI、conftest、一个示例用例）放进 system prompt，接口文档按需加载。费用从每次 $0.8 降到 $0.15 左右。

**如果你的团队预算有限，前期先用 CodeBuddy（IDE 内嵌，按用户订阅不按 token 计费），不用直接调 API。**

---

## 七、第 8 周：搭建私有测试知识库（RAG）——让 AI 懂你的项目

到第七周末尾，你已经有了 AI 辅助的测试流水线。但它有一个致命局限——

**AI 不知道你的项目历史。**

它不知道哪些 Bug 反复出现、哪些模块是质量重灾区、你们团队的测试规范是什么、上次类似需求的用例怎么写的。

第八周的目标就是补上这个缺口——**搭建一个测试私有知识库。**

### 7.1 RAG 是什么（三句话说清）

RAG = Retrieval-Augmented Generation = 检索增强生成。

大白话：先把你的文档（需求文档、历史 Bug 库、测试规范、过往用例）切成小块存到向量数据库。每次向 AI 提问时，先从数据库检索最相关的几块，和你的问题一起发给 AI。**AI 的回答就有了项目上下文，不再是"通用回答"。**

### 7.2 搭一个最简版（30 分钟）

不需要搞什么 LangChain、LlamaIndex。用最基础的工具链：

```python
"""
build_test_rag.py — 搭建测试知识库的最简方案

依赖：pip install chromadb sentence-transformers anthropic
"""

import chromadb
from sentence_transformers import SentenceTransformer
import anthropic
import os
import glob

# ========== 1. 初始化 ==========
embedder = SentenceTransformer("all-MiniLM-L6-v2")  # 本地小模型，免费
chroma_client = chromadb.PersistentClient(path="./test_knowledge_db")
collection = chroma_client.get_or_create_collection("test_docs")

# ========== 2. 喂文档 ==========
def ingest_documents(doc_dir: str):
    """
    把目录下所有 .md / .txt / .py 文件切片存入向量库
    """
    for filepath in glob.glob(f"{doc_dir}/**/*", recursive=True):
        if not filepath.endswith((".md", ".txt", ".py")):
            continue
        
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        
        # 简单切片：每 1000 字符一块，重叠 200 字符
        chunks = []
        chunk_size = 1000
        overlap = 200
        for i in range(0, len(content), chunk_size - overlap):
            chunk = content[i:i + chunk_size]
            if len(chunk) < 100:  # 跳过太短的尾部
                continue
            chunks.append({
                "id": f"{filepath}_chunk_{i}",
                "text": chunk,
                "source": filepath
            })
        
        # 批量存入
        if chunks:
            collection.add(
                ids=[c["id"] for c in chunks],
                documents=[c["text"] for c in chunks],
                metadatas=[{"source": c["source"]} for c in chunks]
            )
        
        print(f"✅ {filepath} → {len(chunks)} 块")

# ========== 3. 查询 ==========
def query_test_knowledge(question: str, n_results: int = 5) -> str:
    """
    检索相关知识，拼接成上下文
    """
    # 用 embedding 模型把问题转成向量
    query_embedding = embedder.encode(question).tolist()
    
    # 从向量库检索最接近的 5 块
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    # 拼接成上下文
    context = "\n\n---\n\n".join(results["documents"][0])
    return context


# ========== 4. 使用知识库辅助 AI ==========
client = anthropic.Anthropic()

def ask_with_test_knowledge(question: str) -> str:
    """带着测试知识库上下文去问 AI"""
    context = query_test_knowledge(question)
    
    prompt = f"""你是一个资深测试工程师。以下是从项目测试知识库中检索到的相关文档：

---
{context}
---

基于以上上下文，请回答问题。如果上下文不足以回答，请明确说明。

问题：{question}"""
    
    resp = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.content[0].text


# ========== 使用示例 ==========
if __name__ == "__main__":
    # 第一步：把项目文档喂进去（只需执行一次，后面增量更新）
    ingest_documents("docs/requirements")     # 需求文档
    ingest_documents("docs/api_specs")        # API 文档  
    ingest_documents("docs/bug_history")      # 历史 Bug 库
    ingest_documents("docs/test_standards")   # 测试规范
    ingest_documents("tests/api")             # 已有测试用例（作为风格参考）
    
    # 第二步：带着知识库提问
    answer = ask_with_test_knowledge(
        "用户反馈支付成功后订单状态没更新，这个项目的订单状态机是怎么设计的？最近有没有类似的 Bug？应该重点测试哪些场景？"
    )
    print(answer)
```

### 7.3 知识库要喂什么？（按重要性排序）

| 优先级 | 文档类型 | 价值 |
|--------|---------|------|
| P0 | **API 接口文档**（OpenAPI/Swagger） | AI 生成用例的核心依据 |
| P0 | **现有测试用例代码** | 给 AI 做风格和架构参考 |
| P1 | **历史 Bug 库**（按模块分类） | 让 AI 知道哪些是重灾区，生成用例时重点覆盖 |
| P1 | **测试规范文档** | 断言标准、命名规范、PR 规范 |
| P2 | **需求文档** | 帮 AI 理解业务逻辑 |
| P2 | **架构设计文档** | 帮 AI 理解系统间调用关系 |
| P3 | **团队周报/复盘记录** | 长期积累的踩坑经验 |

**一个真实案例**：我给一个电商项目的知识库喂了 3 个月的 Bug 库之后，让 AI 帮我评审新的测试计划。AI 直接指出"这个接口你们过去 3 个月出了 7 个线上 Bug、4 个跟金额计算有关、新增商品组合优惠场景你漏了"——我自己翻 JIRA 都不一定找得这么全。

---

## 八、赛道二的必要补充：你不会架构，Agent 流就搭不起来

前面七周全在讲 AI。但我必须说一句——**如果你连 pytest fixture 的分层设计都不理解，Agent 生成的代码你也审核不了。代码审核不了的 Agent 流水线，就是定时炸弹。**

所以第八周你要同时补一点赛道二的东西。不用深入，但必须会下面三个能力：

### 8.1 测试框架分层设计（最小必要知识）

至少能画出你的测试项目的分层结构：

```
conftest.py（全局 fixture：token、base_url、环境变量）
  ├── core/base_client.py   （HTTP/Selenium/Appium 驱动封装）
  ├── data/test_data.py     （测试数据集中管理）
  ├── utils/assertions.py   （自定义断言工具）
  ├── tests/api/            （API 测试，按模块分文件）
  ├── tests/ui/             （UI 测试，按页面分文件）
  └── tests/e2e/            （端到端流程测试）
```

**给 AI 的 system prompt 里要写清楚这个分层结构**，让 AI 知道代码该放哪、该继承谁。不然 AI 会把所有东西糊在一个文件里。

### 8.2 CI/CD 质量门禁（让流水线能自动跑）

至少会在 Jenkins/GitLab CI/GitHub Actions 里加一个 stage：

```yaml
# .github/workflows/test.yml 示例
test:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: "3.12"
    - run: pip install -r requirements.txt
    - run: pytest tests/ --junitxml=results.xml -n auto  # -n auto 并行跑
    - name: AI 诊断失败
      if: failure()  # 只在失败时触发
      run: python analyze_failures.py results.xml
    - name: 发送诊断报告
      if: failure()
      run: python send_report.py  # 发到企业微信/钉钉/飞书
```

这一步不难，但绝大多数测试工程师的脚本都只在本地跑。**能跑在 CI 上和只能跑在本地，在面试官眼里是两个级别。**

### 8.3 测试数据工厂（小但实用）

不要求你写多复杂的，但这个能力要有：

```python
# data/factory.py
import random
import string

class TestDataFactory:
    """测试数据工厂——让 AI 生成的用例引用这个，而不是硬编码数据"""
    
    @staticmethod
    def random_string(length=10):
        return ''.join(random.choices(string.ascii_lowercase, k=length))
    
    @staticmethod
    def valid_product():
        return {
            "name": f"测试商品_{TestDataFactory.random_string(6)}",
            "category_id": random.choice([1, 2, 3]),
            "price": round(random.uniform(0.01, 9999.99), 2),
            "stock": random.randint(1, 9999)
        }
    
    @staticmethod
    def invalid_product_missing_name():
        data = TestDataFactory.valid_product()
        del data["name"]
        return data
    
    @staticmethod
    def product_with_negative_price():
        data = TestDataFactory.valid_product()
        data["price"] = -99.99
        return data
```

**把这个给 AI 当上下文**，AI 生成的用例就会用 `TestDataFactory.valid_product()` 而不是硬编码数据。你改一次工厂方法，所有用例跟着变。

---

## 九、8 周能力提升总表 + 涨薪对照

| 周数 | 核心任务 | 能力跃迁 | 市场定价变化 |
|------|---------|---------|------------|
| 第 1-2 周 | 学会写六要素 Prompt，DeepSeek/Claude 等多模型配合 | L0→L2：从"随便问"到"结构化输出" | +8%~15% |
| 第 3-4 周 | IDE 内嵌 AI（CodeBuddy/Claude Code），建 Skills | L2→L3：从"聊天框"到"项目级协作" | +15%~25% |
| 第 5-6 周 | AI 失败诊断 + 证据链收集自动化 | L3 深化：从"执行"到"诊断" | +15%~25% |
| 第 7 周 | Python 脚本串联 Agent 流水线 | L3→L4：从"单点"到"全流程" | +25%~35% |
| 第 8 周 | RAG 私有知识库 + 补充架构能力 | L4 深化 + 体系化能力 | +25%~35% |

**8 周后你能拿得出手的东西**（面试时这些都是硬通货）：

1. 一套六要素 Prompt 模板库（拿给面试官看，不是"我会用 AI"，是"我知道怎么让 AI 输出高质量测试代码"）
2. 一组 IDE Skills（CodeBuddy/Claude Code，展示你规范化 AI 行为的能力）
3. 一个可运行的 Agent 流水线脚本（放 GitHub 上，面试官可以 clone 下来看）
4. 一个私有测试知识库（面试时讲"我们团队的 Bug 库、测试规范、API 文档全在里面，AI 基于这些生成的东西几乎不需要改"）

---

## 十、别踩这些坑（我的血泪教训）

### ❌ 坑一：上来就搞 Agent 流水线

很多人觉得"Agent 多酷啊"，第一周就想搞全流程自动化。结果 Prompt 都写不好，Agent 生成的代码质量一塌糊涂，后面所有步骤全是垃圾进垃圾出。

**正确顺序**：先把 Prompt 写好（第 1-2 周）→ 再把单点流程跑顺（第 3-6 周）→ 最后串起来（第 7 周）。跳步骤必翻车。

### ❌ 坑二：AI 生成的不审核直接用

我见过有人让 AI 生成测试代码，看都不看直接提交跑 CI。结果第一个用例就挂了——AI 把 API 路径里的 `/v2/` 写成了 `/v1/`。

**AI 审核不了自己生成的东西**。永远要人看一眼。

### ❌ 坑三：知识库贪大求全

一开始就想把所有历史文档全灌进去，结果检索精度一塌糊涂——问的是订单接口，检索出来的却是三年前的离职交接文档。

**先喂最核心的 3-5 个文档**（API 文档 + 测试规范 + 最近一个迭代的用例），跑顺了再加。

### ❌ 坑四：只看不练

这个最要命。

你可能看了这篇文章觉得"嗯写的不错"，然后收藏、划线、关掉。下个月再看到类似文章再看一遍。一年后还在收藏。

**唯一有用的学习方式：从明天开始，用你手头真实的工作任务练。**

- 明天要测一个新接口？别手写用例，用六要素 Prompt 让 Claude 生成。
- 改完代码别手改，让 AI 帮你做 diff 审核。
- 用 @文件路径 让 AI 读你的项目再生成，别复制粘贴。

---

## 写在最后

这篇文章写了很长，但如果只记住一件事，我希望是这句：

**AI 不会替代测试工程师。但会替代不知道 AI 能替你做什么、不知道 AI 做不好什么、不知道怎么让 AI 做得更好的测试工程师。**

你现在的薪资可能是 18K、25K、35K。但你的定价基准，已经从"你会多少种自动化工具"变成了"你的 AI 杠杆系数是多少"。

同样是测一个迭代——你用手写完所有用例要两天，隔壁那个人用 AI 辅助一个下午搞定，剩下的时间在研究测试架构和下一轮迭代的风险分析。

你猜老板给谁涨薪？

8 周时间，选不选是你的事。市场不太等人。

---

*本系列更多内容：[AI 测试技术分享 CSDN 合集](https://blog.csdn.net/)*

---

#AI测试 #测试工程师 #自动化测试 #Prompt工程 #ClaudeCode #测试开发 #RAG #职业发展

# AI 辅助失败诊断与智能断言设计

> 让 AI 帮你从"人肉 grep"进化到"秒级定位根因"

---

## 一、传统测试失败诊断的困境

线上报了一个 Bug：用户支付成功但订单状态仍为"待支付"。

你打开 CI 日志——3000 行。接下来：

1. 用肉眼从上往下扫，找到对应测试用例
2. 看请求发了什么
3. 看响应回了什么
4. 看断言在哪一步挂了
5. 回到第 1 步，找下一个可能相关的用例……

**半小时过去了，眼睛快瞎了。**

这个场景每个测试人都经历过。问题的本质不是"你不会看日志"，而是**日志本身没有为"快速诊断"这个场景设计**。

---

## 二、构建失败证据链

一次测试失败，应该能拿到这几样东西：

```
┌──────────────────────────────────────┐
│          失败证据链（自解释的）        │
├──────────────────────────────────────┤
│ 1. 用例信息（名称、标签、环境）        │
│ 2. 请求快照（URL、方法、headers、body）│
│ 3. 响应快照（状态码、响应体、耗时）    │
│ 4. 断言详情（哪个字段、期望值、实际值） │
│ 5. 上下文（前置步骤的执行记录）         │
│ 6. 环境快照（时间、服务器版本、配置）   │
└──────────────────────────────────────┘
```

### 2.1 请求/响应日志设计

```python
import json
import time
import requests
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class HttpRecord:
    """单次 HTTP 请求的完整记录"""
    trace_id: str
    method: str
    url: str
    request_headers: dict = field(repr=False)
    request_body: Optional[str] = None
    response_status: Optional[int] = None
    response_headers: dict = field(default_factory=dict, repr=False)
    response_body: Optional[str] = None
    elapsed_ms: float = 0
    error: Optional[str] = None
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        """转为结构化字典，敏感信息自动脱敏"""
        safe_req_headers = self._mask_sensitive(self.request_headers)
        safe_resp_headers = self._mask_sensitive(self.response_headers)
        
        return {
            "trace_id": self.trace_id,
            "request": {
                "method": self.method,
                "url": self.url,
                "headers": safe_req_headers,
                "body": self.request_body[:500] if self.request_body else None
            },
            "response": {
                "status": self.response_status,
                "headers": safe_resp_headers,
                "body": self.response_body[:500] if self.response_body else None,
                "elapsed_ms": self.elapsed_ms
            },
            "error": self.error,
            "timestamp": self.timestamp
        }

    @staticmethod
    def _mask_sensitive(headers: dict) -> dict:
        """自动脱敏敏感字段"""
        sensitive_keys = {"authorization", "cookie", "x-api-key", "token"}
        return {
            k: "****" if k.lower() in sensitive_keys else v
            for k, v in headers.items()
        }
```

### 2.2 断言记录设计

```python
@dataclass
class AssertionRecord:
    """单次断言记录"""
    trace_id: str
    field: str           # 断言的字段路径，如 "$.data.status"
    expected: any        # 期望值
    actual: any          # 实际值
    passed: bool         # 是否通过
    message: str         # 断言描述

    def to_dict(self) -> dict:
        return {
            "trace_id": self.trace_id,
            "field": self.field,
            "expected": str(self.expected),
            "actual": str(self.actual),
            "passed": self.passed,
            "message": self.message
        }
```

### 2.3 证据链收集器

```python
class EvidenceCollector:
    """测试证据链收集器"""
    
    def __init__(self, trace_id: str):
        self.trace_id = trace_id
        self.http_records: list[HttpRecord] = []
        self.assertion_records: list[AssertionRecord] = []
        self.steps: list[str] = []  # 文本步骤记录
    
    def log_step(self, step: str):
        self.steps.append(f"[{self.trace_id}] {step}")
    
    def record_http(self, **kwargs) -> HttpRecord:
        record = HttpRecord(trace_id=self.trace_id, **kwargs)
        self.http_records.append(record)
        return record
    
    def record_assertion(self, **kwargs) -> AssertionRecord:
        record = AssertionRecord(trace_id=self.trace_id, **kwargs)
        self.assertion_records.append(record)
        return record
    
    def get_failure_summary(self) -> dict:
        """生成失败摘要，可直接喂给 AI"""
        failed_assertions = [a for a in self.assertion_records if not a.passed]
        failed_http = [r for r in self.http_records if r.response_status and r.response_status >= 400]
        
        return {
            "trace_id": self.trace_id,
            "total_steps": len(self.steps),
            "steps": self.steps,
            "http_calls": [r.to_dict() for r in self.http_records],
            "failed_assertions": [a.to_dict() for a in failed_assertions],
            "failed_http": [r.to_dict() for r in failed_http],
        }
```

---

## 三、AI 辅助诊断的 Prompt 设计

### 3.1 诊断 Prompt 模板

收集好证据链后，喂给 AI：

```python
def build_diagnosis_prompt(evidence: dict) -> str:
    """构建 AI 诊断 Prompt"""
    return f"""
你是一个资深测试工程师，请分析以下测试失败案例，定位根因。

## 测试执行步骤
{json.dumps(evidence["steps"], ensure_ascii=False, indent=2)}

## HTTP 请求记录
{json.dumps(evidence["http_calls"], ensure_ascii=False, indent=2)}

## 失败的断言
{json.dumps(evidence["failed_assertions"], ensure_ascii=False, indent=2)}

请按以下格式输出分析结果：

1. **失败现象**：用一句话描述什么失败了
2. **直接原因**：哪个断言没通过，期望值和实际值的差异
3. **根本原因**：追溯到代码或数据层面，是什么导致了差异
4. **建议修复**：给出具体的修复步骤
5. **置信度**：你对这个诊断的把握（高/中/低）

如果信息不足以判断，请明确指出缺失的信息。
"""
```

### 3.2 实际诊断示例

```python
# 模拟一个失败场景
def test_order_payment():
    collector = EvidenceCollector("order_pay_001")
    
    collector.log_step("1. 创建订单")
    collector.log_step("2. 发起支付")
    
    # 记录支付请求
    collector.record_http(
        method="POST",
        url="/api/orders/123/pay",
        request_body='{"amount": 99.00, "method": "wechat"}',
        response_status=200,
        response_body='{"code": 0, "data": {"status": "paid"}}',
        elapsed_ms=234
    )
    
    collector.log_step("3. 查询订单状态")
    
    # 记录查询请求
    collector.record_http(
        method="GET",
        url="/api/orders/123",
        response_status=200,
        response_body='{"code": 0, "data": {"status": "pending"}}',
        elapsed_ms=89
    )
    
    # 断言失败
    collector.record_assertion(
        field="$.data.status",
        expected="paid",
        actual="pending",
        passed=False,
        message="订单支付后状态应为 paid"
    )
    
    # 生成证据摘要
    evidence = collector.get_failure_summary()
    
    # 构建 Prompt 并调用 AI
    prompt = build_diagnosis_prompt(evidence)
    # diagnosis = call_ai_api(prompt)
    
    print(prompt)
```

AI 的典型诊断输出：

```
1. 失败现象：订单支付后状态仍为 pending，而非预期的 paid

2. 直接原因：
   断言 $.data.status 不匹配
   期望值：paid
   实际值：pending

3. 根本原因：
   支付接口返回了 status: paid，但查询接口返回的是 pending。
   可能的原因：
   a) 支付接口是异步的，状态更新有延迟（最可能）
   b) 支付回调未触发订单状态变更
   c) 数据库主从延迟导致读到了旧数据

4. 建议修复：
   a) 在支付和查询之间增加重试等待逻辑：
      - 支付后等待 1 秒
      - 查询状态，若为 pending 则每 500ms 重试，最多 10 次
   b) 检查支付回调是否正常触发
   c) 考虑使用强制主库读

5. 置信度：高
   缺失信息：支付回调日志、数据库状态变更记录
```

---

## 四、AI 辅助修复 Locator

Web 自动化的头号杀手：**元素定位断裂**。

```python
class LocatorHealer:
    """AI 辅助修复断裂的 Locator"""
    
    def __init__(self, ai_client):
        self.ai = ai_client
    
    def heal(self, page, broken_locator: str, page_html: str) -> str:
        """输入断裂的 Locator 和当前页面 HTML，返回修复后的 Locator"""
        prompt = f"""
我之前的 Playwright Locator 失效了。

## 原来的 Locator
{broken_locator}

## 当前页面的 HTML 片段
{page_html}

## 我要定位的元素特征
（请根据原 Locator 推断：它在页面上应该是什么角色、文字、位置？）

请给出 3 个可能的新 Locator，按推荐程度排序，使用 Playwright 语法。
"""
        response = self.ai.complete(prompt)
        # 解析 AI 返回的 Locator
        return self._parse_locators(response)
    
    def try_heal_and_retry(self, page, action_fn, max_attempts=3):
        """尝试修复 Locator 并重试操作"""
        for attempt in range(max_attempts):
            try:
                return action_fn()
            except Exception as e:
                if "locator" in str(e).lower() or "timeout" in str(e).lower():
                    # 获取当前页面 HTML 供 AI 分析
                    html_snippet = page.content()[:3000]
                    new_locator = self.heal(page, str(e), html_snippet)
                    print(f"🔧 AI 建议新 Locator：{new_locator}")
                    # 这里可以动态更新 Locator 并重试
                else:
                    raise  # 非 Locator 问题，直接抛出
```

---

## 五、传统断言 vs AI 智能断言

### 5.1 传统断言的能力边界

```python
# 传统断言擅长：精确的值比较
assert resp.status_code == 200
assert resp.json()["code"] == 0
assert resp.json()["data"]["name"] == "张三"
assert len(resp.json()["data"]["items"]) == 10
assert resp.elapsed.total_seconds() < 3.0

# 传统断言不擅长：
# - "这个错误信息的意思是对的吗？"
# - "这个返回结构合理吗？"
# - "列表里的数据看起来是正确的业务数据吗？"
```

### 5.2 AI 智能断言的补充场景

```python
class AIAssertion:
    """AI 辅助的非确定性断言"""
    
    def __init__(self, ai_client):
        self.ai = ai_client
    
    def assert_error_message_makes_sense(self, error_msg: str, context: str) -> bool:
        """判断错误信息是否合理（非精确匹配）"""
        prompt = f"""
判断以下错误信息在这个业务上下文中是否合理：

业务上下文：{context}
错误信息：{error_msg}

回答格式：{{"reasonable": true/false, "reason": "判断理由"}}
"""
        result = self.ai.complete_json(prompt)
        return result["reasonable"]
    
    def assert_response_structure_reasonable(self, response: dict, expected_schema: str) -> bool:
        """判断响应结构是否符合预期模式"""
        prompt = f"""
检查以下 API 响应是否符合预期的数据结构模式：

预期模式：{expected_schema}
实际响应：{json.dumps(response, ensure_ascii=False)}

判断：
1. 结构是否基本匹配？
2. 字段类型是否合理？
3. 有没有明显的数据异常（如字符串字段出现了数字）？

回答格式：{{"valid": true/false, "issues": ["问题1", "问题2"]}}
"""
        result = self.ai.complete_json(prompt)
        return result["valid"]
    
    def assert_business_data_plausible(self, items: list, item_type: str) -> dict:
        """判断列表数据是否像真实的业务数据"""
        sample = items[:5]  # 采样前 5 条
        prompt = f"""
检查以下{ item_type }列表数据是否像真实业务数据：

{json.dumps(sample, ensure_ascii=False)}

检查项：
1. 数据是否有重复？
2. 数据是否符合常识（如价格不应为负数）？
3. 字段之间是否自洽（如总价 = 单价 × 数量）？
4. 有没有明显的测试数据特征（如 "test_xxx"）？

回答格式：{{"plausible": true/false, "anomalies": ["异常1"]}}
"""
        return self.ai.complete_json(prompt)
```

### 5.3 两类断言的协作策略

| 场景 | 断言方式 | 原因 |
|------|----------|------|
| 状态码、固定字段 | 传统断言 | 确定性，零成本，即时反馈 |
| 错误信息语义 | AI 断言 | 自然语言，传统正则无法覆盖 |
| 数据结构合理性 | AI 断言 | 需要理解业务模式 |
| 列表数据真实性 | AI 断言 | 需要常识判断 |
| 回归测试核心流程 | 传统断言 | 稳定性优先，不能引入幻觉 |

**原则**：金融、交易等强一致性场景，AI 断言仅做辅助检查，不能替代传统断言；UI 展示、文案校验等场景，AI 断言可以作为主力。

---

## 六、Token 成本控制

调用 AI 做断言不是免费的，需要精打细算：

```python
class TokenBudget:
    """Token 用量控制"""
    
    def __init__(self, daily_limit: int = 100_000):
        self.daily_limit = daily_limit
        self.used_today = 0
        self.call_history: list[dict] = []
    
    def can_call(self, estimated_tokens: int) -> bool:
        return (self.used_today + estimated_tokens) <= self.daily_limit
    
    def record_call(self, tokens_used: int, purpose: str):
        self.used_today += tokens_used
        self.call_history.append({
            "tokens": tokens_used,
            "purpose": purpose,
            "cumulative": self.used_today
        })
    
    def get_summary(self) -> dict:
        return {
            "used": self.used_today,
            "remaining": self.daily_limit - self.used_today,
            "call_count": len(self.call_history)
        }


# 减少 Token 消耗的策略
def optimize_prompt_for_cost(base_prompt: str, response: dict) -> str:
    """优化 Prompt：减少输入 Token"""
    # 1. 只发关键字段，不贴完整响应
    # 2. 采样而不是全量数据
    # 3. 缓存相同类型的 AI 调用结果
    # 4. 先用传统断言过滤，只有传统断言覆盖不了的才用 AI
    pass
```

---

## 七、总结

三条核心原则：

```
1. 证据链要自解释
   → 任何人（包括 AI）拿到证据链，不需要翻源码就能理解失败

2. AI 用于"理解语义"，传统断言用于"精确比较"
   → 各司其职，不越界

3. 诊断 Prompt 要结构化
   → 分步骤、分证据类型、要求特定输出格式
```

**最终目标**：你的测试框架跑完之后，不是输出一行"FAILED"，而是输出一份**任何人一眼就能看懂、AI 可以直接分析**的失败诊断报告。

---

*下一篇预告：《代码调用 AI 接口与智能断言深度实践》——OpenAI/Claude API 集成、Prompt 模板化、成本优化*

---

#AI测试 #测试诊断 #智能断言 #自动化测试 #测试工程化

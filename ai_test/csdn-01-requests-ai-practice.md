# requests 核心编程与 AI 协作实践

> 从 curl 到工程化请求层，用 AI 加速每一步

---

## 一、问题引入

很多测试工程师的接口自动化是这样起步的：

```python
import requests

# 第一版：能跑就行
def test_login():
    resp = requests.post("http://192.168.1.100:8080/api/login",
                         json={"username": "admin", "password": "123456"})
    print(resp.status_code)
    print(resp.json())
```

能跑，但问题很快暴露：

- 环境 IP 硬编码，换了测试环境就要改
- 没有超时设置，服务挂了会无限等待
- 鉴权 token 每次都要手动复制
- 异常处理为零，报错信息看不懂
- 重复代码满天飞，改一处要改 N 处

更关键的是：**当 AI 作为协作者加入时，你的代码结构直接决定了 AI 能不能帮上忙。**

---

## 二、最小可执行链路：先跑通，再优化

任何时候，先让代码跑通。我的原则是：

> 先亲自写一条完整链路（GET → 解析 → 断言），然后让 AI 在这个基础上扩展。

```python
import requests

# 最小链路：构造请求 → 发送 → 接收 → 断言
def test_get_user_info():
    url = "https://api.example.com/v1/users/1"
    headers = {"Authorization": "Bearer YOUR_TOKEN"}
    
    resp = requests.get(url, headers=headers, timeout=10)
    
    # 先断言状态码
    assert resp.status_code == 200, f"期望 200，实际 {resp.status_code}"
    
    # 再断言业务字段
    data = resp.json()
    assert "username" in data, "响应中缺少 username 字段"
    assert isinstance(data["id"], int), "id 字段应为整数"
    
    print(f"✅ 测试通过：用户 {data['username']} 信息获取成功")
```

这段代码虽然原始，但包含了所有关键节点。跑通之后，就可以让 AI 介入扩展了。

---

## 三、Session：被低估的效率利器

直接用 `requests.get()` / `requests.post()` 每次都是新建 TCP 连接。对于需要登录态的接口链测试，Session 是最基本的优化：

```python
import requests

class APISession:
    """基于 Session 的请求封装"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "AutoTest/1.0"
        })
        self.timeout = timeout
    
    def login(self, username: str, password: str) -> str:
        """登录并返回 token"""
        resp = self.session.post(
            f"{self.base_url}/api/login",
            json={"username": username, "password": password},
            timeout=self.timeout
        )
        assert resp.status_code == 200, f"登录失败：{resp.status_code}"
        
        token = resp.json()["data"]["token"]
        # 登录成功后自动挂载 token 到后续所有请求
        self.session.headers["Authorization"] = f"Bearer {token}"
        return token
    
    def get(self, path: str, **kwargs) -> requests.Response:
        return self.session.get(
            f"{self.base_url}{path}", 
            timeout=kwargs.pop("timeout", self.timeout),
            **kwargs
        )
    
    def post(self, path: str, **kwargs) -> requests.Response:
        return self.session.post(
            f"{self.base_url}{path}",
            timeout=kwargs.pop("timeout", self.timeout),
            **kwargs
        )
    
    def close(self):
        self.session.close()
```

### Session 的三个关键收益

| 收益 | 说明 |
|------|------|
| **连接复用** | 同一个 Session 内所有请求共用 TCP 连接，减少握手开销 |
| **状态保持** | cookies 自动管理，登录态天然传递 |
| **公共配置** | headers、base_url 集中管理，修改一处全局生效 |

---

## 四、AI 协作的第一个切入点：从 curl 到 requests

在排查接口问题或阅读 API 文档时，你经常拿到的是 curl 命令：

```bash
curl -X POST "https://api.example.com/v1/orders" \
  -H "Authorization: Bearer abc123" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1001, "quantity": 2}'
```

让 AI 做这个转换是非常可靠的——因为 curl 和 requests 之间有确定性的映射关系：

```python
# AI 生成的 requests 代码
import requests

url = "https://api.example.com/v1/orders"
headers = {
    "Authorization": "Bearer abc123",
    "Content-Type": "application/json"
}
data = {"product_id": 1001, "quantity": 2}

resp = requests.post(url, headers=headers, json=data)
```

**但你需要审核这几件事**：

1. **超时设置**：AI 通常会漏掉 `timeout` 参数，这是致命问题
2. **异常处理**：AI 默认不写 try/except，生产代码中这是必须的
3. **敏感信息**：token 是否硬编码？应该从环境变量读取
4. **数据来源**：测试数据是写死的还是从 fixture 来的？

```python
# 审核后的版本
import os
import requests
from requests.exceptions import Timeout, ConnectionError

def create_order(product_id: int, quantity: int) -> dict:
    url = f"{os.environ['API_BASE_URL']}/v1/orders"
    headers = {"Authorization": f"Bearer {os.environ['API_TOKEN']}"}
    
    try:
        resp = requests.post(
            url, 
            headers=headers, 
            json={"product_id": product_id, "quantity": quantity},
            timeout=10
        )
        resp.raise_for_status()
        return resp.json()
    except Timeout:
        raise RuntimeError(f"创建订单超时：{url}")
    except ConnectionError:
        raise RuntimeError(f"无法连接到服务：{url}")
    except requests.HTTPError as e:
        raise RuntimeError(f"创建订单失败 [{resp.status_code}]：{resp.text}")
```

---

## 五、从一次性脚本到公共请求层

当你的测试文件里有 20 个接口调用，你开始发现：

- `base_url` 重复了 20 次
- `Authorization` header 重复了 20 次
- 登录逻辑在 5 个文件里各写了一遍
- 错误处理的方式各不相同

这正是重构的时机。**让 AI 提出重构方案，你来审核哪些该封装、哪些该保持可见**。

```python
# 公共请求层设计
class HttpClient:
    """统一 HTTP 请求客户端"""
    
    def __init__(self, config: dict):
        self.base_url = config["base_url"]
        self.timeout = config.get("timeout", 30)
        self.retry_count = config.get("retry", 0)
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })
        self._setup_auth(config)
    
    def _setup_auth(self, config: dict):
        """根据配置初始化鉴权"""
        auth_type = config.get("auth_type", "none")
        if auth_type == "bearer":
            self.session.headers["Authorization"] = f"Bearer {config['token']}"
        elif auth_type == "basic":
            self.session.auth = (config["username"], config["password"])
    
    def _log_request(self, method: str, url: str, **kwargs):
        """请求日志（已脱敏）"""
        safe_headers = {k: "****" if k.lower() in ("authorization", "cookie") else v 
                       for k, v in self.session.headers.items()}
        print(f"[{method}] {url} | headers={safe_headers}")
    
    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        timeout = kwargs.pop("timeout", self.timeout)
        
        self._log_request(method, url, **kwargs)
        
        for attempt in range(self.retry_count + 1):
            try:
                resp = self.session.request(
                    method, url, timeout=timeout, **kwargs
                )
                resp.raise_for_status()
                return resp
            except (Timeout, ConnectionError) as e:
                if attempt < self.retry_count:
                    print(f"⚠️ 第 {attempt + 1} 次重试...")
                    continue
                raise RuntimeError(f"请求失败 [{method} {url}]：{e}")
            except requests.HTTPError as e:
                # HTTP 错误不重试（4xx/5xx 重试没有意义）
                raise
```

### 重构后的断言层

既然把请求封装了，断言也应该从测试用例中抽离出来，形成可复用的检查器：

```python
class ResponseAssertion:
    """响应断言工具集"""
    
    @staticmethod
    def status_is(resp: requests.Response, expected: int):
        assert resp.status_code == expected, \
            f"状态码不匹配：期望 {expected}，实际 {resp.status_code}，响应体：{resp.text[:200]}"
    
    @staticmethod
    def field_exists(data: dict, field_path: str):
        """校验字段存在，支持点号路径如 data.user.name"""
        keys = field_path.split(".")
        current = data
        for key in keys:
            if isinstance(current, dict):
                assert key in current, f"字段 '{field_path}' 不存在，当前层级：{list(current.keys())}"
                current = current[key]
            elif isinstance(current, list):
                assert int(key) < len(current), f"索引 {key} 超出列表范围"
                current = current[int(key)]
    
    @staticmethod
    def field_equals(data: dict, field_path: str, expected):
        keys = field_path.split(".")
        current = data
        for key in keys:
            current = current[key] if isinstance(current, dict) else current[int(key)]
        assert current == expected, \
            f"字段 '{field_path}' 不匹配：期望 {expected}，实际 {current}"
    
    @staticmethod
    def response_time_within(resp: requests.Response, max_ms: int):
        elapsed_ms = resp.elapsed.total_seconds() * 1000
        assert elapsed_ms <= max_ms, \
            f"响应时间超标：{elapsed_ms:.0f}ms > {max_ms}ms"
```

---

## 六、AI 协作的第二个切入点：diff 审核重构

当你把 300 行的 requests 脚本重构为上面的分层架构后，怎么验证行为没有变？

**让 AI 用 diff 的方式帮你审核**：

```markdown
给 AI 的 Prompt：
---
我重构了一段接口测试代码，请对比重构前后的行为差异：

## 重构前
[贴原始代码]

## 重构后
[贴新代码]

请逐一检查：
1. 所有请求的 URL、方法、headers、body 是否一致？
2. 所有断言的逻辑是否等价？
3. 有没有隐藏的业务步骤被封装吞掉了？
4. 异常处理是否变弱了？
---
```

**AI 最容易发现的三个问题**：

1. **超时被吃掉了**：原始代码有 `timeout=5`，封装后用了默认值 30
2. **异常被吞了**：封装层加了 try/except，但只是 `pass` 没有 re-raise
3. **请求顺序被改了**：原来 A 请求的返回值传给了 B，封装后变成独立调用了

---

## 七、完整实战：一个接口测试的设计过程

以下是一个真实的测试设计流程：

### 场景：电商订单创建 → 查询 → 取消

```python
import os
import pytest

@pytest.fixture
def api():
    """测试客户端 fixture"""
    client = HttpClient({
        "base_url": os.environ["API_BASE_URL"],
        "auth_type": "bearer",
        "token": os.environ["API_TOKEN"],
        "timeout": 10,
        "retry": 1
    })
    yield client
    client.close()


class TestOrderFlow:
    """订单核心流程测试"""
    
    def test_create_and_query_order(self, api: HttpClient):
        """创建订单后能正确查询"""
        # 1. 创建订单
        create_resp = api.post("/v1/orders", json={
            "product_id": 1001,
            "quantity": 2,
            "customer_id": "cust_001"
        })
        ResponseAssertion.status_is(create_resp, 201)
        ResponseAssertion.field_exists(create_resp.json(), "data.order_id")
        
        order_id = create_resp.json()["data"]["order_id"]
        
        # 2. 查询订单
        query_resp = api.get(f"/v1/orders/{order_id}")
        ResponseAssertion.status_is(query_resp, 200)
        ResponseAssertion.field_equals(query_resp.json(), "data.status", "pending")
        ResponseAssertion.field_equals(query_resp.json(), "data.total", 398.00)
        
        # 3. 取消订单
        cancel_resp = api.post(f"/v1/orders/{order_id}/cancel")
        ResponseAssertion.status_is(cancel_resp, 200)
        ResponseAssertion.field_equals(cancel_resp.json(), "data.status", "cancelled")
    
    def test_create_order_with_invalid_product(self, api: HttpClient):
        """创建订单时产品不存在"""
        resp = api.post("/v1/orders", json={
            "product_id": 99999,
            "quantity": 1,
            "customer_id": "cust_001"
        })
        # 不抛异常，因为业务上应该返回 4xx
        assert resp.status_code == 400
        assert "不存在" in resp.json()["message"]
```

---

## 八、总结：AI 该做什么，你该做什么

| 你做的 | AI 做的 |
|--------|---------|
| 设计分层架构 | 生成样板代码 |
| 定义接口契约 | 填充实现细节 |
| 审核关键逻辑 | 补充边界用例 |
| 决定重试策略 | 提供优化建议 |
| 处理敏感信息 | 格式化日志输出 |

**核心原则**：AI 是你手速的放大器，不是脑力的替代品。你的架构设计能力决定了 AI 能帮你走多远。

---

*下一篇预告：《从 requests 脚本到 pytest 工程化演进》——如何用 AI 把 500 行脚本重构为 50 行配置 + 自动化框架*

---

#接口测试 #Python #requests #AI测试 #自动化测试

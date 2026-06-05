# Claude Code 生成测试用例 + Prompt 终极技巧

> **适配**：Python + Pytest + Httpx + Playwright 企业级自动化测试平台
>
> **解决**：手动写用例慢、AI 输出不规范、断言笼统、用例不可维护、重复造轮子等核心痛点

---

## 一、Prompt 工程核心原则（写好 Prompt 的底层逻辑）

### 1. 测试用例 Prompt 必备 6 要素（缺一个质量就下降）

| 要素 | 说明 | 示例 |
|------|------|------|
| **技术栈与规范** | 明确要求遵循项目现有规范 | 遵循项目 `CLAUDE.md` 编码规范，继承 `@core/base_api.py` 基类 |
| **用例类型** | 明确是 API/UI/异常/性能/安全用例 | 生成 RESTful API 接口的正常 + 异常 + 边界值测试用例 |
| **输入输出** | 明确接口地址、请求方法、参数、响应结构 | 接口：`POST /api/v1/login`，参数：`username/password`，响应包含 `code/data/token` |
| **断言标准** | 强制要求分层断言，禁止笼统断言 | 断言顺序：状态码 → 响应结构 → 业务字段 → 异常信息 |
| **用例结构** | 要求使用 Pytest fixture，用例独立可重复执行 | 使用 `api_client` fixture，每个用例独立会话，无执行顺序依赖 |
| **质量要求** | 要求通过 Ruff + SonarQube 检查，无硬编码、无冗余 | 所有配置从 `config/settings.py` 读取，无硬编码账号密码 |

### 2. 万能公式（直接套用）

```text
基于【技术栈 + 规范】，为【被测对象】生成【用例类型】测试用例

要求：
1. 继承/复用现有【基类/Fixture】
2. 覆盖【正常场景 + 异常场景 + 边界值场景】
3. 断言遵循【分层断言标准】
4. 符合项目编码规范，通过 Ruff + SonarQube 检查
5. 用例独立可重复执行，无依赖
```

---

## 二、Claude Code 专属文件级协作技巧

> 利用 Claude Code 能直接读取项目文件的能力，让 AI 生成的用例 **100% 符合你的项目架构**，不用手动改基类引用。

### 1. 核心语法：`@文件路径` 引用现有代码

```text
# 自动读取 API 基类，生成符合基类的用例
基于 @core/base_api.py 的 BaseAPI 类，为 /api/v1/user 接口生成测试用例

# 参考已有用例风格，保持一致性
参考 @tests/api/test_login.py 的写法，为 /api/v1/order 接口生成相同风格的用例

# 读取配置文件，自动使用正确的环境变量
基于 @config/settings.py 的配置，生成无硬编码的测试用例
```

### 2. 增量修改技巧（不用重写整个文件）

```text
# 只修改指定用例的断言部分
优化 @tests/api/test_user.py 中 test_get_user_info 用例的断言，增加响应结构校验

# 给现有文件新增异常用例
在 @tests/api/test_order.py 中新增3个异常用例：参数为空、参数类型错误、权限不足
```

### 3. 批量生成技巧

```text
# 读取 Swagger 文档，批量生成所有接口用例
解析 @docs/api.yaml Swagger 文档，为所有接口生成基础测试用例，按模块分文件保存到 tests/api/ 目录
```

---

## 三、分场景 Prompt 模板（直接复制修改使用）

### 1. API 测试用例——基础模板

```text
基于项目 CLAUDE.md 编码规范，继承 @core/base_api.py 的 BaseAPI 类，使用 api_client fixture
为 POST /api/v1/order/create 接口生成完整测试用例

接口信息：
- 请求方法：POST
- 请求头：Content-Type: application/json，Authorization: Bearer {token}
- 请求参数：
  {
    "product_id": int,
    "quantity": int,
    "address_id": int
  }
- 正常响应：{"code": 200, "data": {"order_id": str}, "msg": "success"}
- 异常响应：{"code": 400/401/403/500, "msg": "错误信息"}

要求：
1. 覆盖所有场景：
   - 正常场景：参数合法，创建订单成功
   - 异常场景：参数缺失、参数类型错误、参数值非法、token 无效、权限不足
   - 边界值场景：quantity=1、quantity=9999（最大允许值）、quantity=0、quantity=-1
2. 断言分层：先断言状态码，再断言响应结构，最后断言业务字段
3. 所有测试数据从 @data/test_data.py 读取，无硬编码
4. 用例独立，每个用例单独会话，无执行顺序依赖
5. 加入异常捕获和日志打印，失败时输出完整请求和响应信息
6. 代码通过 Ruff + SonarQube 检查，无冗余、无未使用变量
```

### 1.1 API 契约测试（Schema Validation）

> 接口文档和实际返回不一致是联调噩梦。让 Claude 根据 OpenAPI/ Swagger 规范自动生成契约测试，确保接口返回值与文档严格一致。

```text
基于 @docs/api.yaml 的 OpenAPI 3.0 规范，使用 jsonschema 库为以下接口生成契约测试用例：
- POST /api/v1/order/create
- GET /api/v1/order/{order_id}
- GET /api/v1/order/list

要求：
1. 从 OpenAPI 定义中提取每个接口的请求 Body Schema 和响应 Schema
2. 生成三组测试：
   - 正常请求 → 验证响应 JSON 结构和字段类型与 Schema 完全一致
   - 缺少必填字段的请求 → 验证返回 422/400，错误信息字段正确
   - 字段类型错误的请求 → 验证返回 422/400，错误信息字段正确
3. 校验内容包括：字段存在性、字段类型（string/int/boolean/array/object）、
   字段格式（date-time/email/uri）、枚举值范围、嵌套对象结构
4. 将提取的 JSON Schema 保存到 @tests/schemas/ 目录，按模块命名
5. 每个接口至少覆盖 200/201/400/422/500 五种状态码的 Schema 校验
6. 使用 pytest 的 assert 配合 jsonschema.validate()，失败时输出不匹配的具体字段和原因
```

### 1.2 数据驱动参数化测试（`pytest.mark.parametrize`）

> 同一个接口用不同参数反复测，手动复制粘贴修改效率极低。用 parametrize + Claude 生成测试数据集，一份代码覆盖几十组场景。

```text
基于 @core/base_api.py 的 BaseAPI 类，使用 pytest.mark.parametrize
为 POST /api/v1/user/search 接口生成数据驱动测试用例

搜索接口：
- 参数：keyword（搜索关键词）、page（页码）、page_size（每页条数）、
        sort_by（排序字段：create_time/username）、order（asc/desc）
- 响应：{"code": 200, "data": {"list": [...], "total": int, "page": int, "page_size": int}}

要求：
1. 使用 @pytest.mark.parametrize 装饰器，定义 ids 参数为每个 case 起可读名称
2. 测试数据从 @data/test_data.py 的 user_search_cases 变量读取
3. 覆盖以下维度（至少 20 组数据）：

   关键词维度：
   - 精确匹配、模糊匹配、空字符串、不存在的关键词、超长关键词（>100字符）、
     包含 SQL 注入字符（' OR '1'='1）、HTML 标签（<script>alert(1)</script>）

   分页维度：
   - page=1 page_size=10（正常首页）、page=0（非法页码）、page=-1（负页码）、
     page=99999（超大页码，预期返回空列表）、page_size=1（最小每页数）、
     page_size=100（最大每页数）、page_size=0（非法每页数）、
     page_size=1000（超过上限，预期被限制或报错）

   排序维度：
   - sort_by=create_time order=desc、sort_by=username order=asc、
     sort_by=invalid_field（非法排序字段）、order=invalid（非法排序方向）

   组合维度：
   - 关键词 + 按创建时间降序 + 第 1 页 20 条
   - 关键词 + 按用户名升序 + 第 2 页 10 条
   - 空关键词 + 默认排序 + 首页

4. 每个 parametrize case 断言：状态码、响应结构、data 字段存在性、
   返回条数 ≤ page_size、total 为正整数（有数据时）
5. 所有测试数据用 @pytest.fixture 从 data/test_data.py 读取，禁止在用例中硬编码
```

### 1.3 Mock 外部依赖与隔离测试

> 依赖第三方服务（支付、短信、邮件）的接口无法在测试环境调用真实服务，需要 mock 掉外部依赖，专注测试自身业务逻辑。

```text
基于项目 CLAUDE.md 规范，使用 unittest.mock 或 pytest-mock
为 POST /api/v1/order/pay 支付接口生成 Mock 隔离测试用例

业务逻辑：
1. 接收订单号和支付方式
2. 调用第三方支付网关（@services/payment_gateway.py 的 PaymentGateway.pay()）
3. 支付成功后更新订单状态、发送通知短信（@services/sms_service.py 的 SmsService.send()）
4. 返回支付结果

要求：
1. 使用 @pytest.fixture 创建 mock_payment_gateway 和 mock_sms_service fixture
2. 覆盖以下 Mock 场景：

   支付网关场景：
   - Mock 支付成功 → 验证返回 {"code": 200, "data": {"status": "paid"}}
                   → 验证订单状态被更新为 paid
                   → 验证短信发送方法被调用1次
   - Mock 支付失败（余额不足）→ 验证返回错误码和错误信息
                              → 验证订单状态保持 pending
                              → 验证短信发送方法未被调用
   - Mock 支付超时 → 验证返回超时错误码和错误信息
                   → 验证订单状态保持 pending 或标记为 timeout
   - Mock 支付网关抛出异常 → 验证接口返回 500，不影响主流程

3. 使用 mock.assert_called_once_with() 验证调用参数的正确性
4. 测试完成后自动恢复真实对象，不影响其他用例
5. 每个用例的 mock 在 setup 中创建，teardown 中清理
```

### 1.4 并发安全与幂等性测试

> 支付、下单等关键接口在高并发下容易出现重复扣款、超卖等问题。Claude 可以帮你生成并发测试用例，用 threading/asyncio 模拟真实并发场景。

```text
基于项目 CLAUDE.md 规范，使用 Python threading 或 asyncio 库
为 POST /api/v1/order/create 和 PUT /api/v1/order/{id}/pay 接口生成并发安全测试用例

要求：

一、幂等性测试（防止重复下单）：
1. 同一用户用相同参数（相同商品、数量、地址）在 1 秒内并发调用 10 次创建订单接口
2. 断言：只有 1 次成功创建订单（其余返回"重复提交"错误码）
3. 断言：数据库中该用户的该商品订单只有 1 条记录
4. 提示：需要在 Prompt 中告诉 Claude 幂等键的设计（如订单幂等键 = user_id + product_id + timestamp）

二、库存扣减并发测试（防止超卖）：
1. 在测试数据库中准备商品 stock=10
2. 启动 20 个线程并发调用创建订单接口（每个订单 quantity=1）
3. 断言：成功创建的订单数量 ≤ 10
4. 断言：剩余库存 ≥ 0（绝不能为负数）
5. 断言：statistics 接口返回的 stock 与实际剩余库存一致

三、并发支付测试（防止重复扣款）：
1. 创建一笔待支付订单
2. 并发调用支付接口 5 次（同一订单号）
3. 断言：只有 1 次支付成功，其余返回"订单已支付"错误码
4. 断言：用户余额只扣减 1 次

四、通用要求：
1. 使用 threading.Thread 或 asyncio.gather 实现并发
2. 每个并发测试用例运行时，独立准备数据，运行后自动清理
3. 断言中加入数据库层面的校验（直接查表验证数据一致性）
4. 测试超时时间设置为 30 秒，避免死锁卡住 CI 流水线
```

### 1.5 CRUD 全生命周期测试

> 单接口测试孤立无法发现数据流转过程中的问题。用全生命周期测试覆盖"创建 → 查询 → 更新 → 删除"完整链路。

```text
基于项目 CLAUDE.md 规范，为 /api/v1/resource 模块生成 CRUD 全生命周期测试

接口列表：
- POST   /api/v1/resource/create    — 创建资源
- GET    /api/v1/resource/{id}      — 查询资源详情
- GET    /api/v1/resource/list      — 查询资源列表
- PUT    /api/v1/resource/{id}      — 更新资源
- DELETE /api/v1/resource/{id}      — 删除资源
- GET    /api/v1/resource/deleted   — 查询已删除资源（回收站）

要求：
1. 组织为 Class 级别的测试类，共享 fixture 创建的测试数据：

   class TestResourceLifecycle:
       def test_01_create(self, resource_fixture):
           # 创建资源 → 验证返回 resource_id → 保存到 fixture
       def test_02_query_detail(self, resource_fixture):
           # 用上一步的 resource_id 查询 → 验证字段与创建时一致
       def test_03_query_list(self, resource_fixture):
           # 查询列表 → 验证列表中包含刚创建的资源
       def test_04_update(self, resource_fixture):
           # 更新资源 → 验证返回成功 → 再次查询验证字段已变更
       def test_05_delete(self, resource_fixture):
           # 删除资源 → 验证返回成功 → 再次查询返回 404
       def test_06_query_deleted(self, resource_fixture):
           # 查询回收站 → 验证已删除资源出现在列表中 → 验证不可再操作

2. 每个步骤断言以下三个层面的一致性：
   - API 层面：状态码和响应结构正确
   - 缓存层面：Redis 缓存与 API 返回一致（如有缓存层）
   - 数据库层面：直接查表，验证数据与 API 返回一致

3. 使用 pytest-ordering 或 pytest-dependency 管理用例执行顺序
   （仅在同一个 Class 内部有顺序依赖，不同 Class 之间完全独立）

4. 测试完成后通过 fixture teardown 清理所有测试数据
5. 加入 @allure.feature("资源管理") 和 @allure.story("全生命周期") 装饰器
```

---

### 2. WebUI POM 测试用例生成模板

```text
基于项目 CLAUDE.md 编码规范，遵循页面对象模型
参考 @tests/ui/pages/login_page.py 的写法，为订单创建页面生成 POM 类和测试用例

页面信息：
- 页面 URL：https://test.example.com/order/create
- 页面元素：
  - 商品选择下拉框：id=product-select
  - 数量输入框：id=quantity-input
  - 地址选择下拉框：id=address-select
  - 提交按钮：id=submit-btn
  - 成功提示：text=订单创建成功
  - 错误提示：class=error-message

要求：
1. 先生成 OrderCreatePage 类，封装所有元素定位和操作方法
2. 操作方法包括：选择商品、输入数量、选择地址、点击提交、获取成功提示、获取错误提示
3. 生成测试用例，覆盖：
   - 正常创建订单成功
   - 不选择商品提交，显示错误提示
   - 输入数量为 0，显示错误提示
   - 不选择地址提交，显示错误提示
4. 使用 browser 和 page fixture，每个用例独立浏览器会话
5. 失败时自动截图，加入 Allure 报告步骤
6. 元素定位优先使用 CSS 选择器，避免不稳定的 XPath
7. 加入智能等待，避免页面加载导致的用例失败
```

### 3. 异常/边界值用例生成模板（手动最容易漏）

```text
为 @tests/api/test_order.py 中的 test_create_order 用例，补充完整的异常和边界值测试用例

要求：
1. 覆盖所有可能的异常场景：
   - 请求头缺失/错误
   - 请求体格式错误（非 JSON）
   - 所有必填参数缺失
   - 所有参数类型错误（比如 product_id 传字符串）
   - 所有参数值非法（比如 product_id=-1、quantity=1000000）
   - 超长字符串参数（超过数据库字段长度）
   - 特殊字符参数（SQL 注入、XSS 字符）
   - 重复提交相同订单
2. 每个异常场景单独一个用例，断言对应的错误码和错误信息
3. 不要修改原有正常用例，只新增异常用例
4. 保持和原有代码相同的风格和规范
```

### 4. 从需求文档生成用例模板

```text
根据以下需求文档，为用户登录功能生成完整的测试用例清单和自动化测试代码

需求文档：
1. 用户输入正确的用户名和密码，登录成功，跳转到首页
2. 用户输入不存在的用户名，提示"用户不存在"
3. 用户输入错误的密码，提示"密码错误"，连续输错 5 次锁定账号 1 小时
4. 用户输入空的用户名或密码，提示"用户名/密码不能为空"
5. 登录成功后，7 天内免登录
6. 支持手机号和邮箱两种登录方式

要求：
1. 先生成测试用例清单，包含用例ID、用例名称、前置条件、操作步骤、预期结果
2. 再根据用例清单生成对应的 Pytest 自动化测试代码
3. 覆盖所有需求点，包括正常、异常、边界、性能场景
4. 代码符合项目规范，继承现有基类和 fixture
```

---

## 四、功能测试用例深度实战

> 接口测试关注"对不对"，功能测试关注"好不好用"。下面是用 Claude Code 生成专业级功能测试用例的完整方法。

### 1. 业务流程端到端测试（E2E Scenario）

> 用户不会只用单个接口，而是走完一个完整的业务流程。端到端测试模拟真实用户路径，是最容易发现集成问题的测试类型。

```text
基于项目 CLAUDE.md 规范，继承 @core/base_api.py，
参考 @services/order_workflow.py 的业务流程，
为「用户从注册到下单成功」的完整链路生成端到端测试用例

业务链路：
注册账号 → 登录获取 token → 浏览商品列表 → 加入购物车 →
创建收货地址 → 提交订单 → 支付订单 → 查看订单状态 →
确认收货 → 申请售后（部分退款）

要求：
1. 按业务步骤顺序编写，每步做完后用 assert 验证当前状态再进入下一步
2. 每步的断言包含：
   - API 层面：状态码、响应数据字段正确
   - 业务层面：订单金额计算正确、库存扣减正确、优惠券抵扣正确
   - 数据层面：查数据库验证订单/支付/地址表数据一致

3. 覆盖以下分支场景：
   主线流程（全部正常）：
   - 注册 → 登录 → 加购 → 下单 → 支付 → 发货 → 收货 → 完成

   异常分支：
   - 支付时余额不足 → 切换支付方式 → 支付成功
   - 下单时优惠券过期 → 不使用优惠券 → 下单成功
   - 支付前取消订单 → 订单状态变为 cancelled → 库存恢复

   边界分支：
   - 购物车加入 0 件商品 → 提示错误
   - 购物车加入 999 件商品（超过库存）→ 下单时提示库存不足

4. 每个分支场景独立为一个 test_ 方法，前置条件在 fixture 中准备
5. 使用 @allure.feature("用户下单全流程") 标记，每个步骤用 @allure.step 装饰
6. 测试完成后通过 fixture teardown 清理所有测试用户和订单数据
```

### 2. 状态机转换测试

> 订单、工单、审批等业务对象有严格的状态流转规则（比如"已支付→已取消"就是非法跳转）。Claude 可以自动生成状态迁移矩阵和测试用例。

```text
参考 @models/order.py 中 Order 模型的状态定义和 @services/order_workflow.py 的状态流转逻辑，
生成订单状态机的完整测试用例

订单状态枚举：
PENDING_PAY（待支付）→ PAID（已支付）→ SHIPPED（已发货）→ DELIVERED（已签收）→ COMPLETED（已完成）
PENDING_PAY → CANCELLED（已取消）
PAID → REFUNDING（退款中）→ REFUNDED（已退款）
SHIPPED → RETURNING（退货中）→ RETURNED（已退货）

合法状态转换：
PENDING_PAY → PAID（支付成功）
PENDING_PAY → CANCELLED（用户取消/超时取消）
PAID → SHIPPED（商家发货）
PAID → REFUNDING（用户申请退款）
SHIPPED → DELIVERED（用户签收）
SHIPPED → RETURNING（用户申请退货）
DELIVERED → COMPLETED（用户确认/超时自动确认）
REFUNDING → REFUNDED（退款完成）
RETURNING → RETURNED（退货完成）

要求：
1. 生成状态转移矩阵表（markdown 格式），标注每个转移是否合法
2. 对每个合法转移，生成一个测试用例验证转移成功：
   - 创建状态的订单 → 调用转移接口 → 验证新状态正确 → 验证关联操作执行
   （如 PAID → SHIPPED 时验证库存扣减、物流单号生成）
3. 对每个非法转移，生成一个测试用例验证转移失败：
   - 创建状态的订单 → 调用非法转移接口 → 验证返回错误码 → 验证状态未改变
   非法转移示例：PAID → CANCELLED（已支付订单不能取消）、
              SHIPPED → CANCELLED（已发货不能取消）
4. 测试数据从 @data/order_states.py 的状态配置读取
5. 每个用例独立创建订单，不共享状态
```

### 3. 数据一致性校验（接口 vs 缓存 vs 数据库）

> 分布式系统中，接口返回、Redis 缓存、数据库三者的数据可能不一致。这是线上 Bug 的重灾区。用 Claude 生成三方对账测试。

```text
基于项目 CLAUDE.md 规范，为 POST /api/v1/user/update 接口
生成数据一致性校验测试用例

被测接口：更新用户信息（昵称、头像、手机号）
系统架构：API → Redis（热数据缓存）→ MySQL（持久化存储）
          API → Kafka（数据变更消息）→ ES（搜索索引）

要求：
1. 每个更新操作后，做三方数据校验：
   - 接口返回的数据
   - Redis 缓存中的数据（直接调用 redis_client.get()）
   - MySQL 数据库中的数据（直接执行 SQL 查询）
   → 三者必须完全一致

2. 覆盖以下一致性场景：

   写入一致性：
   - 更新昵称后 → 验证 API 返回 / Redis / MySQL 中的昵称都一致
   - 更新头像 URL 后 → 同上
   - 同时更新昵称和手机号 → 验证所有字段三方一致

   缓存失效一致性：
   - 更新用户信息后 → 验证 Redis 中的旧数据已被删除或更新
   - 更新后立即查询 → 验证 API 返回的是新数据（不是缓存中的旧数据）

   最终一致性（ES）：
   - 更新用户信息后 → 等待 5 秒 → 查询 ES 搜索索引
   - 验证 ES 中的用户信息已同步更新（允许 5 秒延迟）

   事务回滚一致性：
   - 模拟更新成功但缓存写入失败 → 验证 MySQL 中数据已回滚
   - 模拟更新成功但消息发送失败 → 验证重试机制触发

3. 使用 @pytest.fixture 创建 clean_redis 和 clean_es fixture，
   测试前清理缓存和索引，测试后恢复
4. 每个校验失败时，输出三方数据的具体差异信息
```

### 4. 权限与角色矩阵测试

> RBAC 权限系统的测试组合呈指数增长，手动写容易遗漏。让 Claude 根据角色-权限映射表自动生成矩阵用例。

```text
参考 @config/permissions.py 中的角色权限定义，
为以下接口生成权限矩阵测试用例

角色定义：
- admin：超级管理员，拥有所有权限
- editor：编辑者，可增删改查自己的内容
- viewer：观察者，只能查看
- anonymous：未登录用户

被测接口：
- GET    /api/v1/article/{id}       — 查看文章
- POST   /api/v1/article/create     — 创建文章
- PUT    /api/v1/article/{id}       — 编辑文章
- DELETE /api/v1/article/{id}       — 删除文章
- GET    /api/v1/article/draft      — 查看草稿列表
- PUT    /api/v1/article/{id}/publish — 发布文章
- DELETE /api/v1/user/{id}          — 删除用户（仅 admin）

要求：
1. 生成角色 × 接口的权限矩阵表（markdown），标出每个组合是否允许访问

2. 对每个「允许」的组合 → 生成正向测试：用该角色调用接口 → 验证 200
3. 对每个「拒绝」的组合 → 生成反向测试：用该角色调用接口 → 验证 403

4. 特别注意以下边界权限场景：
   - editor 编辑别人的文章 → 应返回 403
   - editor 删除别人的文章 → 应返回 403
   - viewer 尝试创建文章 → 应返回 403
   - anonymous 访问任何需要登录的接口 → 应返回 401

5. 使用 @pytest.mark.parametrize 按角色分组，
   用 conftest.py 中的不同 role_client fixture 注入不同角色的认证 token
6. 测试数据：每个角色预置 1 个测试用户，每个 editor 预置 1 篇自己的文章
```

### 5. 多角色协作场景测试

> 单角色测试通过不代表业务流程跑得通。多角色协作场景涉及并发操作、权限交叉、数据可见性等问题。

```text
基于项目 CLAUDE.md 规范，使用多个 fixture 模拟不同角色的并发操作，
为「文章协作编辑」功能生成多角色协作场景测试用例

业务场景：文章协作编辑
- 作者 A（editor）创建文章草稿
- 审核员 B（reviewer）审核通过 → 文章状态变为 published
- 编辑 C（editor）发现错误 → 提交修改建议 → 创建修订版本
- 作者 A 接受修订 → 更新文章
- 审核员 B 重新审核 → 通过

要求：

场景一：正常协作流程
1. editor_A 创建草稿 → 验证草稿仅 editor_A 和 admin 可见
2. editor_A 提交审核 → 验证 article.status = "pending_review"
3. reviewer 审核通过 → 验证 article.status = "published" → 验证对所有人可见
4. editor_C 发现错误 → 创建修订版本 → 验证 article.status = "revision_pending"
5. editor_A 接受修订 → 验证文章内容已更新 → article.status = "published"
6. reviewer 重新审核 → 通过 → 验证 revision 记录被标记为 resolved

场景二：并发修改冲突
1. editor_A 和 editor_C 同时打开同一篇文章编辑
2. editor_A 先提交保存 → 成功
3. editor_C 后提交保存 → 检测到版本冲突 → 返回 409 Conflict
4. 验证 editor_C 的修改未被保存，article.content 为 editor_A 的版本

场景三：权限交叉验证
1. editor_A 创建文章（article.author_id = editor_A.id）
2. editor_C 尝试直接修改 editor_A 的草稿 → 验证 403
3. editor_C 尝试提交审核 editor_A 的草稿 → 验证 403
4. admin 可以修改任何文章 → 验证 200

要求：
1. 使用 conftest.py 中预定义的 editor_a_client、editor_c_client、
   reviewer_client、admin_client fixture
2. 每个场景的测试用例按操作顺序编写，中间步骤用 assert 验证
3. 并发冲突测试使用 threading.Thread 模拟
4. 测试完成后清理所有测试文章和修订记录
```

### 6. 配置开关与灰度功能测试

> 功能开关（Feature Flag）和灰度发布是现代系统的标配。测试需要覆盖开关开启/关闭、灰度比例、白名单/黑名单等场景。

```text
参考 @config/feature_flags.py 中的功能开关配置，
为「新支付方式灰度发布」功能生成测试用例

功能开关配置：
- feature.new_payment.enabled：总开关（true/false）
- feature.new_payment.percentage：灰度比例（0-100）
- feature.new_payment.whitelist：白名单用户ID列表
- feature.new_payment.blacklist：黑名单用户ID列表

优先级：白名单 > 黑名单 > 开关 > 灰度比例

业务行为：
- 开关关闭 → 所有用户使用旧支付方式
- 开关开启 + 白名单命中 → 使用新支付方式
- 开关开启 + 黑名单命中 → 使用旧支付方式
- 开关开启 + 非白非黑 + 灰度比例命中 → 使用新支付方式
- 开关开启 + 非白非黑 + 灰度比例未命中 → 使用旧支付方式

要求：
1. 使用 @pytest.mark.parametrize 覆盖以下组合（至少 15 组）：

   | 开关 | 百分比 | 用户类型 | 预期 |
   |------|--------|----------|------|
   | false | - | 任意 | 旧支付 |
   | true | 100 | 白名单 | 新支付 |
   | true | 0 | 白名单 | 新支付（白名单优先）|
   | true | 100 | 黑名单 | 旧支付（黑名单优先）|
   | true | 100 | 普通 | 新支付 |
   | true | 0 | 普通 | 旧支付 |
   | true | 50 | 特殊UID | 验证哈希取模逻辑 |

2. 通过 admin API 动态修改开关配置，测试完成后恢复默认值
3. 验证灰度哈希算法的一致性：同一用户多次请求 → 始终看到同一个支付方式
4. 验证灰度比例的统计准确性：1000 个请求 × 50% 灰度 → 新支付比例在 45%-55% 之间
5. 使用 @data/feature_flag_test_cases.py 存放测试数据集
```

---

## 五、真实需求 → 用例全流程实战

> **需求**：生成用户注册接口的自动化测试用例

### 步骤 1：写一个高质量的 Prompt

```text
基于项目 CLAUDE.md 编码规范，继承 @core/base_api.py 的 BaseAPI 类，使用 api_client fixture
为 POST /api/v1/user/register 接口生成完整测试用例

接口信息：
- 请求方法：POST
- 请求参数：
  {
    "username": "string(3-20字符)",
    "password": "string(6-20字符)",
    "email": "string(邮箱格式)"
  }
- 正常响应：{"code": 200, "data": {"user_id": int}, "msg": "注册成功"}
- 异常响应：{"code": 400, "msg": "参数错误"}

要求：
1. 覆盖所有场景：正常、异常、边界值
2. 断言分层：状态码 → 响应结构 → 业务字段
3. 测试数据从 @data/test_data.py 读取，无硬编码
4. 用例独立，无执行顺序依赖
5. 加入异常捕获和日志
6. 代码通过 Ruff + SonarQube 检查
```

### 步骤 2：让 Claude 生成初稿

Claude 会自动读取 `base_api.py` 和 `test_data.py`，生成符合规范的用例，不用你手动改基类引用。

### 步骤 3：增量优化（关键！）

```text
# 优化1：增加 SQL 注入和 XSS 异常用例
新增 2 个安全测试用例：用户名包含 SQL 注入语句、用户名包含 XSS 脚本

# 优化2：完善断言
给所有用例增加 JSON Schema 响应结构校验，确保接口返回格式稳定

# 优化3：复用 fixture
使用 @tests/api/conftest.py 中的 clean_user fixture，测试完成后自动删除测试用户
```

### 步骤 4：自动质检

- 保存文件，Ruff 自动格式化和修复基础问题
- 查看 SonarQube 警告，处理断言不规范、重复代码等问题
- 执行 `pytest tests/api/test_register.py -v`，验证用例能正常运行

---

## 六、避坑指南：AI 生成用例常见问题与解决

### 1. ❌ 生成的用例有硬编码

**解决**：在 Prompt 里强制要求——

> 所有配置、账号、测试数据必须从 `config/settings.py` 或 `data/test_data.py` 读取，绝对禁止硬编码任何字符串或数字。

### 2. ❌ 断言太笼统（只有 `assert resp`）

**解决**：在 Prompt 里明确断言标准——

> 断言必须分层：先断言 `resp.status_code == 200`，再断言 `resp.json()["code"] == 200`，最后断言具体业务字段 `resp.json()["data"]["user_id"] > 0`。禁止使用 `assert resp` 或 `assert resp.json()`。

### 3. ❌ 用例有执行顺序依赖

**解决**：在 Prompt 里要求——

> 每个用例必须独立，不能依赖上一个用例的执行结果。所有前置数据在 fixture 中准备，测试完成后自动清理。

### 4. ❌ 不遵循现有项目架构

**解决**：使用 `@文件路径` 语法，让 Claude 读取现有基类和用例——

> 参考 `@tests/api/test_login.py` 的写法，保持相同的代码风格和结构，继承 `@core/base_api.py` 基类。

### 5. ❌ 异常场景覆盖不全

**解决**：在 Prompt 里明确要求覆盖的异常类型——

> 必须覆盖：参数缺失、参数类型错误、参数值非法、请求头错误、权限不足、重复提交、超长字符串、特殊字符。

---

## 七、进阶技巧：让 AI 生成的用例质量再上一个台阶

### 1. 给 AI 一个「好例子」

```text
参考这个高质量用例的写法：@tests/api/test_login.py
为 /api/v1/user/info 接口生成相同质量的用例
```

AI 会模仿好例子的结构、断言、异常处理方式，生成的用例质量会大幅提升。

### 2. 要求生成测试数据

```text
同时生成对应的测试数据，保存到 @data/test_data.py 的 register_test_data 变量中
```

不用手动写测试数据，AI 会自动生成合法和非法的测试数据。

### 3. 要求加入 Allure 报告支持

```text
所有用例加入 Allure 报告步骤，用 @allure.step 装饰关键操作，失败时自动附加请求和响应信息
```

生成的用例直接支持 Allure 报告，不用后期手动加。

### 4. 要求生成单元测试

```text
同时为 @core/base_api.py 中的 request 方法生成单元测试用例，覆盖所有异常情况
```

不仅能生成业务用例，还能生成框架代码的单元测试。

---

## 八、终极效率技巧：保存为自定义 Skill

把常用的 Prompt 模板保存为 Claude Code 自定义 Skill，以后直接调用，不用每次重写：

| 项目 | 内容 |
|------|------|
| **技能名** | `generate-api-test` |
| **技能内容** | 上面的 API 用例生成模板 |
| **调用方式** | `/skill generate-api-test /api/v1/order/create` |

> 这样你只需要输入接口地址，就能一键生成完整的测试用例，效率大幅提升。

---

*本文基于 Claude Code 实战经验编写，持续更新中。*

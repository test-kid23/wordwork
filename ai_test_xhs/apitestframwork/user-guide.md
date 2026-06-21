# ApiTest 功能使用指南

> 本文档面向平台终端用户，详细说明每个功能的使用方法和操作示例。

---

## 目录

- [1. 快速入门](#1-快速入门)
- [2. 命名空间管理](#2-命名空间管理)
- [3. 用例管理](#3-用例管理)
- [4. 执行与报告](#4-执行与报告)
- [5. 测试套件](#5-测试套件)
- [6. Mock 服务](#6-mock-服务)
- [7. 性能测试](#7-性能测试)
- [8. Webhook 集成](#8-webhook-集成)
- [9. 定时任务](#9-定时任务)
- [10. 分布式执行节点](#10-分布式执行节点)
- [11. 插件系统](#11-插件系统)
- [12. 权限管理](#12-权限管理)
- [13. 审计日志](#13-审计日志)
- [14. 多语言支持](#14-多语言支持)
- [附录：API 接口总览](#附录api-接口总览)

---

## 1. 快速入门

### 1.1 登录与认证

系统使用 JWT Token 进行身份认证。首次使用需由管理员创建账户。

**前端登录**：访问平台首页，在登录页面输入用户名和密码即可。

**API 登录**：

```bash
# 登录获取 Token（支持用户名或邮箱登录）
curl -X POST http://<host>:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your_password"}'

# 响应示例
# {"token":"eyJ...","user":{"id":1,"username":"admin","role":"admin"}}

# 后续所有 API 请求需携带 Token
curl http://<host>:5000/api/v1/namespace \
  -H "Authorization: Bearer eyJ..."
```

### 1.2 基本工作流程

```
创建命名空间 → 配置环境变量 → 编写 YAML 用例 → 执行用例 → 查看报告
```

1. **创建命名空间**：组织用例的顶层容器，配置全局变量和环境变量
2. **编写用例**：使用 YAML 格式定义请求和断言
3. **执行用例**：支持同步/异步、单个/批量执行
4. **查看报告**：在线查看结果，或导出 HTML/PDF/Allure 报告

---

## 2. 命名空间管理

命名空间是用例、Mock、Webhook 等资源的顶层组织单元，支持层级结构。

### 2.1 创建命名空间

**前端操作**：点击左侧导航「命名空间」→ 右上角「新建」按钮。

**API 方式**：

```bash
curl -X POST http://<host>:5000/api/v1/namespace \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "电商项目",
    "description": "电商 API 自动化测试",
    "global_variables": {
      "base_url": "https://api.example.com",
      "api_version": "v2"
    },
    "env_config": {
      "dev": {"base_url": "http://dev.example.com"},
      "staging": {"base_url": "https://staging.example.com"},
      "prod": {"base_url": "https://api.example.com"}
    }
  }'
```

### 2.2 层级命名空间

支持通过 `parent_id` 创建父子层级关系，适合按项目/模块/服务组织。

```
公司项目（根）
├── 用户服务
│   ├── 登录模块
│   └── 注册模块
└── 订单服务
    ├── 下单模块
    └── 支付模块
```

**查看树结构**：

```bash
curl http://<host>:5000/api/v1/namespace/tree \
  -H "Authorization: Bearer <token>"
```

### 2.3 环境变量配置

每个命名空间可配置多套环境变量，执行时根据环境名称覆盖全局变量：

```json
{
  "global_variables": {"base_url": "https://api.example.com", "timeout": 30},
  "env_config": {
    "dev": {"base_url": "http://localhost:8080", "timeout": 60},
    "prod": {"base_url": "https://api.example.com", "timeout": 30}
  }
}
```

### 2.4 全局变量设置

`global_variables` 中的变量可在所有用例中通过 `${变量名}` 引用。支持嵌套对象：

```yaml
# 命名空间全局变量
global_variables:
  db_host: "192.168.1.100"
  credentials:
    username: "testuser"
    password: "testpass"

# 用例中引用
request:
  url: ${base_url}/api/users
  headers:
    Authorization: "Basic ${credentials.username}:${credentials.password}"
```

---

## 3. 用例管理

### 3.1 YAML 用例格式

每个用例由 YAML 定义，包含请求配置、断言规则和变量提取三部分。

#### 单用例格式

```yaml
name: 用户登录测试
variables:                        # 用例级变量（可选）
  username: testuser
  password: "123456"
request:
  method: POST                    # HTTP 方法：GET/POST/PUT/DELETE/PATCH
  url: ${base_url}/auth/login     # 支持变量引用
  headers:                        # 请求头
    Content-Type: application/json
    Authorization: Bearer ${token}
  body:                           # 请求体（POST/PUT/PATCH）
    username: ${username}
    password: ${password}
  params:                         # URL 查询参数（可选）
    remember: true
  timeout: 30                     # 请求超时（秒），可选，默认 30s
extract:                          # 提取响应字段（可选）
  user_id: $.data.id              # JSONPath 语法
  auth_token: $.token
assertions:                       # 断言列表
  - type: status_code
    expected: 200
  - type: json_field
    field: $.data.id
    expected: 1
```

#### 数据驱动（多用例 + 并行）

```yaml
name: 批量用户查询
parallel: 5                # 并行度，默认 1（串行）
timeout: 300               # 套件总超时（秒）
variables:
  base_path: /api/users
test_cases:
  - name: 查询用户1
    variables:
      user_id: 1
    request:
      method: GET
      url: ${base_url}${base_path}/${user_id}
    extract:
      user_name: $.data.name
    assertions:
      - type: status_code
        expected: 200
  - name: 查询用户2（引用上游变量）
    variables:
      user_id: 2
    request:
      method: GET
      url: ${base_url}${base_path}/${user_id}
    assertions:
      - type: json_field
        field: $.data.name
        expected: ${user_name}    # 引用上游 extract 的变量
```

### 3.2 创建用例

**前端操作**：进入命名空间 → 点击「用例管理」→ 「新建用例」→ 在 CodeMirror 编辑器中编写 YAML → 保存。

**API 方式**：

```bash
curl -X POST http://<host>:5000/api/v1/testcase \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "namespace_id": 1,
    "name": "登录接口测试",
    "description": "验证登录接口返回正确 Token",
    "yaml_content": "name: 登录接口测试\nrequest:\n  method: POST\n  url: ${base_url}/auth/login\n  headers:\n    Content-Type: application/json\n  body:\n    username: test\n    password: 123456\nassertions:\n  - type: status_code\n    expected: 200\n  - type: not_null\n    field: $.token",
    "tags": ["smoke", "login"]
  }'
```

### 3.3 变量系统

#### 三级变量覆盖

变量解析优先级（从高到低）：

```
用例级 variables > 环境变量覆盖（env_config） > 命名空间全局变量（global_variables）
```

高优先级变量会覆盖同名低优先级变量，适合在不同环境中复用同一用例。

#### 变量引用语法

支持 `${var}` 和 `${nested.path}` 两种语法：

```yaml
variables:
  user:
    name: test
    role: admin
request:
  url: ${base_url}/users/${user.name}
  # 解析为: https://api.example.com/users/test
```

#### 用例间变量传递（extract）

通过 `extract` 字段提取响应数据供下游用例使用：

```yaml
# 用例 A：登录并提取 Token
extract:
  token: $.data.token              # JSONPath 提取
  user_id: $.data.user.id          # 嵌套路径

# 用例 B：引用上游提取的变量
request:
  headers:
    Authorization: Bearer ${token}
  url: ${base_url}/users/${user_id}
```

### 3.4 断言引擎

系统内置 10 种断言类型，覆盖常见验证场景：

| 断言类型 | 说明 | 示例 |
|---------|------|------|
| `status_code` | HTTP 状态码 | `expected: 200` |
| `json_field` | JSON 字段值匹配 | `field: $.data.id, expected: 1` |
| `contains` | 内容包含 | `field: $.data.name, expected: "test"` |
| `regex` | 正则匹配 | `field: $.data.email, expected: "^[\\w.]+@[\\w.]+$"` |
| `json_schema` | JSON Schema 验证 | `expected: {"type": "object", "required": ["id"]}` |
| `header` | 响应头匹配 | `field: Content-Type, expected: application/json` |
| `response_time` | 响应时间上限 | `expected: 1000`（毫秒） |
| `array_length` | 数组长度 | `field: $.data.list, expected: 10` |
| `not_null` | 非空检查 | `field: $.data.token` |
| `type_check` | 类型检查 | `field: $.data.count, expected: integer` |

完整断言示例：

```yaml
assertions:
  - type: status_code
    expected: 200
  - type: json_field
    field: $.data.id
    expected: 1
  - type: contains
    field: $.data.name
    expected: "test"
  - type: regex
    field: $.data.email
    expected: "^[\\w.]+@[\\w.]+$"
  - type: json_schema
    expected: {"type": "object", "required": ["id", "name"]}
  - type: header
    field: Content-Type
    expected: application/json
  - type: response_time
    expected: 1000              # 响应时间 < 1000ms
  - type: array_length
    field: $.data.list
    expected: 10
  - type: not_null
    field: $.data.token
  - type: type_check
    field: $.data.count
    expected: integer           # 支持: string, integer, float, boolean, array, object, null
```

断言引擎支持插件式扩展，可通过插件系统注册自定义断言类型。

### 3.5 用例导入导出

**导出**：将命名空间下所有用例打包为 ZIP 下载。

```bash
# 导出 ZIP
curl -o testcases.zip \
  "http://<host>:5000/api/v1/testcase/export?namespace_id=1" \
  -H "Authorization: Bearer <token>"
```

**导入**：上传 YAML 文件或 ZIP 包，支持 3 种冲突策略：

| 策略 | 说明 |
|------|------|
| `skip` | 同名用例跳过（默认） |
| `rename` | 同名用例自动重命名 |
| `overwrite` | 覆盖同名用例 |

```bash
# 导入 ZIP
curl -X POST \
  "http://<host>:5000/api/v1/testcase/import?namespace_id=1&conflict_strategy=skip" \
  -H "Authorization: Bearer <token>" \
  -F "file=@testcases.zip"
```

### 3.6 标签管理

创建用例时可通过 `tags` 字段添加标签，便于分类和过滤：

```bash
# 创建带标签的用例
curl -X POST http://<host>:5000/api/v1/testcase \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "namespace_id": 1,
    "name": "登录测试",
    "yaml_content": "...",
    "tags": ["smoke", "P0", "login"]
  }'

# 按标签筛选
curl "http://<host>:5000/api/v1/testcase?namespace_id=1&tags=smoke,P0" \
  -H "Authorization: Bearer <token>"
```

### 3.7 版本管理

每次更新用例 YAML 内容时，系统自动创建版本快照，支持 diff 对比和一键回滚。

```bash
# 查看版本列表
curl http://<host>:5000/api/v1/testcase/1/versions \
  -H "Authorization: Bearer <token>"

# 查看某个版本的详细内容
curl http://<host>:5000/api/v1/testcase/1/versions/3 \
  -H "Authorization: Bearer <token>"

# 对比两个版本的差异
curl http://<host>:5000/api/v1/testcase/1/versions/2/diff/3 \
  -H "Authorization: Bearer <token>"

# 回滚到指定版本
curl -X POST http://<host>:5000/api/v1/testcase/1/versions/3/rollback \
  -H "Authorization: Bearer <token>"
```

### 3.8 用例评审流程

用例从编写到上线的审批流程，支持状态机流转：

```
draft → pending_review → approved
                      ↘ rejected → draft（修改后重新提交）
```

| 状态 | 说明 | 可操作角色 |
|------|------|-----------|
| `draft` | 草稿，可自由编辑 | 所有编辑者 |
| `pending_review` | 待审核 | 提交人 |
| `approved` | 已通过 | admin / manager |
| `rejected` | 已驳回，需修改 | admin / manager |

```bash
# 提交评审
curl -X POST http://<host>:5000/api/v1/testcase/1/review/submit \
  -H "Authorization: Bearer <token>"

# 批准（仅 admin/manager）
curl -X POST http://<host>:5000/api/v1/testcase/1/review/approve \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"review_id": 1, "comments": "审核通过"}'

# 驳回（仅 admin/manager，必须填写原因）
curl -X POST http://<host>:5000/api/v1/testcase/1/review/reject \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"review_id": 1, "comments": "需要增加异常场景覆盖"}'

# 重置为草稿（从 approved/rejected 状态）
curl -X POST http://<host>:5000/api/v1/testcase/1/review/reset \
  -H "Authorization: Bearer <token>"

# 查看评审记录
curl http://<host>:5000/api/v1/testcase/1/reviews \
  -H "Authorization: Bearer <token>"
```

---

## 4. 执行与报告

### 4.1 触发执行

支持两种执行模式：

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| 同步执行 | 请求阻塞等待结果返回 | 快速调试、单用例 |
| 异步执行 | 提交到 Celery 队列，轮询状态 | 批量执行、长耗时用例 |

```bash
# 方式一：执行已保存的用例（按 ID）
curl -X POST http://<host>:5000/api/v1/execution/run \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"testcase_id": 1, "async_mode": false}'

# 方式二：直接传入 YAML 执行
curl -X POST http://<host>:5000/api/v1/execution/run \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "namespace_id": 1,
    "yaml_content": "name: 快速测试\nrequest:\n  method: GET\n  url: ${base_url}/health\nassertions:\n  - type: status_code\n    expected: 200",
    "async_mode": true
  }'

# 异步模式响应（202）
# {"record_id":1,"task_id":"xxx","status":"pending","poll_url":"/api/v1/execution/records/1/status"}
```

**批量执行**（多用例合并为一个套件）：

```bash
# 按用例 ID 列表批量执行
curl -X POST http://<host>:5000/api/v1/execution/batch-run \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"testcase_ids": [1, 2, 3, 5]}'

# 按标签批量执行
curl -X POST http://<host>:5000/api/v1/execution/batch-run \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"namespace_id": 1, "tags": ["smoke"]}'
```

### 4.2 执行记录查看

```bash
# 轮询异步执行状态
curl http://<host>:5000/api/v1/execution/records/1/status \
  -H "Authorization: Bearer <token>"
# → {"id":1,"status":"pass","total":1,"passed":1,"failed":0,...}

# 查看执行详情（含完整报告）
curl http://<host>:5000/api/v1/execution/records/1 \
  -H "Authorization: Bearer <token>"

# 执行记录列表（分页 + 筛选）
curl "http://<host>:5000/api/v1/execution/records?namespace_id=1&status=fail&page=1" \
  -H "Authorization: Bearer <token>"

# 取消正在执行的异步任务
curl -X POST http://<host>:5000/api/v1/execution/records/1/cancel \
  -H "Authorization: Bearer <token>"
```

### 4.3 报告导出

支持 3 种报告格式：

```bash
# HTML 报告（在线预览）
curl "http://<host>:5000/api/v1/execution/records/1/export?format=html" \
  -H "Authorization: Bearer <token>"

# HTML 报告（下载）
curl "http://<host>:5000/api/v1/execution/records/1/export?format=html&download=true" \
  -H "Authorization: Bearer <token>" -o report.html

# PDF 报告（下载）
curl "http://<host>:5000/api/v1/execution/records/1/export?format=pdf" \
  -H "Authorization: Bearer <token>" -o report.pdf

# Allure HTML 报告（单文件）
curl "http://<host>:5000/api/v1/execution/records/1/allure-export?mode=html" \
  -H "Authorization: Bearer <token>" -o allure-report.html

# Allure Results（JSON ZIP，可本地 allure generate）
curl "http://<host>:5000/api/v1/execution/records/1/allure-export?mode=results" \
  -H "Authorization: Bearer <token>" -o allure-results.zip
```

### 4.4 趋势图表

```bash
# 获取最近 30 天的执行趋势
curl "http://<host>:5000/api/v1/execution/trends?namespace_id=1&days=30" \
  -H "Authorization: Bearer <token>"

# 响应包含：每日统计（总数/通过/失败/通过率/平均耗时）+ 失败 Top5 用例
```

---

## 5. 测试套件

测试套件是将多个用例组织为固定集合，方便一键执行和定时调度。

### 5.1 创建套件

```bash
curl -X POST http://<host>:5000/api/v1/test-suite \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "namespace_id": 1,
    "name": "冒烟测试套件",
    "description": "核心接口冒烟测试",
    "testcase_ids": [1, 2, 3, 5, 8]
  }'
```

### 5.2 执行套件

```bash
# 一键执行套件中的所有用例
curl -X POST http://<host>:5000/api/v1/test-suite/1/run \
  -H "Authorization: Bearer <token>"
```

### 5.3 管理套件

```bash
# 查看套件列表
curl "http://<host>:5000/api/v1/test-suite?namespace_id=1" \
  -H "Authorization: Bearer <token>"

# 更新套件（增减用例）
curl -X PUT http://<host>:5000/api/v1/test-suite/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"testcase_ids": [1, 2, 3, 5, 8, 10]}'

# 删除套件
curl -X DELETE http://<host>:5000/api/v1/test-suite/1 \
  -H "Authorization: Bearer <token>"
```

---

## 6. Mock 服务

API Mock 服务允许创建虚拟端点，用于前后端开发解耦和测试数据模拟。

### 6.1 创建 Mock 端点

```bash
curl -X POST http://<host>:5000/api/v1/mock \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "namespace_id": 1,
    "method": "GET",
    "url_pattern": "/api/users/:id",
    "response_status": 200,
    "response_headers": {"Content-Type": "application/json"},
    "response_body": "{\"id\": {{ params.id }}, \"name\": \"Mock User\", \"email\": \"mock@example.com\"}",
    "delay_ms": 100,
    "is_active": true
  }'
```

### 6.2 URL 参数匹配

使用 `:param` 语法定义路径参数，匹配时自动提取：

| 模式 | 匹配请求 |
|------|---------|
| `/api/users/:id` | `/api/users/123` → `params.id = "123"` |
| `/api/:version/users/:id` | `/api/v2/users/456` → `params.version = "v2"`, `params.id = "456"` |

### 6.3 Jinja2 模板渲染

响应体支持 Jinja2 模板语法，可动态引用请求参数：

```json
// 可用模板变量
{{ params.id }}              // URL 路径参数
{{ headers.Authorization }}  // 请求头
{{ query.page }}             // 查询参数
{{ body.name }}              // 请求体字段（JSON）

// 模板示例
{
  "id": {{ params.id }},
  "request_from": "{{ headers.X-Forwarded-For }}",
  "page": {{ query.page | default(1) }}
}
```

### 6.4 条件匹配与延迟模拟

- **delay_ms**：模拟网络延迟，如 `100` 表示延迟 100ms
- **is_active**：启用/禁用 Mock 端点，禁用后请求不会匹配

### 6.5 访问 Mock 端点

Mock 匹配通过独立的 `/mock/` 路由暴露，无需认证（方便前后端直接调用）：

```bash
# 访问路径：/mock/{namespace_id}/{url_pattern}
curl http://<host>:5000/mock/1/api/users/123
# → {"id": 123, "name": "Mock User", "email": "mock@example.com"}

# 带查询参数
curl "http://<host>:5000/mock/1/api/users?page=1&size=10"

# POST 请求
curl -X POST http://<host>:5000/mock/1/api/orders \
  -H "Content-Type: application/json" \
  -d '{"item": "book", "qty": 2}'
```

---

## 7. 性能测试

内置性能测试引擎，支持并发压测和实时统计。

### 7.1 创建压测配置

```bash
curl -X POST http://<host>:5000/api/v1/perf/configs \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "namespace_id": 1,
    "testcase_id": 5,
    "name": "登录接口压测",
    "concurrency": 50,
    "total_requests": 1000,
    "duration_seconds": 60
  }'
```

| 参数 | 说明 |
|------|------|
| `concurrency` | 并发线程数 |
| `total_requests` | 总请求数 |
| `duration_seconds` | 最大持续时间（秒），先到先停 |

### 7.2 执行压测

```bash
# 触发压测（异步）
curl -X POST http://<host>:5000/api/v1/perf/run \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"config_id": 1}'
```

### 7.3 SSE 实时看板（计划中）

> **注意**：SSE 实时进度推送功能尚未实现，代码中已有基础设施（`stream_with_context`），后续版本将开放。目前可通过轮询结果接口获取进度。

### 7.4 结果分析

PerfRunner 使用流式算法实时计算以下指标：

| 指标 | 说明 |
|------|------|
| P50 | 50% 请求的响应时间低于此值 |
| P95 | 95% 请求的响应时间低于此值 |
| P99 | 99% 请求的响应时间低于此值 |
| RPS | 每秒请求数（Requests Per Second） |
| Error Rate | 错误率 |

```bash
# 查看压测结果列表
curl http://<host>:5000/api/v1/perf/results \
  -H "Authorization: Bearer <token>"

# 查看单个结果详情
curl http://<host>:5000/api/v1/perf/results/1 \
  -H "Authorization: Bearer <token>"
```

---

## 8. Webhook 集成

Webhook 用于在执行事件发生时自动通知外部系统（如 CI/CD、企业微信、钉钉等）。

### 8.1 支持的事件类型

| 事件 | 触发时机 |
|------|---------|
| `execution.started` | 执行开始 |
| `execution.completed` | 执行完成（全部通过） |
| `execution.failed` | 执行完成（存在失败） |

### 8.2 创建 Webhook

```bash
curl -X POST http://<host>:5000/api/v1/webhook \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "namespace_id": 1,
    "name": "CI 通知",
    "url": "https://ci.example.com/webhook/apitest",
    "events": ["execution.completed", "execution.failed"],
    "secret": "my-hmac-secret"
  }'
```

### 8.3 HMAC 签名

配置 `secret` 后，每次投递会在请求头中携带 HMAC-SHA256 签名：

```
X-Webhook-Signature: sha256=<hex_digest>
```

接收方可验证签名确保请求来源可信。

### 8.4 投递记录

```bash
# 发送测试投递
curl -X POST http://<host>:5000/api/v1/webhook/1/test \
  -H "Authorization: Bearer <token>"

# 查看投递历史
curl "http://<host>:5000/api/v1/webhook/1/deliveries?page=1" \
  -H "Authorization: Bearer <token>"

# 查看可用事件类型
curl http://<host>:5000/api/v1/webhook/events \
  -H "Authorization: Bearer <token>"
```

---

## 9. 定时任务

通过 Celery Beat 实现 cron 定时执行用例或测试套件。

### 9.1 创建定时任务

```bash
curl -X POST http://<host>:5000/api/v1/schedule \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "namespace_id": 1,
    "testcase_id": 5,
    "name": "每日冒烟测试",
    "cron_expr": "0 8 * * *"
  }'
```

**Cron 表达式说明**（5 字段格式）：

```
┌───────────── 分钟 (0-59)
│ ┌───────────── 小时 (0-23)
│ │ ┌───────────── 日 (1-31)
│ │ │ ┌───────────── 月 (1-12)
│ │ │ │ ┌───────────── 星期 (0-6, 0=周日)
│ │ │ │ │
* * * * *
```

常用示例：

| 表达式 | 说明 |
|--------|------|
| `0 8 * * *` | 每天早上 8:00 |
| `*/30 * * * *` | 每 30 分钟 |
| `0 9 * * 1-5` | 工作日 9:00 |
| `0 0 1 * *` | 每月 1 号 0:00 |

### 9.2 立即执行

无需等待定时触发，手动立即执行：

```bash
curl -X POST http://<host>:5000/api/v1/schedule/1/run-now \
  -H "Authorization: Bearer <token>"
```

### 9.3 管理定时任务

```bash
# 查看任务列表
curl "http://<host>:5000/api/v1/schedule?namespace_id=1" \
  -H "Authorization: Bearer <token>"

# 启用/禁用切换
curl -X POST http://<host>:5000/api/v1/schedule/1/toggle \
  -H "Authorization: Bearer <token>"

# 更新 cron 表达式
curl -X PUT http://<host>:5000/api/v1/schedule/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"cron_expr": "0 9 * * 1-5"}'

# 删除任务
curl -X DELETE http://<host>:5000/api/v1/schedule/1 \
  -H "Authorization: Bearer <token>"
```

---

## 10. 分布式执行节点

支持多 Worker 节点横向扩展执行能力，Master 智能调度任务分配。

### 10.1 架构说明

```
Master (API)  →  NodeManager (least-load 策略)  →  Worker Node 1
                                                  →  Worker Node 2
                                                  →  Worker Node N
```

- **自动注册**：Celery Worker 启动时通过 `worker_ready` 信号自动注册到 Master
- **心跳检测**：Worker 定期发送心跳，Master 自动标记离线节点
- **负载均衡**：采用 least-load 策略，将任务分配给负载最低的节点

### 10.2 节点管理

```bash
# 查看所有执行节点
curl http://<host>:5000/api/v1/execution/nodes \
  -H "Authorization: Bearer <token>"

# 查看单个节点详情
curl http://<host>:5000/api/v1/execution/nodes/1 \
  -H "Authorization: Bearer <token>"
```

前端「执行节点」页面可视化展示各节点状态、负载和执行次数。

---

## 11. 插件系统

基于 `entry_points` 的插件发现和生命周期管理，支持扩展断言类型和执行钩子。

### 11.1 插件安装与管理

```bash
# 查看已安装插件
curl http://<host>:5000/api/v1/plugins \
  -H "Authorization: Bearer <token>"

# 安装插件（通过 entry_point 路径）
curl -X POST http://<host>:5000/api/v1/plugins/install \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"entry_point": "my_package.plugins:MyPlugin"}'

# 启用插件
curl -X POST http://<host>:5000/api/v1/plugins/1/enable \
  -H "Authorization: Bearer <token>"

# 禁用插件
curl -X POST http://<host>:5000/api/v1/plugins/1/disable \
  -H "Authorization: Bearer <token>"
```

### 11.2 插件开发指南

继承 `BasePlugin` 抽象基类，实现钩子方法：

```python
from app.plugins.base import BasePlugin

class MyPlugin(BasePlugin):
    name = "my_plugin"
    version = "1.0.0"
    description = "自定义断言插件"

    def on_install(self):
        """插件安装时调用"""
        pass

    def on_enable(self):
        """插件启用时调用"""
        pass

    def on_disable(self):
        """插件禁用时调用"""
        pass

    def execute_hook(self, hook_name: str, context: dict) -> dict:
        """执行钩子，hook_name 为钩子名称，context 为上下文数据"""
        if hook_name == "custom_assertion":
            # 自定义断言逻辑
            return {"passed": True, "message": "Custom check passed"}
        return {}
```

安全机制：插件 `entry_point` 加载使用 `ThreadPoolExecutor` + 10 秒超时保护，防止恶意插件阻塞系统。

---

## 12. 权限管理

### 12.1 角色说明

系统采用 RBAC 权限模型，分为全局角色和命名空间级权限。

**全局角色**：

| 角色 | 权限 |
|------|------|
| `admin` | 系统管理员，拥有所有权限，可管理用户和插件 |
| `manager` | 项目经理，可审批用例评审 |
| `tester` | 测试人员，可创建和执行用例 |
| `viewer` | 只读用户，仅可查看 |

**命名空间级权限**：

| 角色 | 权限 |
|------|------|
| `owner` | 命名空间所有者，可授权/撤销他人权限 |
| `editor` | 编辑者，可创建/修改/删除用例和执行 |
| `viewer` | 查看者，只读访问 |

### 12.2 命名空间级权限管理

```bash
# 查看命名空间权限列表
curl http://<host>:5000/api/v1/permission/namespace/1/users \
  -H "Authorization: Bearer <token>"

# 授权（仅 owner 可操作）
curl -X POST http://<host>:5000/api/v1/permission/namespace/1/grant \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 3, "role": "editor"}'

# 撤销权限
curl -X POST http://<host>:5000/api/v1/permission/namespace/1/revoke \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 3}'
```

> 安全限制：不能撤销命名空间的最后一个 owner，需先将其他用户设为 owner。

---

## 13. 审计日志

系统自动记录所有管理操作的审计日志，支持查询、过滤和 CSV 导出。

### 13.1 日志查询

```bash
# 分页查询审计日志
curl "http://<host>:5000/api/v1/audit?page=1&per_page=20" \
  -H "Authorization: Bearer <token>"

# 按操作类型筛选
curl "http://<host>:5000/api/v1/audit?action=create&resource_type=testcase" \
  -H "Authorization: Bearer <token>"

# 按用户名模糊搜索
curl "http://<host>:5000/api/v1/audit?username=admin" \
  -H "Authorization: Bearer <token>"

# 按日期范围筛选
curl "http://<host>:5000/api/v1/audit?date_from=2026-06-01&date_to=2026-06-15" \
  -H "Authorization: Bearer <token>"

# 查看统计数据
curl "http://<host>:5000/api/v1/audit/stats?days=30" \
  -H "Authorization: Bearer <token>"
```

### 13.2 CSV 导出

```bash
# 导出审计日志为 CSV（支持同样的筛选参数）
curl "http://<host>:5000/api/v1/audit/export?date_from=2026-06-01" \
  -H "Authorization: Bearer <token>" -o audit_logs.csv
```

- 最大导出 10,000 条记录
- 使用 UTF-8 BOM 编码，Excel 可直接打开不乱码
- JSON 详情字段使用可读格式呈现

---

## 14. 多语言支持

### 14.1 前端语言切换

- 支持中文（zh-CN）和英文（en-US）
- 在页面右上角点击语言图标即可切换
- 语言偏好自动保存到 `localStorage`，下次登录保持
- Element Plus 组件库的日期选择器、分页等组件跟随自动切换

### 14.2 后端 i18n

后端 API 返回的错误消息会根据请求头 `Accept-Language` 自动切换语言：

```bash
# 请求中文错误消息
curl http://<host>:5000/api/v1/namespace/999 \
  -H "Authorization: Bearer <token>" \
  -H "Accept-Language: zh-CN"
# → {"error": {"message": "资源未找到"}}

# 请求英文错误消息
curl http://<host>:5000/api/v1/namespace/999 \
  -H "Authorization: Bearer <token>" \
  -H "Accept-Language: en-US"
# → {"error": {"message": "Resource not found"}}
```

---

## 附录：API 接口总览

> 完整交互式文档见 Swagger UI：`http://<host>:5000/api/docs`

**Base URL**: `http://<host>:5000` | **Content-Type**: `application/json` | **认证**: Bearer Token

| 模块 | 方法 | 路径 | 说明 |
|------|------|------|------|
| **认证** | POST | `/api/v1/auth/register` | 用户注册 |
| | POST | `/api/v1/auth/login` | 用户登录（返回 JWT） |
| | GET | `/api/v1/auth/me` | 当前用户信息 |
| **命名空间** | GET/POST | `/api/v1/namespace` | 列表（分页）/ 创建 |
| | GET/PUT/DELETE | `/api/v1/namespace/:id` | 详情 / 更新 / 删除 |
| | GET | `/api/v1/namespace/tree` | 层级树结构 |
| **用例** | GET/POST | `/api/v1/testcase` | 列表（分页+搜索+标签）/ 创建 |
| | GET/PUT/DELETE | `/api/v1/testcase/:id` | 详情 / 更新 / 删除 |
| | POST | `/api/v1/testcase/batch-delete` | 批量删除 |
| | GET | `/api/v1/testcase/export` | 导出 ZIP |
| | POST | `/api/v1/testcase/import` | 导入 YAML/ZIP |
| | GET | `/api/v1/testcase/:id/versions` | 版本列表 |
| | GET | `/api/v1/testcase/:id/versions/:vid` | 版本详情 |
| | GET | `/api/v1/testcase/:id/versions/:a/diff/:b` | 版本对比 |
| | POST | `/api/v1/testcase/:id/versions/:vid/rollback` | 回滚版本 |
| **评审** | POST | `/api/v1/testcase/:id/review/submit` | 提交评审 |
| | POST | `/api/v1/testcase/:id/review/approve` | 批准 |
| | POST | `/api/v1/testcase/:id/review/reject` | 驳回 |
| | POST | `/api/v1/testcase/:id/review/reset` | 重置为草稿 |
| | GET | `/api/v1/testcase/:id/reviews` | 评审记录 |
| **执行** | POST | `/api/v1/execution/run` | 触发执行 |
| | POST | `/api/v1/execution/batch-run` | 批量执行 |
| | GET | `/api/v1/execution/records` | 记录列表（分页） |
| | GET | `/api/v1/execution/records/:id` | 记录详情 |
| | GET | `/api/v1/execution/records/:id/status` | 状态轮询 |
| | POST | `/api/v1/execution/records/:id/cancel` | 取消执行 |
| | GET | `/api/v1/execution/records/:id/export` | 导出报告 HTML/PDF |
| | GET | `/api/v1/execution/records/:id/allure-export` | Allure 报告导出 |
| | GET | `/api/v1/execution/trends` | 趋势统计 |
| **测试套件** | GET/POST | `/api/v1/test-suite` | 列表 / 创建 |
| | GET/PUT/DELETE | `/api/v1/test-suite/:id` | 详情 / 更新 / 删除 |
| | POST | `/api/v1/test-suite/:id/run` | 执行套件 |
| **执行节点** | GET | `/api/v1/execution/nodes` | 节点列表 |
| | POST | `/api/v1/execution/nodes/register` | 节点注册 |
| | POST | `/api/v1/execution/nodes/heartbeat` | 心跳更新 |
| | GET | `/api/v1/execution/nodes/:id` | 节点详情 |
| | POST | `/api/v1/execution/nodes/cleanup` | 节点清理 |
| **Mock** | GET/POST | `/api/v1/mock` | Mock 端点列表 / 创建 |
| | GET/PUT/DELETE | `/api/v1/mock/:id` | 详情 / 更新 / 删除 |
| | GET | `/api/v1/mock/:id/hits` | 命中日志 |
| | ANY | `/mock/:namespace_id/:path` | Mock 请求匹配（无需认证） |
| **性能测试** | GET/POST | `/api/v1/perf/configs` | 配置列表 / 创建 |
| | GET | `/api/v1/perf/configs/:id` | 配置详情 |
| | POST | `/api/v1/perf/run` | 触发压测 |
| | GET | `/api/v1/perf/results` | 结果列表 |
| | GET/DELETE | `/api/v1/perf/results/:id` | 结果详情 / 删除 |
| **插件** | GET | `/api/v1/plugins` | 已安装插件 |
| | POST | `/api/v1/plugins/install` | 安装插件 |
| | POST | `/api/v1/plugins/:id/enable` | 启用 |
| | POST | `/api/v1/plugins/:id/disable` | 禁用 |
| **Webhook** | GET/POST | `/api/v1/webhook` | 列表 / 创建 |
| | GET/PUT/DELETE | `/api/v1/webhook/:id` | 详情 / 更新 / 删除 |
| | POST | `/api/v1/webhook/:id/test` | 发送测试 |
| | GET | `/api/v1/webhook/:id/deliveries` | 投递历史 |
| | GET | `/api/v1/webhook/events` | 可用事件类型 |
| **定时任务** | GET/POST | `/api/v1/schedule` | 列表 / 创建 |
| | GET/PUT/DELETE | `/api/v1/schedule/:id` | 详情 / 更新 / 删除 |
| | POST | `/api/v1/schedule/:id/toggle` | 启用/禁用切换 |
| | POST | `/api/v1/schedule/:id/run-now` | 立即执行 |
| **权限** | GET | `/api/v1/permission/namespace/:id/users` | 查看权限 |
| | POST | `/api/v1/permission/namespace/:id/grant` | 授权 |
| | POST | `/api/v1/permission/namespace/:id/revoke` | 撤销 |
| **审计** | GET | `/api/v1/audit` | 审计日志查询（分页） |
| | GET | `/api/v1/audit/export` | CSV 导出 |
| | GET | `/api/v1/audit/stats` | 统计数据 |

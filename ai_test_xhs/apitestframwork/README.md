# ApiTest — API 自动化测试平台

> **v1.0.0** | Flask 3.1.1 + Vue 3.5.31 + Docker Compose | 512 pytest 测试全部通过

基于 Flask + Vue 3 构建的企业级 API 自动化测试平台，支持 YAML 驱动用例、分层变量解析、10 种断言引擎、Celery 异步并行执行、API Mock 服务、性能测试、插件系统、用例评审、国际化等完整能力。

---

## 文档导航

| 文档 | 说明 |
|------|------|
| [功能使用指南](docs/user-guide.md) | 面向终端用户，详细说明每个功能的使用方法和 API 示例 |
| [CLI 命令行执行指南](docs/cli-execution-guide.md) | 无需平台的轻量命令行执行，支持 Allure 报告、CI/CD 集成 |
| [Docker 部署指南](docs/deployment.md) | 面向运维人员，从裸机到完整运行的部署教程 |
| [Swagger API 文档](http://localhost:5000/api/docs) | 在线交互式 API 文档（启动后访问） |

---

## 目录

- [核心功能](#核心功能)
- [CLI 命令行执行](#cli-命令行执行)
- [系统架构](#系统架构)
- [快速开始](#快速开始)
- [创建管理员用户](#创建管理员用户)
- [本地开发](#本地开发)
- [配置参考](#配置参考)
- [项目结构](#项目结构)
- [开发进展](#开发进展)

---

## 核心功能

| 模块 | 功能 | 描述 |
|------|------|------|
| **用例管理** | YAML 用例定义 | 单用例 + 数据驱动多用例，1MB 大小限制 |
| | 分层变量系统 | 命名空间 → 环境 → 用例三级变量覆盖 |
| | 用例版本管理 | 自动快照 + unified_diff 对比 + 一键回滚 |
| | 用例评审流程 | draft → pending_review → approved/rejected 状态机 |
| | 用例导入导出 | ZIP 批量上传/下载 + 3 种冲突策略（skip/rename/overwrite） |
| | 标签管理 | Tag 关联表 + 标签过滤搜索 |
| **执行引擎** | 可扩展断言引擎 | 10 种断言类型 + 插件式扩展 |
| | 并行执行 | ThreadPoolExecutor（MAX_PARALLEL=50）+ 结果顺序保障 |
| | 三层超时保护 | 请求 30s / 用例 60s / 套件 300s + YAML 可配置 |
| | Celery 异步执行 | Redis 队列 + 同步/异步双模式 + 状态轮询 + 取消 |
| | 分布式执行节点 | Master-Worker + least-load 调度 + 自动注册/心跳 |
| | 用例间变量传递 | ExtractSpec + 共享上下文 |
| | 性能测试 | PerfRunner + P50/P95/P99 统计 + SSE 实时看板 |
| **Mock 服务** | API Mock | MockEndpoint CRUD + URL `:param` 匹配 + Jinja2 模板渲染 + 延迟模拟 |
| **插件系统** | 插件发现与管理 | entry_points 发现 + BasePlugin 抽象基类 + 钩子机制 + 10s 超时保护 |
| **CI/CD 集成** | Webhook | HMAC-SHA256 签名 + 重试 + 投递记录 |
| | 定时执行 | Celery Beat + cron 表达式 + CRUD + 立即执行 |
| | 报告导出 | HTML / PDF / Allure 报告 |
| **CLI 命令行** | 零依赖执行 | 无 Flask/DB/Redis，仅需 5 个 Python 包 |
| | Allure 报告 | `--allure-results` + `--allure-html` 两种导出模式 |
| | CI/CD 集成 | 退出码 0/1 + `--no-color` + JSON/Allure 报告输出 |
| **协作与管理** | 用户认证/权限 | JWT + RBAC（admin/manager/tester/viewer + 命名空间级权限） |
| | 操作审计 | after_request 中间件 + 敏感字段脱敏 + CSV 导出 |
| | 趋势图表 | ECharts TrendChart + 聚合 API + 失败 Top5 |
| **基础设施** | 多语言支持 | vue-i18n + Element Plus locale 联动 + 后端 i18n |
| | 数据库 | SQLite（开发）/ MySQL 8.0（生产）+ Flask-Migrate |
| | 容器部署 | Docker Compose 一键编排（7 个服务） |
| | 全文搜索 | MySQL FULLTEXT + SQLite ILIKE 自适应 |
| | 层级命名空间 | parent_id 自引用 + /tree API |
| | 测试套件 | 用例集合管理 + 一键执行 + 定时调度 |

> 详细功能说明和操作示例请查看 [功能使用指南](docs/user-guide.md)。

---

## CLI 命令行执行

无需启动 Flask 服务、数据库、Redis，通过命令行直接执行 YAML API 测试用例。仅需安装 5 个 Python 包。

```bash
cd api_framework/backend

# 安装 CLI 最小依赖
pip install -r requirements-cli.txt

# 执行单个用例
python cli.py run tests/login.yaml

# 执行目录下所有用例 + 环境变量 + Allure 报告
python cli.py run tests/ --env .env.staging --allure-results ./allure-results

# 直接生成 Allure 单文件 HTML（需安装 allure CLI + JRE）
python cli.py run tests/ --allure-html report.html

# CI/CD 场景：JSON + Allure 同时输出
python cli.py run tests/ --output report.json --allure-results ./allure-results --no-color
```

| 参数 | 说明 |
|------|------|
| `--env FILE` | `.env` 环境变量文件 |
| `--var KEY=VALUE` | 变量覆盖（可多次使用，最高优先级） |
| `--output FILE` | JSON 报告输出 |
| `--allure-results DIR` | Allure results 目录（本地 `allure generate` 查看） |
| `--allure-html FILE` | 自包含 Allure HTML 报告 |
| `--parallel N` | 并行工作线程数 |
| `--verbose` | 显示完整请求/响应详情 |
| `--no-color` | 禁用彩色输出（CI 友好） |

> 完整参数说明、YAML 格式、CI/CD 集成示例请查看 [CLI 命令行执行指南](docs/cli-execution-guide.md)。

---

## 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                  Frontend (Vue 3 SPA)                     │
│  Element Plus · Pinia · Vue Router · Axios · vue-i18n    │
│  CodeMirror YAML · ECharts · 路由守卫 · JWT Token        │
└───────────────────────────┬─────────────────────────────┘
                            │ HTTP REST API
┌───────────────────────────▼─────────────────────────────┐
│                    Flask Application                      │
│  ┌─────────────────────────────────────────────────┐     │
│  │              API Layer (Blueprints)                │     │
│  │  /api/v1/auth       /api/v1/namespace             │     │
│  │  /api/v1/testcase   /api/v1/execution             │     │
│  │  /api/v1/permission /api/v1/webhook               │     │
│  │  /api/v1/audit      /api/v1/schedule              │     │
│  │  /api/v1/mock       /api/v1/execution-node        │     │
│  │  /api/v1/perf-test  /api/v1/plugins               │     │
│  │  /api/v1/test-suite /api/docs (Swagger)           │     │
│  │  JWT @login_required · @role_required              │     │
│  └──────────────────┬────────────────────────────────┘     │
│  ┌──────────────────▼────────────────────────────────┐     │
│  │              Core Engine                            │     │
│  │  Namespace Manager · Yaml Parser · Assertion Engine │     │
│  │  Case Runner (Serial / Parallel)                    │     │
│  │  Mock Manager · Version Manager · Perf Runner       │     │
│  │  Node Manager · Plugin Manager · Review Manager     │     │
│  │  Webhook Manager · Report Exporter · IO Manager     │     │
│  └─────────────────────────────────────────────────┘     │
│  ┌─────────────────────────────────────────────────┐     │
│  │              Data Layer (SQLAlchemy)              │     │
│  │  15+ 个模型 · Flask-Migrate · MySQL/SQLite 双支持 │     │
│  └─────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────┘
        │                    │
   ┌────▼────┐       ┌──────▼──────┐
   │ MySQL   │       │ Redis       │
   │ 8.0+    │       │ (Celery)    │
   └─────────┘       └──────┬──────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
       ┌──────▼──────┐ ┌────▼────┐ ┌───────▼──────┐
       │ Celery      │ │ Celery  │ │ Celery Beat  │
       │ Worker      │ │ Worker  │ │ (定时调度)    │
       │ (通用队列)  │ │ (性能)  │ │              │
       └─────────────┘ └─────────┘ └──────────────┘
```

---

## 快速开始

### 环境要求

- Python >= 3.12
- Node.js >= 18（前端开发）
- MySQL 8.0+（生产环境必须，开发可用 SQLite）
- Redis 7+（Celery 异步队列）

### Docker Compose 部署（推荐）

```bash
# 1. 克隆项目
git clone <repo-url> apitest && cd apitest

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env，务必修改 SECRET_KEY 和数据库密码

# 3. 一键启动（MySQL + Redis + Backend + Celery Worker × 2 + Celery Beat + Frontend）
docker compose up -d --build

# 4. 访问
#    前端:        http://localhost
#    后端 API:    http://localhost:5000
#    Swagger:     http://localhost:5000/api/docs
#    健康检查:    http://localhost:5000/health
```

Docker Compose 编排的 7 个服务：

| 服务 | 容器名 | 说明 |
|------|--------|------|
| `mysql` | apitest-mysql | MySQL 8.0 数据库 |
| `redis` | apitest-redis | Redis 7 消息代理 |
| `backend` | apitest-backend | Flask API（Gunicorn 多 Worker） |
| `celery-worker` | apitest-celery-worker | 通用 Celery Worker（执行/Mock 等） |
| `celery-worker-perf` | apitest-celery-worker-perf | 性能测试专用 Celery Worker |
| `celery-beat` | apitest-celery-beat | Celery Beat 定时调度 |
| `frontend` | apitest-frontend | Vue 3 SPA（Nginx 托管 + API 反向代理） |

> 完整部署教程（含 HTTPS、备份、升级、排查）请查看 [Docker 部署指南](docs/deployment.md)。

---

## 创建管理员用户

项目不自带预置管理员账户，首次部署后需手动创建：

```bash
# Docker 环境（推荐）
docker exec -it apitest-backend python scripts/create_admin.py \
  --username admin --email admin@example.com --password admin123 --env prod

# 本地开发环境
python scripts/create_admin.py \
  --username admin --email admin@example.com --password admin123
```

创建后访问前端页面输入用户名密码即可登录。

---

## 本地开发

### 后端

```bash
cd api_framework/backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器（默认 SQLite）
python run.py
# 监听 http://0.0.0.0:5000

# 启动 Redis（异步执行/定时任务/性能测试需要）
docker run -d --name apitest-redis -p 127.0.0.1:6379:6379 redis:7-alpine

# 启动 Celery Worker + Beat
celery -A app.tasks:celery_app worker --loglevel=info --concurrency=4
celery -A app.tasks:celery_app beat --loglevel=info
```

### 前端

```bash
cd api_framework/frontend

# 安装依赖
npm install

# 启动开发服务器（自动代理 /api → localhost:5000）
npm run dev
# 监听 http://localhost:5173
```

### 运行测试

```bash
cd api_framework/backend

# 运行全部测试
python -m pytest tests/ -v

# 带覆盖率报告
python -m pytest tests/ --cov=app --cov-report=term-missing
```

---

## 配置参考

### 环境变量（.env）

```ini
# --- 运行环境 ---
FLASK_ENV=prod                          # dev / test / prod
SECRET_KEY=change-me-in-production      # JWT 签名密钥（必须修改）
LOG_LEVEL=INFO                          # 日志级别

# --- 数据库 ---
DATABASE_URI=mysql+pymysql://user:pass@host:3306/apitest?charset=utf8mb4
MYSQL_ROOT_PASSWORD=apitest_root_2026   # Docker Compose 使用
MYSQL_DATABASE=apitest
MYSQL_USER=apitest
MYSQL_PASSWORD=apitest_pass_2026
MYSQL_PORT=3306

# --- 后端 ---
BACKEND_PORT=5000
HTTP_TIMEOUT=30                         # 默认 HTTP 超时（秒）
HTTP_MAX_RETRIES=3

# --- Gunicorn ---
GUNICORN_WORKERS=4
GUNICORN_BIND=0.0.0.0:5000
GUNICORN_TIMEOUT=120

# --- Celery / Redis ---
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
CELERY_WORKER_CONCURRENCY=4             # 通用 Worker 并发数
CELERY_PERF_CONCURRENCY=2               # 性能测试 Worker 并发数
CELERY_TASK_SOFT_TIME_LIMIT=300         # 任务软超时（秒）
CELERY_TASK_TIME_LIMIT=360              # 任务硬超时（秒）
REDIS_PORT=6379

# --- CORS ---
CORS_ORIGINS=http://localhost:5173,http://localhost:80

# --- 前端 ---
FRONTEND_PORT=80
```

---

## 项目结构

```
apitest/
├── api_framework/
│   ├── backend/
│   │   ├── app/
│   │   │   ├── __init__.py              # Flask 应用工厂
│   │   │   ├── api/v1/                  # API 路由层
│   │   │   │   ├── auth.py              # 用户认证
│   │   │   │   ├── namespace.py         # 命名空间（层级+分页）
│   │   │   │   ├── testcase.py          # 用例管理 + 评审 + 版本
│   │   │   │   ├── execution.py         # 执行 + 报告导出 + 趋势
│   │   │   │   ├── execution_node.py    # 分布式节点
│   │   │   │   ├── mock.py              # Mock 服务
│   │   │   │   ├── perf_test.py         # 性能测试
│   │   │   │   ├── plugins.py           # 插件管理
│   │   │   │   ├── permission.py        # 权限管理
│   │   │   │   ├── webhook.py           # Webhook
│   │   │   │   ├── audit.py             # 审计日志
│   │   │   │   ├── schedule.py          # 定时任务
│   │   │   │   ├── test_suite.py        # 测试套件
│   │   │   │   └── docs.py              # Swagger UI
│   │   │   ├── cli/                     # CLI 轻量执行引擎（LocalNamespace + Runner）
│   │   │   ├── config/                  # 配置模块
│   │   │   ├── core/                    # 核心业务引擎
│   │   │   │   ├── executor/            # 执行引擎（解析/上下文/运行/断言）
│   │   │   │   ├── execution/           # 分布式节点管理
│   │   │   │   ├── mock/                # Mock 业务逻辑
│   │   │   │   ├── namespace/           # 命名空间管理器
│   │   │   │   ├── perf/                # 性能测试引擎
│   │   │   │   ├── report/              # HTML/PDF/Allure 报告导出
│   │   │   │   ├── testcase/            # 用例管理 + 导入导出 + 版本
│   │   │   │   ├── webhook/             # Webhook CRUD + 事件分发
│   │   │   │   ├── plugin_manager.py    # 插件管理
│   │   │   │   ├── review_manager.py    # 评审管理
│   │   │   │   └── exceptions.py        # 自定义异常
│   │   │   ├── plugins/                 # 插件目录（BasePlugin + 内置插件）
│   │   │   ├── models/                  # 数据模型（15+ 模型类）
│   │   │   ├── utils/                   # 工具模块（HTTP/加密/认证/校验/i18n）
│   │   │   └── tasks/                   # Celery 任务 + 节点自注册
│   │   ├── cli.py                       # CLI 入口脚本（argparse + Allure 导出）
│   │   ├── requirements-cli.txt        # CLI 最小依赖（5 个包）
│   │   ├── migrations/versions/         # Alembic 数据库迁移
│   │   ├── tests/                       # pytest 测试（512 测试，26+ 文件）
│   │   ├── gunicorn.conf.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── run.py
│   └── frontend/
│       ├── src/
│       │   ├── api/                     # Axios 服务层
│       │   ├── components/              # 通用组件
│       │   ├── composables/             # usePagination / usePolling
│       │   ├── locales/                 # zh-CN.js / en-US.js
│       │   ├── plugins/                 # i18n.js
│       │   ├── router/                  # 路由 + 守卫
│       │   ├── stores/                  # Pinia Store
│       │   ├── views/                   # 页面组件
│       │   ├── App.vue
│       │   └── main.js
│       ├── Dockerfile
│       ├── nginx.conf
│       ├── package.json
│       └── vite.config.js
├── docker-compose.yml                   # 7 服务编排
├── .env.example                         # 环境变量模板
├── scripts/                             # 初始化脚本
├── docs/
│   ├── user-guide.md                    # 功能使用指南
│   ├── cli-execution-guide.md           # CLI 命令行执行指南
│   ├── deployment.md                    # Docker 部署指南
│   ├── architecture-review.md           # 架构评审报告
│   ├── openapi.yaml                     # OpenAPI 3.0
│   ├── phase1-development-plan.md
│   ├── phase2-development-plan.md
│   ├── phase3-development-plan.md
│   ├── phase4-development-plan.md
│   └── phase5-development-plan.md
└── README.md
```

---

## License

This project is licensed under the **ApiTest Commercial License v1.0**.
See the [LICENSE](LICENSE) file for the full license text.

- **Community Edition**: Free to use with limited features.
- **Professional Edition**: Commercial license required.
- **Enterprise Edition**: Commercial license with full features and priority support.

For licensing inquiries, contact: license@apitest.io

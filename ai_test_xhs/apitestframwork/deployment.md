# ApiTest Docker 部署指南

> 本文档面向运维人员，从裸 Linux 服务器到完整运行的 ApiTest 平台部署全流程。

---

## 目录

- [1. 环境要求](#1-环境要求)
- [2. 安装 Docker 和 Docker Compose](#2-安装-docker-和-docker-compose)
- [3. 获取项目](#3-获取项目)
- [4. 配置环境变量](#4-配置环境变量)
- [5. 构建与启动](#5-构建与启动)
- [6. 创建管理员用户](#6-创建管理员用户)
- [7. 配置 HTTPS（生产环境）](#7-配置-https生产环境)
- [8. 数据备份与恢复](#8-数据备份与恢复)
- [9. 升级步骤](#9-升级步骤)
- [10. 内网离线部署](#10-内网离线部署)
- [11. 常见问题排查](#11-常见问题排查)
- [附录：完整 .env 配置参考](#附录完整-env-配置参考)

---

## 1. 环境要求

### 硬件最低配置

| 资源 | 最低要求 | 推荐配置 |
|------|---------|---------|
| CPU | 2 核 | 4 核 |
| 内存 | 2 GB | 4 GB |
| 磁盘 | 10 GB | 20 GB（含数据库空间） |
| 网络 | 可访问外网（拉取 Docker 镜像）或使用离线镜像导入 | 独立公网 IP |

### 软件要求

| 软件 | 版本 | 说明 |
|------|------|------|
| 操作系统 | CentOS 7+ / Ubuntu 20.04+ / Debian 11+ | 推荐 Ubuntu 22.04 LTS |
| Docker | 20.10+ | 容器运行时 |
| Docker Compose | v2.0+（`docker compose` 命令） | 服务编排 |
| Git | 任意版本 | 拉取项目代码（内网部署可手动拷贝） |

> 以下所有命令均以 root 用户执行。如使用普通用户，请在命令前加 `sudo`。

---

## 2. 安装 Docker 和 Docker Compose

### CentOS / RHEL / Rocky Linux

```bash
# 安装依赖
yum install -y yum-utils device-mapper-persistent-data lvm2

# 添加 Docker 仓库（阿里云镜像源，国内推荐）
yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

# 安装 Docker
yum install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 启动并设为开机自启
systemctl start docker
systemctl enable docker

# 配置 Docker 镜像加速（可选，加速拉取）
mkdir -p /etc/docker
cat > /etc/docker/daemon.json << 'EOF'
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com",
    "https://registry.docker-cn.com"
  ]
}
EOF
systemctl daemon-reload
systemctl restart docker
```

### Ubuntu / Debian

```bash
# 更新包索引并安装依赖
apt-get update
apt-get install -y ca-certificates curl gnupg lsb-release

# 添加 Docker 官方 GPG 密钥
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

# 添加 Docker 仓库
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装 Docker
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 启动并设为开机自启
systemctl start docker
systemctl enable docker
```

### 验证安装

```bash
# 验证 Docker
docker --version
# 期望输出: Docker version 24.x.x 或更高

# 验证 Docker Compose（v2 插件方式）
docker compose version
# 期望输出: Docker Compose version v2.x.x 或更高

# 验证 Docker 服务运行正常
docker run --rm hello-world
# 期望输出: Hello from Docker!
```

---

## 3. 获取项目

```bash
# 克隆项目代码
git clone <repo-url> /opt/apitest
cd /opt/apitest

# 项目目录结构
# apitest/
# ├── api_framework/
# │   ├── backend/          # Flask 后端
# │   │   ├── Dockerfile
# │   │   └── requirements.txt
# │   └── frontend/         # Vue 前端
# │       ├── Dockerfile
# │       └── package.json
# ├── docker-compose.yml    # 服务编排文件
# ├── .env.example          # 环境变量模板
# ├── scripts/              # 初始化脚本
# └── docs/                 # 文档
```

---

## 4. 配置环境变量

### 复制模板

```bash
cd /opt/apitest
cp .env.example .env
```

### 必须修改的配置项

以下配置项**务必修改**，使用默认值存在安全风险：

```bash
vi .env   # 或使用 nano .env
```

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `SECRET_KEY` | JWT 签名密钥，**必须修改** | `SECRET_KEY=your-random-secret-key-32-chars` |
| `MYSQL_ROOT_PASSWORD` | MySQL root 密码 | `MYSQL_ROOT_PASSWORD=StrongR00tP@ss!` |
| `MYSQL_PASSWORD` | 应用数据库密码 | `MYSQL_PASSWORD=StrongAppP@ss!` |

生成随机密钥：

```bash
# 生成 32 位随机字符串作为 SECRET_KEY
openssl rand -hex 32
# 输出示例: a3f5b7c8d9e1f2a4b6c8d0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8
```

### 可选配置项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `BACKEND_PORT` | `5000` | 后端 API 端口 |
| `FRONTEND_PORT` | `80` | 前端 Web 端口 |
| `MYSQL_PORT` | `3306` | MySQL 端口（仅 127.0.0.1） |
| `REDIS_PORT` | `6379` | Redis 端口（仅 127.0.0.1） |
| `CELERY_WORKER_CONCURRENCY` | `4` | 通用 Worker 并发数 |
| `CELERY_PERF_CONCURRENCY` | `2` | 性能测试 Worker 并发数 |
| `LOG_LEVEL` | `INFO` | 日志级别（DEBUG/INFO/WARNING/ERROR） |
| `HTTP_TIMEOUT` | `30` | 默认 HTTP 请求超时（秒） |
| `CORS_ORIGINS` | `http://localhost:5173,http://localhost:80` | 允许的 CORS 来源 |

### CORS 配置

生产环境中，`CORS_ORIGINS` 应仅配置实际访问的域名：

```bash
# 如果使用自定义域名
CORS_ORIGINS=https://apitest.yourcompany.com,http://apitest.yourcompany.com
```

---

## 5. 构建与启动

### 一键启动

```bash
cd /opt/apitest

# 构建镜像并启动所有服务（后台运行）
docker compose up -d --build
```

此命令会构建并启动以下 7 个服务：

| 服务 | 容器名 | 说明 |
|------|--------|------|
| `mysql` | apitest-mysql | MySQL 8.0 数据库 |
| `redis` | apitest-redis | Redis 7 消息代理 |
| `backend` | apitest-backend | Flask API（Gunicorn 多 Worker） |
| `celery-worker` | apitest-celery-worker | 通用 Celery Worker |
| `celery-worker-perf` | apitest-celery-worker-perf | 性能测试专用 Worker |
| `celery-beat` | apitest-celery-beat | Celery Beat 定时调度 |
| `frontend` | apitest-frontend | Vue SPA（Nginx 托管） |

### 验证服务状态

```bash
# 查看所有容器状态（应全部为 Up）
docker compose ps

# 期望输出:
# NAME                     STATUS
# apitest-mysql            Up (healthy)
# apitest-redis            Up (healthy)
# apitest-backend          Up (healthy)
# apitest-celery-worker    Up
# apitest-celery-worker-perf Up
# apitest-celery-beat      Up
# apitest-frontend         Up (healthy)

# 等待所有服务启动（MySQL 初始化约需 30 秒）
# 健康检查通过后继续下一步
```

### 验证接口可用

```bash
# 后端健康检查
curl http://localhost:5000/health
# 期望输出: {"status":"ok"} 或类似

# 前端访问
curl -s -o /dev/null -w "%{http_code}" http://localhost
# 期望输出: 200
```

### 访问地址

| 服务 | 地址 |
|------|------|
| 前端界面 | `http://<服务器IP>:80` |
| 后端 API | `http://<服务器IP>:5000` |
| Swagger 文档 | `http://<服务器IP>:5000/api/docs` |
| 健康检查 | `http://<服务器IP>:5000/health` |

### 查看日志

```bash
# 查看所有服务日志（实时）
docker compose logs -f

# 查看指定服务日志
docker compose logs -f backend
docker compose logs -f celery-worker

# 查看最近 100 行
docker compose logs --tail=100 backend
```

### 常用运维命令

```bash
# 停止所有服务
docker compose down

# 停止并清除数据卷（会删除数据库和 Redis 数据！）
docker compose down -v

# 重启单个服务
docker compose restart backend

# 仅重建后端（代码更新后）
docker compose up -d --build backend
```

---

## 6. 创建管理员用户

项目不自带预置管理员账户，首次部署后必须手动创建。

### 方式一：在 Docker 容器内执行（推荐）

```bash
docker exec -it apitest-backend python scripts/create_admin.py \
  --username admin \
  --email admin@example.com \
  --password "YourStrongPassword123!" \
  --env prod
```

参数说明：

| 参数 | 说明 |
|------|------|
| `--username` | 管理员用户名（用于登录） |
| `--email` | 管理员邮箱（也可用于登录） |
| `--password` | 密码（建议 8 位以上，含大小写+特殊字符） |
| `--env` | **Docker 环境必须使用 `prod`** |

> **重要**：Docker 环境下必须使用 `--env prod`，否则会写入本地 SQLite 而非 MySQL 数据库。

### 验证登录

```bash
# 使用 API 验证
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"YourStrongPassword123!"}'

# 成功响应:
# {"token":"eyJ...","user":{"id":1,"username":"admin","role":"admin"}}
```

登录成功后，访问前端页面 `http://<服务器IP>` 输入用户名密码即可进入平台。

---

## 7. 配置 HTTPS（生产环境）

生产环境强烈建议配置 HTTPS，保护 JWT Token 和用户数据安全。

### 方式一：宿主机 Nginx 反向代理（推荐）

在 Docker 前面加一层宿主机 Nginx 做 SSL 终结：

```bash
# 安装 Nginx
apt-get install -y nginx   # Ubuntu
# yum install -y nginx      # CentOS

# 安装 certbot（Let's Encrypt）
apt-get install -y certbot python3-certbot-nginx
```

**Nginx 配置**（`/etc/nginx/conf.d/apitest.conf`）：

```nginx
server {
    listen 80;
    server_name apitest.yourdomain.com;

    # Let's Encrypt 验证
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    # HTTP 重定向到 HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name apitest.yourdomain.com;

    # SSL 证书（certbot 生成后自动填充路径）
    ssl_certificate /etc/letsencrypt/live/apitest.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/apitest.yourdomain.com/privkey.pem;

    # SSL 安全配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # 前端
    location / {
        proxy_pass http://127.0.0.1:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 后端 API
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
    }

    # 健康检查
    location /health {
        proxy_pass http://127.0.0.1:5000;
    }
}
```

**申请 SSL 证书**：

```bash
# 先确保 80 端口可访问且域名已解析到服务器
mkdir -p /var/www/certbot
certbot certonly --nginx -d apitest.yourdomain.com

# 证书自动续期（certbot 会自动添加 cron 任务）
certbot renew --dry-run

# 重启 Nginx
systemctl restart nginx
```

**更新 .env 的 CORS 配置**：

```bash
CORS_ORIGINS=https://apitest.yourdomain.com
```

重启后端使配置生效：

```bash
docker compose restart backend
```

### 方式二：修改 docker-compose.yml 添加 Nginx SSL

如果不想使用宿主机 Nginx，可修改 `frontend` 服务的 Dockerfile 和 nginx.conf 支持 SSL，但方式一更简单推荐。

---

## 8. 数据备份与恢复

### MySQL 数据库备份

```bash
# 手动备份（推荐定期执行，加入 crontab）
docker exec apitest-mysql mysqldump -u root -p"apitest_root_2026" apitest \
  > /backup/apitest_db_$(date +%Y%m%d_%H%M%S).sql

# 设置每日凌晨 3 点自动备份
cat > /etc/cron.d/apitest-backup << 'EOF'
0 3 * * * root docker exec apitest-mysql mysqldump -u root -p"apitest_root_2026" apitest > /backup/apitest_db_$(date +\%Y\%m\%d).sql 2>&1
EOF

# 创建备份目录
mkdir -p /backup
```

### Redis 数据备份

```bash
# 备份 Redis RDB 文件
docker exec apitest-redis redis-cli -a "apitest_redis_2026" BGSAVE
docker cp apitest-redis:/data/dump.rdb /backup/redis_dump_$(date +%Y%m%d).rdb
```

### 恢复步骤

```bash
# 恢复 MySQL
cat /backup/apitest_db_20260615.sql | docker exec -i apitest-mysql mysql -u root -p"apitest_root_2026" apitest

# 恢复 Redis
docker stop apitest-redis
docker cp /backup/redis_dump_20260615.rdb apitest-redis:/data/dump.rdb
docker start apitest-redis
```

---

## 9. 升级步骤

```bash
cd /opt/apitest

# 1. 拉取最新代码
git pull origin main

# 2. 备份数据库（升级前必须）
docker exec apitest-mysql mysqldump -u root -p"apitest_root_2026" apitest \
  > /backup/apitest_db_before_upgrade_$(date +%Y%m%d).sql

# 3. 重建并重启服务
docker compose up -d --build

# 4. 执行数据库迁移（如有）
docker exec -it apitest-backend flask db upgrade

# 5. 验证服务状态
docker compose ps
curl http://localhost:5000/health

# 6. 如需回滚
# docker compose down
# git checkout <previous-tag-or-commit>
# cat /backup/apitest_db_before_upgrade_xxx.sql | docker exec -i apitest-mysql mysql -u root -p"apitest_root_2026" apitest
# docker compose up -d --build
```

---

## 10. 内网离线部署

> 适用于无公网访问的企业内网环境。核心思路：**在有网机器上构建镜像，导出后搬运到内网机器加载运行。**

### 10.1 一键导出部署包（有网机器执行）

项目已内置导出脚本 `scripts/export-offline-package.sh`，在项目根目录执行即可：

```bash
cd /opt/apitest   # 项目根目录

# 一键导出：自动完成 构建镜像 → 导出镜像 → 打包部署文件
bash scripts/export-offline-package.sh
```

脚本会自动完成以下操作：

1. 构建后端 + 前端应用镜像
2. 拉取 MySQL 和 Redis 基础镜像
3. 将所有镜像导出为 tar 文件
4. 生成已替换为 `image` 模式的离线 docker-compose.yml
5. 打包 .env 模板和初始化脚本

运行后生成的 `apitest-offline/` 目录结构：

```
apitest-offline/
├── apitest-backend.tar          # 后端镜像（含 Flask + Allure CLI + JRE）
├── apitest-frontend.tar         # 前端镜像（含 Vue 构建产物 + Nginx）
├── mysql-8.0.tar                # MySQL 镜像
├── redis-7-alpine.tar           # Redis 镜像
├── docker-compose.yml           # 已替换为 image 模式，可直接使用
├── .env                         # 环境变量模板（需修改密码）
└── scripts/
    └── mysql-init/
        └── 01-init.sql
```

### 10.2 一键导入部署（内网机器执行）

**前提**：内网机器已安装 Docker 20.10+ 和 Docker Compose v2.0+。

将 `apitest-offline/` 目录拷贝到内网机器后，执行导入脚本：

```bash
# 一键导入：自动加载镜像 + 准备部署目录
bash import-offline-deploy.sh /path/to/apitest-offline
```

导入完成后，按提示执行：

```bash
cd /opt/apitest
vi .env                    # 必须修改: SECRET_KEY / 数据库密码
docker compose up -d       # 启动所有服务

# 创建管理员
docker exec -it apitest-backend python scripts/create_admin.py \
  --username admin --email admin@example.com \
  --password "YourStrongPassword123!" --env prod
```

> **说明**：`docker-compose.yml` 已在导出阶段自动替换为 `image` 模式，内网机器无需手动修改，直接 `docker compose up -d` 即可启动。

### 10.3 内网升级流程

当项目有新版本时，在**有网机器**上重新执行 `bash scripts/export-offline-package.sh`，将新生成的 `apitest-offline/` 拷贝到内网后执行：

```bash
cd /opt/apitest

# 1. 备份数据库
docker exec apitest-mysql mysqldump -u root -p"apitest_root_2026" apitest \
  > /backup/apitest_db_$(date +%Y%m%d).sql

# 2. 加载新镜像
docker load -i apitest-backend.tar
docker load -i apitest-frontend.tar

# 3. 重启服务
docker compose up -d

# 4. 执行数据库迁移（如有）
docker exec -it apitest-backend flask db upgrade
```

---

## 11. 常见问题排查

### 服务启动失败

```bash
# 查看具体错误日志
docker compose logs backend
docker compose logs mysql

# 常见原因：端口被占用
ss -tlnp | grep -E ':(80|5000|3306|6379)'
# 如果端口被占用，修改 .env 中对应的端口配置
```

### 数据库连接问题

```bash
# 检查 MySQL 是否就绪
docker exec apitest-mysql mysqladmin ping -h localhost -u root -p"apitest_root_2026"

# 检查后端能否连接 MySQL
docker exec apitest-backend python -c "
from sqlalchemy import create_engine, text
e = create_engine('mysql+pymysql://apitest:apitest_pass_2026@mysql:3306/apitest?charset=utf8mb4')
with e.connect() as c:
    print(c.execute(text('SELECT 1')).scalar())
"

# 检查数据库迁移状态
docker exec apitest-backend flask db current
```

### Redis 连接问题

```bash
# 检查 Redis 是否运行
docker exec apitest-redis redis-cli -a "apitest_redis_2026" ping
# 期望输出: PONG

# 检查 Celery Worker 日志
docker compose logs celery-worker

# 如果 Worker 报 Redis 连接错误，确认 .env 中 CELERY_BROKER_URL 格式正确
# Docker 内部应使用: redis://:password@redis:6379/0
```

### 端口冲突

```bash
# 查看端口占用
ss -tlnp | grep :80
ss -tlnp | grep :5000

# 修改 .env 中的端口
vi .env
# FRONTEND_PORT=8080    # 改为其他未占用端口
# BACKEND_PORT=5001

# 重启生效
docker compose down
docker compose up -d
```

### 前端页面空白或 404

```bash
# 检查前端容器是否正常
docker compose logs frontend

# 如果是路由问题，确认 nginx.conf 配置了 try_files
docker exec apitest-frontend cat /etc/nginx/conf.d/default.conf | grep try_files

# 重建前端
docker compose up -d --build frontend
```

### 日志查看方法

```bash
# 实时查看所有服务日志
docker compose logs -f

# 查看单个服务最近日志
docker compose logs --tail=200 backend

# 进入容器查看应用日志文件
docker exec apitest-backend cat /app/logs/error.log
docker exec apitest-backend cat /app/logs/app.log
```

---

## 附录：完整 .env 配置参考

```ini
# =============================================================================
# ApiTest - 环境变量配置
# =============================================================================

# --- 运行环境 ---
FLASK_ENV=prod
SECRET_KEY=your-random-secret-key-here-change-me    # 必须修改！
LOG_LEVEL=INFO

# --- 数据库 ---
MYSQL_ROOT_PASSWORD=StrongR00tP@ss                   # 必须修改！
MYSQL_DATABASE=apitest
MYSQL_USER=apitest
MYSQL_PASSWORD=StrongAppP@ss                         # 必须修改！
MYSQL_PORT=3306

# --- 后端配置 ---
BACKEND_PORT=5000
HTTP_TIMEOUT=30
HTTP_MAX_RETRIES=3

# --- Gunicorn 配置 ---
# GUNICORN_WORKERS=4
# GUNICORN_BIND=0.0.0.0:5000
# GUNICORN_TIMEOUT=120

# --- 前端配置 ---
FRONTEND_PORT=80

# --- Celery / Redis 配置 ---
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
CELERY_WORKER_CONCURRENCY=4
CELERY_PERF_CONCURRENCY=2
CELERY_TASK_SOFT_TIME_LIMIT=300
CELERY_TASK_TIME_LIMIT=360
REDIS_PORT=6379

# --- CORS 配置 ---
CORS_ORIGINS=https://apitest.yourdomain.com
```

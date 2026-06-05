# Cosbench 对象存储性能测试完全指南：从安装到分布式压测

> **摘要**：Cosbench 是 Intel 开源的云对象存储基准测试工具，支持 S3/Swift 等协议。本文从环境准备、安装部署、工作原理、XML 配置详解、六大典型测试场景、多节点分布式压测，到常见问题排查，提供一站式 Cosbench 使用教程。

---

## 一、环境准备

### 1.1 基础依赖

- **Java 版本**：必须使用 **Java 8**（Java 11+ 存在兼容性问题，高并发场景会崩溃）
- **网络要求**：所有节点之间网络互通，开放 **19088**（Controller）和 **18088**（Driver）端口

### 1.2 硬件建议

| 节点类型 | 最低配置 | 推荐配置 |
| -------- | -------- | -------- |
| Controller 节点 | 2 核 4G | 4 核 8G |
| Driver 节点 | 8 核 16G | 16 核 32G + 万兆网卡（大文件测试必须） |

---

## 二、安装部署

### 2.1 一键安装脚本（所有节点执行）

```bash
# 1. 关闭防火墙和 SELinux（生产环境可仅开放指定端口）
systemctl stop firewalld
systemctl disable firewalld
setenforce 0
sed -i 's/^SELINUX=enforcing$/SELINUX=disabled/' /etc/selinux/config

# 2. 安装依赖
yum install -y java-1.8.0-openjdk nmap-ncat curl wget unzip   # CentOS/RHEL
# apt-get install -y openjdk-8-jdk nmap curl wget unzip        # Ubuntu/Debian

# 3. 下载并解压 Cosbench
wget https://github.com/intel-cloud/cosbench/releases/download/v0.4.2.c4/0.4.2.c4.zip
unzip 0.4.2.c4.zip -d /opt/
mv /opt/0.4.2.c4 /opt/cosbench
cd /opt/cosbench

# 4. 添加执行权限
chmod +x *.sh

# 5. 关键修复：关闭 S3 MD5 校验（否则读测试会失败）
sed -i 's/nohup java /nohup java -Dcom.amazonaws.services.s3.disableGetObjectMD5Validation=true /' cosbench-start.sh

# 6. 取消系统 HTTP 代理（否则会导致节点通信失败）
unset http_proxy
unset https_proxy
echo "unset http_proxy" >> /etc/profile
echo "unset https_proxy" >> /etc/profile
```

### 2.2 单节点快速启动（适合测试环境）

单节点模式下，同一台机器同时运行 Controller 和 Driver 服务：

```bash
cd /opt/cosbench
sh start-all.sh

# 验证启动
ps aux | grep cosbench   # 应该能看到两个 Java 进程
```

启动成功后，访问 Web 管理界面：

> `http://<节点IP>:19088/controller/index.html`

---

## 三、核心架构与工作原理

Cosbench 采用**主从架构**，由两个核心组件组成：

| 组件 | 作用 | 默认端口 |
| ------ | ------ | ---------- |
| Controller | 控制中心，负责任务调度、进度监控、结果汇总 | 19088 |
| Driver | 负载生成器，负责实际发送 HTTP 请求到对象存储 | 18088 |

**工作流程：**

1. 用户通过 Web 界面或 CLI 提交 XML 配置文件到 Controller
2. Controller 将任务分发给所有注册的 Driver 节点
3. Driver 节点根据配置并发发送请求到对象存储
4. Driver 将测试结果实时上报给 Controller
5. Controller 汇总所有数据，生成可视化报告

---

## 四、基础使用：第一个 S3 测试任务

### 步骤 1：编写测试配置文件

Cosbench 使用 XML 文件定义测试任务，以下是一个可直接复制使用的 S3 测试模板：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<workload name="S3基础性能测试" description="4K对象100%写测试">
    <!-- 存储配置：替换为你的对象存储信息 -->
    <storage type="s3" config="
        accesskey=你的AccessKey;
        secretkey=你的SecretKey;
        endpoint=http://对象存储网关IP:端口;
        pathStyleAccess=true;   <!-- 必须开启，否则 MinIO/Ceph 会报错 -->
        connectionTimeout=30000;
        socketTimeout=60000
    " />

    <workflow>
        <!-- 阶段1：初始化（创建存储桶） -->
        <workstage name="init">
            <work type="init" workers="1" config="
                cprefix=cosbench-test-;   <!-- 存储桶前缀 -->
                containers=r(1,5);        <!-- 创建5个存储桶：cosbench-test-1到cosbench-test-5 -->
                partition=container       <!-- 存储桶平均分配给多个Driver -->
            " />
        </workstage>

        <!-- 阶段2：准备数据（上传测试对象） -->
        <workstage name="prepare">
            <work type="prepare" workers="32" config="
                containers=r(1,5);
                objects=r(1,1000);       <!-- 每个桶上传1000个对象 -->
                sizes=4k;                <!-- 对象大小：4KB -->
                division=object          <!-- 对象平均分配给多个Driver -->
            " />
        </workstage>

        <!-- 阶段3：正式测试（核心压测阶段） -->
        <workstage name="main" runtime="300">   <!-- 测试运行300秒（5分钟） -->
            <work type="normal" workers="64" config="
                containers=r(1,5);
                objects=r(1,1000);
                sizes=4k;
                op=write;                <!-- 操作类型：write/read/delete -->
                ratio=100;               <!-- 写操作占比100% -->
                interval=5               <!-- 每5秒上报一次数据 -->
            " />
        </workstage>

        <!-- 阶段4：清理数据（删除测试对象） -->
        <workstage name="cleanup">
            <work type="cleanup" workers="16" config="
                containers=r(1,5);
                objects=r(1,1000);
            " />
        </workstage>

        <!-- 阶段5：销毁（删除存储桶） -->
        <workstage name="dispose">
            <work type="dispose" workers="1" config="
                containers=r(1,5);
            " />
        </workstage>
    </workflow>
</workload>
```

### 步骤 2：提交测试任务

1. 打开 Web 管理界面：`http://<ControllerIP>:19088/controller/index.html`
2. 点击左侧菜单的 **Submit New Workloads**
3. 点击 **Browse** 选择你编写的 XML 配置文件
4. 点击 **Submit** 提交任务

### 步骤 3：查看测试结果

任务提交后，会自动跳转到任务详情页面，实时显示测试进度和性能数据。

> 📷 *（此处插入 Cosbench Web 界面任务详情截图）*

**核心指标解读：**

| 指标 | 含义 | 关注重点 |
| ------ | ------ | ---------- |
| Throughput | 吞吐量（每秒操作数） | 越高越好，代表系统处理能力 |
| Bandwidth | 带宽（MB/s） | 大文件测试重点关注 |
| Avg ResTime | 平均响应时间（ms） | 越低越好，代表用户体验 |
| 95th ResTime | 95% 响应时间（ms） | 比平均时间更重要，代表大多数用户的体验 |
| 99th ResTime | 99% 响应时间（ms） | 极端情况的性能表现 |
| Success Ratio | 成功率 | **必须 100%**，否则测试结果无效 |

测试完成后，点击 **Download** 按钮可下载完整的 HTML 和 CSV 报告，用于后续分析。

---

## 五、核心参数详解

### 5.1 存储配置参数（`storage` 标签）

| 参数 | 说明 | 示例值 |
| ------ | ------ | -------- |
| `type` | 存储类型 | `s3` / `swift` / `azureblob` |
| `accesskey` | 访问密钥 | `AKIAIOSFODNN7EXAMPLE` |
| `secretkey` | 安全密钥 | `wJalrXUtnFEMI/...` |
| `endpoint` | 对象存储网关地址 | `http://192.168.1.100:9000` |
| `pathStyleAccess` | 是否使用路径风格访问 | `true`（MinIO/Ceph 必须）/ `false`（AWS S3） |
| `connectionTimeout` | 连接超时时间（ms） | `30000` |
| `socketTimeout` | 套接字超时时间（ms） | `60000` |

### 5.2 工作配置参数（`work` 标签）

| 参数 | 说明 | 常用值 |
| ------ | ------ | -------- |
| `type` | 工作类型 | `init` / `prepare` / `normal` / `cleanup` / `dispose` |
| `workers` | 并发线程数 | `1, 8, 32, 64, 128` |
| `runtime` | 运行时间（秒） | `60, 300, 600` |
| `containers` | 存储桶范围 | `r(1,10)`（1 到 10 号桶） |
| `objects` | 对象范围 | `r(1,10000)`（1 到 10000 号对象） |
| `sizes` | 对象大小 | `4k, 64k, 1M, 10M, 100M, 1G` |
| `op` | 操作类型 | `write` / `read` / `delete` / `list` |
| `ratio` | 操作占比 | `70`（70% 读）、`30`（30% 写） |
| `division` | 任务分配方式 | `object`（按对象分配）/ `container`（按桶分配） |

---

## 六、典型测试场景模板

### 场景 1：混合读写性能测试（70% 读 + 30% 写）

```xml
<workstage name="main" runtime="300">
    <work type="normal" workers="64" config="
        containers=r(1,5);
        objects=r(1,1000);
        sizes=8k;
        op=read;
        ratio=70;
    " />
    <work type="normal" workers="64" config="
        containers=r(1,5);
        objects=r(1,1000);
        sizes=8k;
        op=write;
        ratio=30;
    " />
</workstage>
```

### 场景 2：大文件吞吐量测试（100M 对象）

```xml
<workstage name="prepare">
    <work type="prepare" workers="8" config="
        containers=r(1,2);
        objects=r(1,100);
        sizes=100M;
    " />
</workstage>

<workstage name="main" runtime="300">
    <work type="normal" workers="16" config="
        containers=r(1,2);
        objects=r(1,100);
        sizes=100M;
        op=read;
        ratio=100;
    " />
</workstage>
```

### 场景 3：小文件并发测试（1K 对象）

```xml
<workstage name="prepare">
    <work type="prepare" workers="64" config="
        containers=r(1,10);
        objects=r(1,10000);
        sizes=1k;
    " />
</workstage>

<workstage name="main" runtime="300">
    <work type="normal" workers="128" config="
        containers=r(1,10);
        objects=r(1,10000);
        sizes=1k;
        op=read;
        ratio=100;
    " />
</workstage>
```

### 场景 4：元数据性能测试（LIST 操作）

```xml
<workstage name="main" runtime="300">
    <work type="normal" workers="32" config="
        containers=r(1,5);
        op=list;
        listlength=1000;   <!-- 每次列出 1000 个对象 -->
    " />
</workstage>
```

---

## 七、高级功能使用教程

### 7.1 多节点分布式压测（生产环境必备）

当单节点 Driver 无法产生足够压力时，可部署多节点 Driver 集群。

**部署步骤：**

**①** 在所有 Driver 节点上执行前面的安装脚本。

**②** 在每个 Driver 节点上修改 `start-driver.sh`，将 IP 改为当前节点的实际 IP：

```bash
vim /opt/cosbench/start-driver.sh
# 修改第 3 行：ip=127.0.0.1 → ip=当前节点IP
```

**③** 在每个 Driver 节点上启动 Driver 服务：

```bash
sh start-driver.sh
```

**④** 在 Controller 节点上修改 `conf/controller.conf`，注册所有 Driver：

```ini
[controller]
concurrency=1
drivers=3   # Driver 节点总数
log_level=INFO

[driver1]
name=driver1
url=http://192.168.1.101:18088/driver

[driver2]
name=driver2
url=http://192.168.1.102:18088/driver

[driver3]
name=driver3
url=http://192.168.1.103:18088/driver
```

**⑤** 重启 Controller 服务：

```bash
sh stop-controller.sh
sh start-controller.sh
```

**⑥** 验证：打开 Web 界面，左侧 **Active Drivers** 应显示所有注册的 Driver 节点。

### 7.2 数据完整性校验

Cosbench 支持在读写过程中自动校验数据完整性，检测静默数据损坏。

**使用方法**：在 `storage` 标签中添加 `validation=true` 参数：

```xml
<storage type="s3" config="
    accesskey=xxx;
    secretkey=xxx;
    endpoint=http://xxx;
    pathStyleAccess=true;
    validation=true   <!-- 开启数据校验 -->
" />
```

> ⚠️ **注意**：数据校验会增加 CPU 开销，约降低 10-20% 的性能。建议在可靠性测试时开启，纯性能测试时关闭。

### 7.3 分段上传测试（大文件必备）

对于大于 100M 的文件，建议使用分段上传功能，可显著提高上传速度和稳定性。

> ⚠️ **注意**：官方版 Cosbench 不支持 `mprepare` 分段上传，需使用第三方增强版（如 [SineIO/cosbench](https://github.com/sine-io/cosbench-sineio)）。

**配置示例：**

```xml
<work type="mprepare" workers="8" config="
    containers=r(1,2);
    objects=r(1,10);
    sizes=1G;
    partsize=100M;   <!-- 分段大小：100MB -->
" />
```

### 7.4 压力曲线测试（自动阶梯并发）

自动测试不同并发数下的性能表现，生成性能曲线：

```xml
<workstage name="main">
    <work type="normal" workers="(1,8,16,32,64,128)" config="
        containers=r(1,5);
        objects=r(1,1000);
        sizes=4k;
        op=read;
        ratio=100;
        runtime=60;   <!-- 每个并发级别运行 60 秒 -->
    " />
</workstage>
```

> `workers="(1,8,16,32,64,128)"` 为 Cosbench 阶梯并发语法，会自动依次按每个并发档位执行测试。

---

## 八、使用技巧与最佳实践

### 8.1 测试前准备

| 准备项 | 说明 |
| -------- | ------ |
| **时间同步** | 所有节点和对象存储服务器时间误差不能超过 5 分钟，否则会导致 S3 签名认证失败 |
| **足够的数据量** | 测试对象总数应大于对象存储缓存大小的 3 倍，避免缓存影响测试结果 |
| **合理预热时间** | 正式测试前先运行 5-10 分钟预热，让系统达到稳定状态 |
| **关闭干扰服务** | 测试期间关闭其他占用 CPU、内存和网络的服务 |

**时间同步命令：**

```bash
yum install -y chrony
systemctl start chronyd
chronyc sources -v
```

### 8.2 参数调优技巧

**`workers` 数量设置：**

| 场景 | 每个 Driver 的建议 workers 数 |
| ------ | ------ |
| 通用上限 | 不超过 CPU 核心数的 2 倍 |
| 小文件测试 | 64 - 128 |
| 大文件测试 | 8 - 16 |

**对象大小选择：**

| 业务场景 | 建议对象大小 |
| ---------- | -------------- |
| 图片、文档等小文件 | 4K - 64K |
| 视频、备份等大文件 | 1M - 1G |
| 数据库备份 | 10M - 100M |

**JVM 内存调整**（测试大量小文件时必须增加）：

```bash
vim cosbench-start.sh
# 修改 startup 命令，添加 JVM 参数：-Xmx8G -Xms4G
nohup java -Xmx8G -Xms4G -Dcom.amazonaws.services.s3.disableGetObjectMD5Validation=true ...
```

### 8.3 避坑指南

| 避坑项 | 说明 |
| ------ | ------ |
| ❌ 不要使用 root 用户运行 | 可能导致权限问题和安全风险 |
| ❌ 测试完成后必须清理数据 | 否则会占用大量存储空间 |
| ❌ 避免跨地域测试 | 网络延迟会严重影响测试结果，建议同地域内网测试 |
| ✅ 多次测试取平均值 | 每次测试运行 3-5 次，取平均值以减少误差 |

---

## 九、常见问题与解决方案

### 问题 1：启动报错 `Ncat: Connection refused`

**原因**：Java 未安装或版本不正确。

```bash
# 检查 Java 版本
java -version
# 确保输出是 java version "1.8.0_xxx"
# 如果不是，卸载其他版本，重新安装 Java 8
```

### 问题 2：读测试失败 `Unable to verify integrity of data download`

**原因**：S3 MD5 校验问题。

**解决**：确保 `cosbench-start.sh` 中已添加 `-Dcom.amazonaws.services.s3.disableGetObjectMD5Validation=true` 参数（安装脚本第 5 步已做此修复）。

### 问题 3：认证失败 `The request signature we calculated does not match`

**原因**：
- AccessKey 或 SecretKey 错误
- 节点时间不同步（差距超过 5 分钟）
- endpoint 格式错误

**解决**：
1. 检查 AccessKey 和 SecretKey 是否正确
2. 同步所有节点时间（参考 8.1 节）
3. 确保 endpoint 包含协议头（`http://` 或 `https://`）

### 问题 4：Driver 节点无法连接到 Controller

**原因**：防火墙未关闭或端口未开放。

```bash
# 临时关闭防火墙
systemctl stop firewalld

# 或开放指定端口
firewall-cmd --zone=public --add-port=19088/tcp --permanent
firewall-cmd --zone=public --add-port=18088/tcp --permanent
firewall-cmd --reload
```

### 问题 5：测试过程中出现大量超时错误

**原因**：
- 对象存储性能达到瓶颈
- 网络带宽不足
- Driver 节点压力过大

**解决**：
1. 减少 `workers` 数量
2. 检查网络带宽（使用 `iftop` 等工具）
3. 增加 Driver 节点数量

---

## 十、总结

Cosbench 是对象存储性能测试的首选工具，通过合理配置可以模拟各种真实业务场景，全面评估对象存储的性能和可靠性。

**使用建议：**

1. 从简单的单节点单线程测试开始，逐步增加复杂度
2. 每次只改变一个参数，便于分析参数对性能的影响
3. 结合监控工具（如 Prometheus + Grafana）同时监控对象存储服务器的 CPU、内存、磁盘和网络使用情况
4. 测试完成后，详细记录测试环境、配置参数和结果，便于后续对比分析

---

> 📌 **参考资料**
> - [Cosbench 官方 GitHub](https://github.com/intel-cloud/cosbench)
> - [SineIO 增强版 Cosbench](https://github.com/sine-io/cosbench-sineio)（支持分段上传等扩展功能）

> 🔧 **本文环境**：Cosbench v0.4.2.c4 / Java 8 / CentOS 7+ / Ubuntu 18.04+

---

*本文为 Cosbench 对象存储性能测试一站式指南，如有疑问欢迎在评论区交流。*

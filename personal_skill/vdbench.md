# Vdbench 存储测试工具完整使用教程

Vdbench 是 Oracle 官方开发的企业级存储 I/O 性能测试工具，广泛应用于磁盘阵列、SAN/NAS、分布式存储、云盘等存储系统的性能评估与数据完整性验证。它支持跨平台运行（Linux / Windows / macOS），具备高度灵活的工作负载定义能力和强大的分布式测试功能。

---

## 一、工具简介与版本说明

### 核心优势

| 优势 | 说明 |
|------|------|
| **跨平台兼容性** | 同一安装包支持 Linux、Windows 和 macOS |
| **双模式测试** | 同时支持块设备（Raw Disk）和文件系统（File System）测试 |
| **分布式架构** | 支持多客户端协同测试，模拟真实生产环境的并发压力 |
| **数据完整性校验** | 内置强大的数据校验机制，可检测静默数据损坏 |
| **丰富的报告** | 生成 HTML 格式的详细报告，包含 IOPS、吞吐量、延迟分布等关键指标 |

### 最新稳定版本

- **推荐版本**：5.04.07（2024 年发布）
- **官方下载地址**：Oracle Vdbench Downloads（需 Oracle 账号登录）
- **官方文档**：下载包内包含 `vdbench.pdf` 完整用户指南

---

## 二、安装部署

### 前置条件

- **Java 环境**：需要 Java 8 或更高版本（64 位）
- **Linux 额外依赖**：需要安装 `csh`（C Shell）

### Linux 系统安装

```bash
# 1. 安装 Java 和 csh
yum install java-1.8.0-openjdk csh -y   # CentOS / RHEL
apt-get install openjdk-8-jdk csh -y    # Ubuntu / Debian

# 2. 下载并解压 vdbench
unzip vdbench50407.zip -d /opt/vdbench

# 3. 添加执行权限
cd /opt/vdbench
chmod +x vdbench

# 4. 验证安装
./vdbench -t
```

### Windows 系统安装

```cmd
# 1. 安装 64 位 Java 8 或更高版本
# 2. 解压 vdbench50407.zip 到任意目录（如 C:\vdbench）
# 3. 打开命令提示符，进入 vdbench 目录
# 4. 执行验证命令：
vdbench.bat -t
```

---

## 三、基础使用入门

Vdbench 通过配置文件（`.par` 文件）定义测试参数，然后通过命令行执行。

### 命令行基本语法

```bash
# Linux
./vdbench -f 配置文件.par -o 输出目录

# Windows
vdbench.bat -f 配置文件.par -o 输出目录
```

### 块设备测试（Raw Disk）

适用于测试裸盘、LUN、云盘等块设备的性能。

**示例：单盘 4K 随机读测试**

```
# 存储设备定义（Storage Define）
sd=sd1, lun=/dev/nvme0n1, openflags=o_direct, size=100G

# 工作负载定义（Workload Define）
wd=wd1, sd=sd1, rdpct=100, seekpct=100, xfersize=4k, threads=32

# 运行定义（Run Define）
rd=rd1, wd=wd1, iorate=max, warmup=60, elapsed=300, interval=5
```

### 文件系统测试（File System）

适用于测试 NFS、SMB、本地文件系统等的性能。

**示例：文件系统 1M 顺序写测试**

```
# 文件系统定义（File System Define）
fsd=fsd1, anchor=/mnt/test, depth=2, width=5, files=100, size=1G, openflags=directio

# 文件工作负载定义（File Workload Define）
fwd=fwd1, fsd=fsd1, operation=write, fileio=sequential, xfersize=1M, threads=16

# 运行定义
rd=rd1, fwd=fwd1, fwdrate=max, format=yes, warmup=60, elapsed=300, interval=5
```

---

## 四、核心参数详解

### 块设备测试核心参数（SD / WD）

| 参数 | 说明 | 常用值 |
|------|------|--------|
| `sd` | 存储设备名称，自定义 | `sd1`, `sd2`... |
| `lun` | 块设备路径 | `/dev/sdb`, `/dev/nvme0n1` |
| `openflags` | 打开标志 | `o_direct`（绕过缓存） |
| `size` | 测试使用的设备大小 | `10G`, `100G`, `1T` |
| `wd` | 工作负载名称，自定义 | `wd1`, `wd2`... |
| `rdpct` | 读请求百分比 | `0`（纯写）, `50`（读写各半）, `100`（纯读） |
| `seekpct` | 随机访问百分比 | `0`（顺序）, `100`（随机） |
| `xfersize` | I/O 块大小 | `4k`, `8k`, `64k`, `1M` |
| `threads` | 并发线程数 | `1`, `8`, `32`, `128` |

### 文件系统测试核心参数（FSD / FWD）

| 参数 | 说明 | 常用值 |
|------|------|--------|
| `fsd` | 文件系统名称，自定义 | `fsd1`, `fsd2`... |
| `anchor` | 测试目录路径 | `/mnt/nfs`, `E:\test` |
| `depth` | 目录深度 | `1`, `2`, `3` |
| `width` | 每层目录数 | `5`, `10`, `100` |
| `files` | 每个目录的文件数 | `10`, `100`, `1000` |
| `size` | 单个文件大小 | `64k`, `1G`, `10G` |
| `shared` | 是否多客户端共享同一目录 | `yes` / `no` |
| `fwd` | 文件工作负载名称，自定义 | `fwd1`, `fwd2`... |
| `operation` | 操作类型 | `read`, `write`, `create`, `delete` |
| `fileio` | 文件 I/O 模式 | `sequential`, `random` |
| `fileselect` | 文件选择方式 | `sequential`, `random` |

### 运行控制核心参数（RD）

| 参数 | 说明 | 常用值 |
|------|------|--------|
| `rd` | 运行定义名称，自定义 | `rd1`, `rd2`... |
| `iorate` / `fwdrate` | I/O 速率 | `max`（最大）, `1000`（固定 IOPS） |
| `warmup` | 预热时间（秒） | `30`, `60`, `120` |
| `elapsed` | 正式测试时间（秒） | `300`, `600`, `1800` |
| `interval` | 报告间隔（秒） | `1`, `5`, `10` |
| `format` | 是否格式化文件系统 | `yes` / `no` / `restart` |

---

## 五、典型测试场景模板

### 场景 1：SSD 最大随机读 IOPS 测试

```
messagescan=no
sd=sd1, lun=/dev/nvme0n1, openflags=o_direct, size=100G
wd=wd1, sd=sd1, rdpct=100, seekpct=100, xfersize=4k, threads=128
rd=rd1, wd=wd1, iorate=max, warmup=60, elapsed=600, interval=1
```

### 场景 2：HDD 顺序吞吐量测试

```
messagescan=no
sd=sd1, lun=/dev/sdb, openflags=o_direct, size=500G
wd=wd1, sd=sd1, rdpct=0, seekpct=0, xfersize=1M, threads=8
rd=rd1, wd=wd1, iorate=max, warmup=30, elapsed=300, interval=5
```

### 场景 3：数据库混合负载模拟（70% 读 / 30% 写）

```
messagescan=no
sd=sd1, lun=/dev/vdb, openflags=o_direct, size=200G
wd=wd1, sd=sd1, rdpct=70, seekpct=100, xfersize=8k, threads=64
rd=rd1, wd=wd1, iorate=max, warmup=60, elapsed=600, interval=5
```

### 场景 4：NFS 小文件性能测试

```
messagescan=no
fsd=fsd1, anchor=/mnt/nfs_share, depth=2, width=100, files=100, size=64k, openflags=directio
fwd=format, threads=32, xfersize=32k
fwd=fwd1, fsd=fsd1, operation=read, rdpct=60, xfersize=32k, threads=32
rd=rd1, fwd=fwd1, fwdrate=max, format=restart, elapsed=600, interval=1
```

---

## 六、测试结果解读

Vdbench 会在指定的输出目录生成一系列报告文件，其中最重要的是：

| 文件 | 说明 |
|------|------|
| `summary.html` | 测试结果汇总报告 |
| `totals.html` | 详细的性能统计数据 |
| `histogram.html` | 延迟分布直方图 |
| `flatfile.csv` | 原始数据，可用于 Excel 分析 |

### 核心性能指标

| 指标 | 含义 | 计算方式 |
|------|------|----------|
| **IOPS** | 每秒 I/O 操作数 | 总 I/O 数 / 测试时间 |
| **MB/sec** | 吞吐量（每秒传输数据量） | IOPS × 块大小 / 1024 |
| **Resp Time** | 平均响应延迟（ms） | 总延迟时间 / 总 I/O 数 |
| **Max Resp** | 最大响应延迟（ms） | 单次 I/O 的最长耗时 |
| **CPU%** | CPU 使用率 | 系统 CPU + 用户 CPU |

### 结果分析要点

- **预热数据排除**：最终结果通常取 `avg_2-N`（排除第一个时间间隔）
- **指标联动分析**：高 IOPS 但高延迟，可能表示系统过载
- **稳定性观察**：查看 `interval` 数据，判断性能是否稳定
- **错误检查**：确保 I/O errors 为 0，否则测试结果不可信
- **瓶颈定位**：
  - 吞吐量达到上限但 CPU 使用率低 → 存储带宽瓶颈
  - CPU 使用率接近 100% → 客户端 CPU 瓶颈
  - 延迟随并发数急剧上升 → 存储系统处理能力瓶颈

---

## 七、使用技巧与最佳实践

### 测试前准备

1. **使用 O_DIRECT 模式**：`openflags=o_direct` 绕过操作系统缓存，获取真实磁盘性能
2. **足够的测试数据量**：测试数据量应大于存储系统缓存大小（通常 ≥ 3 倍）
3. **合理的预热时间**：SSD 建议预热 60 秒以上，HDD 建议预热 30 秒以上
4. **足够的测试时长**：正式测试时间建议 ≥ 5 分钟，以获得稳定的统计结果
5. **关闭不必要的服务**：测试期间关闭其他可能占用资源的服务

### 参数调优技巧

- **线程数调整**：逐步增加线程数，直到 IOPS 不再增长或延迟超过阈值
- **块大小选择**：
  - 数据库、OLTP 场景：`4k` ~ `16k`
  - 文件服务器、流媒体：`64k` ~ `1M`
  - 备份、归档场景：`1M` ~ `4M`
- **I/O 对齐**：使用 `align=4k` 或 `align=8k` 确保 I/O 对齐，提升 SSD 性能
- **数据模式**：使用 `pattern=random` 生成随机数据，避免存储系统压缩 / 去重影响测试结果

### 自动化测试脚本

```bash
#!/bin/bash
# 自动化测试脚本：测试不同块大小的随机读性能

BLOCK_SIZES=("4k" "8k" "16k" "32k" "64k")
THREADS=32
DEVICE=/dev/nvme0n1

for bs in "${BLOCK_SIZES[@]}"; do
    echo "Testing $bs random read..."
    cat > test_${bs}.par << EOF
messagescan=no
sd=sd1, lun=$DEVICE, openflags=o_direct, size=100G
wd=wd1, sd=sd1, rdpct=100, seekpct=100, xfersize=$bs, threads=$THREADS
rd=rd1, wd=wd1, iorate=max, warmup=60, elapsed=300, interval=5
EOF
    ./vdbench -f test_${bs}.par -o output_${bs}
done
```

---

## 八、高级功能使用教程

### 1. 多客户端分布式测试

Vdbench 支持主从架构，由一个主节点控制多个从节点同时发起 I/O 请求。

**配置步骤**：

1. 在所有节点上安装相同版本的 vdbench 和 Java
2. 配置主节点到所有从节点的 SSH 免密登录
3. 在配置文件中定义所有主机

**示例：三客户端块设备测试**

```
messagescan=no
# 主机定义（Host Define）
hd=default, vdbench=/opt/vdbench, user=root, shell=ssh
hd=hd1, system=192.168.1.101
hd=hd2, system=192.168.1.102
hd=hd3, system=192.168.1.103

# 存储设备定义（每个客户端都有自己的 sd）
sd=sd1, host=hd1, lun=/dev/vdb, openflags=o_direct, size=100G
sd=sd2, host=hd2, lun=/dev/vdb, openflags=o_direct, size=100G
sd=sd3, host=hd3, lun=/dev/vdb, openflags=o_direct, size=100G

# 工作负载定义
wd=wd1, sd=sd*, rdpct=70, seekpct=100, xfersize=8k, threads=32

# 运行定义
rd=rd1, wd=wd1, iorate=max, warmup=60, elapsed=600, interval=5
```

> **执行方式**：在主节点上执行测试命令即可，主节点会自动将配置文件分发到所有从节点并协调测试。

### 2. 数据完整性校验

Vdbench 提供强大的数据校验功能，可检测存储系统的静默数据损坏。

**关键参数**：

| 参数 | 说明 |
|------|------|
| `-j` | 启用数据校验，校验日志写入磁盘 |
| `-jn` | 异步写入校验日志，性能影响更小 |
| `-jr` | 读取校验日志并验证数据完整性 |

**使用方法**：

```bash
# 第一步：写入数据并生成校验日志
./vdbench -f write_test.par -jn -o output_write

# 第二步：验证数据完整性
./vdbench -f write_test.par -jr -o output_verify
```

> **注意**：数据校验会增加 CPU 和磁盘开销，测试性能时建议关闭，验证数据可靠性时再开启。

### 3. 混合负载测试

Vdbench 支持同时运行多个不同的工作负载，模拟真实生产环境中的复杂 I/O 模式。

**示例：同时运行 OLTP 和备份负载**

```
messagescan=no
sd=sd1, lun=/dev/vdb, openflags=o_direct, size=200G

# OLTP 负载：70% 读 30% 写，8k 随机
wd=oltp, sd=sd1, rdpct=70, seekpct=100, xfersize=8k, threads=64

# 备份负载：100% 写，1M 顺序
wd=backup, sd=sd1, rdpct=0, seekpct=0, xfersize=1M, threads=4

# 运行定义：同时运行两个负载
rd=rd1, wd=(oltp,backup), iorate=max, warmup=60, elapsed=600, interval=5
```

### 4. 曲线测试（IO Rate Curve）

曲线测试可以自动测试不同 IOPS 下的延迟表现，生成性能曲线。

**示例：测试从 1000 到 10000 IOPS 的延迟**

```
messagescan=no
sd=sd1, lun=/dev/vdb, openflags=o_direct, size=100G
wd=wd1, sd=sd1, rdpct=70, seekpct=100, xfersize=8k, threads=32

# 曲线测试：IOPS 从 1000 到 10000，步长 1000
rd=rd1, wd=wd1, iorate=(curve), curve=(1000-10000,1000), warmup=30, elapsed=60, interval=1
```

### 5. 元数据性能测试

Vdbench 可以测试文件系统的元数据操作性能，如文件创建、删除、重命名等。

**示例：文件创建性能测试**

```
messagescan=no
fsd=fsd1, anchor=/mnt/test, depth=2, width=100, files=100, size=0, openflags=directio

# 文件创建操作
fwd=create, fsd=fsd1, operation=create, threads=32

# 运行定义
rd=rd1, fwd=create, fwdrate=max, format=no, elapsed=300, interval=1
```

---

## 九、常见问题与解决方案

### 问题 1：Java 版本不兼容

- **错误信息**：`Unsupported major.minor version 52.0`
- **解决方案**：安装 Java 8 或更高版本，并确保 `JAVA_HOME` 环境变量指向正确的 Java 路径。

### 问题 2：权限不足

- **错误信息**：`Permission denied`
- **解决方案**：
  - 为 vdbench 脚本添加执行权限：`chmod +x vdbench`
  - 确保测试用户对块设备或测试目录有读写权限
  - Linux 下测试块设备建议使用 `root` 用户

### 问题 3：多客户端 SSH 连接失败

- **错误信息**：`ssh: connect to host port 22: Connection refused`
- **解决方案**：
  - 确保所有从节点都安装了 SSH 服务并已启动
  - 配置主节点到从节点的免密登录
  - 检查防火墙设置，确保 22 端口开放

### 问题 4：测试结果不稳定

- **可能原因**：
  - 测试数据量太小，被存储系统缓存影响
  - 预热时间不足
  - 系统中有其他进程占用资源
  - 存储系统正在进行后台操作（如垃圾回收、数据重建）
- **解决方案**：
  - 增加测试数据量（≥ 3 倍缓存大小）
  - 延长预热时间
  - 关闭不必要的服务
  - 等待存储系统后台操作完成后再测试

### 问题 5：数据校验失败

- **错误信息**：`Data integrity error detected`
- **解决方案**：
  - 重新运行测试，确认是否为偶发错误
  - 检查存储系统的硬件健康状态
  - 检查存储系统的配置（如 RAID 级别、缓存策略）
  - 检查网络连接（如果是网络存储）

---

## 十、总结

Vdbench 是一款功能强大、灵活度高的企业级存储测试工具。通过合理配置参数，可以模拟各种真实的业务负载，全面评估存储系统的性能和可靠性。

**使用建议**：

1. 从简单的单线程顺序读写开始，逐步增加复杂度
2. 每次只改变一个参数，便于分析参数对性能的影响
3. 多次运行测试，取平均值以减少误差
4. 结合其他工具（如 `iostat`、`nmon`）进行全方位监控
5. 测试完成后，详细记录测试环境和参数，便于后续对比分析

---

> **声明**：本文基于 Vdbench 5.04.07 官方文档编写，旨在提供中文操作指南。具体参数请以官方 `vdbench.pdf` 为准。

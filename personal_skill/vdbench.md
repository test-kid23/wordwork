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

- **推荐版本**：5.04.06（2024 年发布）
- **官方下载地址**：Oracle Vdbench Downloads（需 Oracle 账号登录）
- **官方文档**：下载包内包含 `vdbench.pdf` 完整用户指南

---

## 二、安装部署

### 前置条件

- **Java 环境**：需要 Java 8 或更高版本（64 位）——**唯一必须手动安装的依赖**
- **Linux**：Vdbench 启动脚本是 C Shell 脚本（`csh`），但 CentOS/RHEL 通常已预装；Ubuntu/Debian 最小化安装可能需要手动装。**遇到 `bad interpreter: /bin/csh` 错误再装就行**。
- **Windows**：只需 64 位 Java，无需额外 Shell 环境

> **关于启动脚本的认知关键**：Vdbench 本质上是一个 Java 程序（`vdbench.jar`），`vdbench` 和 `vdbench.bat` 只是不同系统下的启动外壳。Linux 用 C Shell（`csh`），Windows 用 Batch（`cmd`）。理解这一点，很多问题自然迎刃而解。

### Linux 系统安装

```bash
# 1. 安装 Java（csh 通常已预装，出问题再补）
yum install java-1.8.0-openjdk -y   # CentOS / RHEL
apt-get install openjdk-8-jdk -y    # Ubuntu / Debian

# 1.1 验证 Java 安装
java -version           # 确认版本 ≥ 1.8
echo $JAVA_HOME         # 确认环境变量已设置

# 1.2 如果遇到 "bad interpreter: /bin/csh"，补装 csh：
yum install csh -y                  # CentOS / RHEL
apt-get install csh -y              # Ubuntu / Debian

# 2. 下载并解压 vdbench
unzip vdbench50406.zip -d /opt/vdbench

# 3. 添加执行权限（vdbench 是 csh 脚本）
cd /opt/vdbench
chmod +x vdbench

# 4. 验证安装
./vdbench -t            # 输出测试配置即表示安装成功
```

### Windows 系统安装

```cmd
REM 1. 安装 64 位 Java 8 或更高版本
REM    （推荐 Oracle JDK 或 OpenJDK，安装后确保 java 在 PATH 中）

REM 1.1 验证 Java
java -version
REM 预期输出：java version "1.8.0_xxx" 或更高

REM 2. 解压 vdbench50406.zip 到任意目录（如 C:\vdbench）

REM 3. 打开命令提示符（cmd 或 PowerShell），进入 vdbench 目录
cd C:\vdbench

REM 4. 执行验证命令：
vdbench.bat -t
REM 注意：Windows 下使用 vdbench.bat，而非 vdbench
```

### Linux 🆚 Windows 关键差异速查表

| 差异点 | Linux | Windows |
|--------|-------|---------|
| **启动脚本** | `./vdbench`（C Shell 脚本） | `vdbench.bat`（Batch 脚本） |
| **依赖** | Java 8+（`csh` 通常已预装） | Java 8+（仅此） |
| **设备路径** | `/dev/sdb`, `/dev/nvme0n1` | `\\.\PhysicalDrive1` 或 `D:` |
| **目录路径** | `/mnt/test` | `E:\test` |
| **权限要求** | root 或 sudo（块设备） | 管理员权限（块设备） |
| **openflags** | `o_direct` 块设备 / `directio` 文件系统均可用 | 块设备用 `o_direct`；**SMB/网络路径必须用 `directio`**，`o_direct` 会报错 |
| **路径分隔符** | `/`（正斜杠） | `\`（反斜杠，par 文件中直接用反斜杠） |

> **重要提醒**：Windows 下测试物理磁盘需要用 `\\.\PhysicalDriveN` 格式（N 为磁盘编号），可在"磁盘管理"或 `diskpart` 中确认。Windows 的 `vdbench.bat` 本质上是调用 `java -jar vdbench.jar` 并传递参数，与 Linux 上的 `vdbench` 脚本行为完全一致。

---

## 三、基础使用入门

Vdbench 通过配置文件（通常是 `.par` 文件，但不强制——不加后缀也能执行）定义测试参数，然后通过命令行运行。

### 命令行基本语法

```bash
# Linux
./vdbench -f 配置文件.par -o 输出目录

# Windows
vdbench.bat -f 配置文件.par -o 输出目录
```

### 块设备测试（Raw Disk）

适用于测试裸盘、LUN、云盘等块设备的性能。这是 Vdbench 最直接的使用方式——直接对块设备发起读写，不经过文件系统。

**Linux 示例：单盘 4K 随机读测试**

```bash
# 存储设备定义（Storage Define）
sd=sd1, lun=/dev/nvme0n1, openflags=o_direct, size=100G

# 工作负载定义（Workload Define）
wd=wd1, sd=sd1, rdpct=100, seekpct=100, xfersize=4k, threads=32

# 运行定义（Run Define）
rd=rd1, wd=wd1, iorate=max, warmup=60, elapsed=300, interval=5
```

**Windows 示例：物理磁盘 4K 随机读测试**

```bash
# Windows 下测试物理磁盘用 \\.\PhysicalDriveN（N 为磁盘编号）
# 通过 diskpart → list disk 查看磁盘编号
sd=sd1, lun=\\.\PhysicalDrive1, openflags=o_direct, size=100G

wd=wd1, sd=sd1, rdpct=100, seekpct=100, xfersize=4k, threads=32

rd=rd1, wd=wd1, iorate=max, warmup=60, elapsed=300, interval=5
```

> **⚠️ 危险警告**：`openflags=o_direct` 绕过了操作系统缓存，但不会阻止你误操作磁盘。**务必确认 `lun` 指向的是正确的测试磁盘**，否则可能摧毁生产数据。Windows 下 `\\.\PhysicalDrive0` 通常是系统盘，千万不要碰！

### 文件系统测试（File System）

适用于测试 NFS、SMB、本地文件系统等的性能。文件系统模式会先在指定目录下创建文件结构，再对文件进行读写操作。

**Linux 示例：文件系统 1M 顺序写测试**

```bash
# 文件系统定义（File System Define）
fsd=fsd1, anchor=/mnt/test, depth=2, width=5, files=100, size=1G, openflags=directio

# 文件工作负载定义（File Workload Define）
fwd=fwd1, fsd=fsd1, operation=write, fileio=sequential, xfersize=1M, threads=16

# 运行定义
rd=rd1, fwd=fwd1, fwdrate=max, format=yes, warmup=60, elapsed=300, interval=5
```

**Windows 示例：本地目录 1M 顺序写测试**

```bash
fsd=fsd1, anchor=E:\vdbench_test, depth=2, width=5, files=100, size=1G, openflags=directio

fwd=fwd1, fsd=fsd1, operation=write, fileio=sequential, xfersize=1M, threads=16

rd=rd1, fwd=fwd1, fwdrate=max, format=yes, warmup=60, elapsed=300, interval=5
```

### 块设备 vs 文件系统：什么时候用哪个？

| 对比维度 | 块设备测试（SD） | 文件系统测试（FSD） |
|----------|:---:|:---:|
| **测试目标** | 磁盘 / LUN 本身的裸性能 | 文件系统层 + 存储层的综合性能 |
| **适用场景** | 数据库裸盘、SAN LUN、云盘 | NFS/SMB 共享、本地文件系统、NAS |
| **是否产生文件** | ❌ 不产生，直接写扇区 | ✅ 会产生，需要 `format=yes` 预处理 |
| **数据校验支持** | ✅ 通过 SDs（需额外定义） | ✅ 原生支持 |
| **Windows 路径** | `\\.\PhysicalDrive1` | `D:\test` 或 `E:\vdbench_data` |
| **测试代表什么** | "这块盘能跑多快" | "这个文件系统上能跑多快" |
| **受文件系统影响** | ❌ 不受 | ✅ 受（文件系统元数据开销） |

---

## 四、缓存读写 vs 绕过缓存读写（openflags 详解）

这是 Vdbench 测试中**最重要、也最容易被忽视的概念**。如果不理解，你的测试结果可能毫无意义。

### 操作系统缓存的干扰

当你读写文件或块设备时，操作系统会在内存中缓存数据：

```
┌─────────────┐      ┌─────────────────┐      ┌──────────┐
│  Vdbench     │ ──→  │  操作系统页面缓存  │ ──→  │   磁盘    │
│  应用层 I/O   │ ←──  │  (Page Cache)    │ ←──  │  物理介质  │
└─────────────┘      └─────────────────┘      └──────────┘
      ↑                      ↑                      ↑
   测试工具              缓存命中≈内存速度        真实磁盘速度
```

**不绕过缓存时**：
- 写操作：数据写入内存缓存就返回"完成"，实际并未落盘 → **虚假高 IOPS**
- 读操作：如果数据已在缓存中，直接从内存读取 → **虚假高 IOPS、虚假低延迟**

**绕过缓存时**：
- 写操作：必须等待数据真正写入磁盘才返回 → **真实磁盘性能**
- 读操作：直接从磁盘读取，不经过缓存 → **真实磁盘性能**

### openflags 参数详解

#### 块设备测试（SD）

| openflags 值 | 行为 | 适用场景 |
|-------------|------|----------|
| `o_direct` | **绕过操作系统缓存**，直接读写磁盘 | ⭐ **性能基准测试，推荐默认使用** |
| 不设置（默认） | 使用系统缓存，性能数据"虚高" | 仅测试缓存性能或排查缓存问题时使用 |
| `o_dsync` | 每次写操作后同步元数据 | 对数据一致性要求极高的场景 |

**示例对比**：

```bash
# ❌ 不使用 o_direct — 测得的是"内存+磁盘"的混合性能，不可信
sd=sd1, lun=/dev/nvme0n1, size=100G

# ✅ 使用 o_direct — 测得的是磁盘真实性能
sd=sd1, lun=/dev/nvme0n1, openflags=o_direct, size=100G
```

#### 文件系统测试（FSD）

| openflags 值 | 行为 | 说明 |
|-------------|------|------|
| `directio` | 绕过文件系统缓存 | 等价于块设备的 `o_direct` |
| 不设置（默认） | 使用文件系统缓存 | 测试结果受缓存严重干扰 |
| `sync` | 同步写入模式 | 每次写入确认落盘 |

**示例对比**：

```bash
# ❌ 不绕过缓存 — NFS 客户端缓存会严重干扰测试
fsd=fsd1, anchor=/mnt/nfs, depth=2, width=5, files=100, size=1G

# ✅ 绕过缓存 — 测得 NFS 存储的真实远程 I/O 性能
fsd=fsd1, anchor=/mnt/nfs, depth=2, width=5, files=100, size=1G, openflags=directio
```

### 什么时候可以不用 o_direct？

| 场景 | 是否需要 o_direct | 原因 |
|------|:---:|------|
| **磁盘 / 存储性能基准测试** | ✅ 必须 | 目的是测磁盘，不是测内存 |
| **数据库 OLTP 负载模拟** | ✅ 必须 | 数据库自己管理缓存，OS 缓存是干扰 |
| **NFS / 网络存储测试** | ✅ 必须 | 客户端缓存会严重虚高结果 |
| **排查存储性能问题** | ✅ 必须 | 排除缓存变量才能定位瓶颈 |
| **测试"应用层感受到的缓存收益"** | ❌ 可以不用 | 此时你想测的就是缓存加速效果 |
| **纯缓存命中率测试** | ❌ 可以不用 | 测试目的本身就是缓存 |

> **一句话总结**：除非你明确知道自己在测试缓存的效果，否则一律加 `openflags=o_direct`（块设备）或 `openflags=directio`（文件系统）。

### 实际效果对比

以一个典型的 SSD 为例，同一设备在有无 `o_direct` 下的差异：

| 指标 | 无 o_direct（缓存） | 有 o_direct（直通） | 差异 |
|------|:---:|:---:|:---:|
| 4K 随机读 IOPS | 500,000+ | 80,000~150,000 | **3~6 倍差异** |
| 4K 随机写 IOPS | 300,000+ | 40,000~100,000 | **3~8 倍差异** |
| 平均延迟 | 0.05~0.1ms | 0.2~0.5ms | **2~10 倍差异** |

这就是为什么不加 `o_direct` 的测试结果基本等于"自欺欺人"。

---

## 五、核心参数详解

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
| `journal` | 数据校验日志路径（需提前手动创建该目录） | `/root/jn`, `E:\vdbench_jn` |

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
| `journal` | 数据校验日志路径（需提前手动创建该目录） | `/root/jn`, `E:\vdbench_jn` |
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

## 六、典型测试场景模板

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

## 七、测试结果解读

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

## 八、使用技巧与最佳实践

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

## 九、高级功能使用教程

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

Vdbench 内置了 IO 级别的数据校验机制，核心目标是**检测存储系统的静默数据损坏（Silent Data Corruption）**——位翻转、写错位、元数据错误等，这是业界最难发现、最危险的存储故障类型。

#### 校验原理：512 字节扇区签名机制

Vdbench 以 **512 字节为一个扇区单元**对写入数据做结构化签名，**不管你的 IO 块大小是 4K、1M 还是更大，都会按 512 字节逐扇区嵌入校验元数据**：

```
┌────────────────────────────────────────────────┐
│              每个 512 字节扇区嵌入：               │
│                                                  │
│  ┌──────────────────────┬────────────────────┐  │
│  │  8 字节 LBA           │  1 字节 写入序号密钥   │  │
│  │  (Logical Byte Addr)  │  (Validation Key)   │  │
│  └──────────────────────┴────────────────────┘  │
│                                                  │
│  LBA：标记该扇区所属的块偏移地址                     │
│        → 检测「写错位、数据块张冠李戴」               │
│                                                  │
│  Validation Key：标记该块的写入次数（0~126 循环）    │
│        → 检测「覆盖写丢失、旧数据残留」               │
└────────────────────────────────────────────────┘
```

**校验工作流程**：

```
┌───────────────────────────────────────────────────────┐
│                    写入阶段                             │
│                                                        │
│  生成预期签名 → 记录到校验映射表 → 嵌入扇区 → 写入磁盘     │
│                                                        │
├───────────────────────────────────────────────────────┤
│                    读取 / 校验阶段                      │
│                                                        │
│  读取磁盘数据 → 解析扇区中 LBA + Key → 与映射表对比      │
│                                                        │
│  匹配 → ✓ 通过    不匹配 → ✗ data_error，输出位置和值    │
└───────────────────────────────────────────────────────┘
```

> **通俗理解**：Vdbench 在数据里嵌入了"门牌号"（LBA）和"第几次装修"（Key），读回来时逐一核对——地址错了还是数据旧了，一秒定位。

#### 两类校验存储模式

校验映射表有两种存储方式：

| 模式 | 参数 | 存储位置 | 特点 | 适用场景 |
|------|:---:|------|------|----------|
| **内存模式** | `-v` | 仅内存 | 速度快、无磁盘开销；进程退出即失效，无法跨运行校验 | 短时间快速校验 |
| **日志模式** | `-j` / `-jn` / `-jr` / `-jro` | 磁盘 Journal 文件 | 持久化，支持跨运行、故障后恢复校验 | **可靠性测试，主流推荐** |

#### 关键参数详解

| 参数 | 模式 | 日志持久化 | 是否运行业务 IO | 核心用途 |
|------|:---:|:---:|:---:|------|
| `-v` | 内存校验 | 否 | 是 | 短时间快速校验，进程退出即失效 |
| `-j` | 同步 Journal | 是（同步写） | 是 | 严格可靠性校验，性能损耗大 |
| **`-jn`** | 异步 Journal | 是（异步写） | 是 | **兼顾性能与可靠性，主流推荐** |
| `-jr` | 恢复日志 + 续跑 | 是 | 是 | 故障后恢复测试，续跑并校验 |
| **`-jro`** | 仅恢复日志校验 | 是 | **否** | **纯只读校验，不新增 IO 负载** |

**`-jn` 详解**（Journal No-wait）：

- 日志文件**异步写入**，不等待刷盘就继续下发业务 IO，几乎不拖慢压测性能。
- 极端情况（进程强杀、主机瞬间断电）下可能丢失极少量最新日志，正常停止时日志会完整刷盘。
- **绝大多数需要 Journal 校验的场景，优先用 `-jn` 替代 `-j`**。

**`-jro` 详解**（Journal Recover Only）：

- 加载已有 Journal 日志，**只执行全量只读校验，不发起任何新的读写 IO**。
- 与 `-jr` 的区别：`-jr` 恢复后继续跑业务负载，`-jro` 恢复后只校验，不新增 IO。
- 典型场景：
  - 上一轮 `-jn` 跑完写压力后，单独执行只读全量校验；
  - 存储断电/故障/重启后，加载历史 Journal 验证数据是否损坏；
  - 多轮压测间隙快速校验，不干扰性能指标。

#### 完整使用流程

> **⚠️ 关键前提**：使用数据校验时，**SD/FSD 必须配置 `journal` 参数**指定校验日志目录，且**该目录必须提前手动创建**，否则 Vdbench 无法写入校验日志，校验会失败。

**第一步：创建 Journal 目录**

```bash
# Linux
mkdir -p /root/jn

# Windows（PowerShell）
mkdir E:\vdbench_jn
```

**第二步：写入数据并生成校验日志**

块设备示例 `write_verify.par`：

```bash
messagescan=no

sd=sd1, lun=/dev/vdb, openflags=o_direct, size=100G, journal=/root/jn

wd=wd_write, sd=sd1, rdpct=0, seekpct=0, xfersize=4k, threads=32

rd=rd1, wd=wd_write, iorate=max, elapsed=600, interval=5
```

文件系统示例 `write_verify_file.par`：

```bash
messagescan=no

fsd=fsd1, anchor=/mnt/test, depth=2, width=5, files=100, size=1G, openflags=directio, journal=/root/jn

fwd=fwd1, fsd=fsd1, operation=write, fileio=sequential, xfersize=1M, threads=16

rd=rd1, fwd=fwd1, fwdrate=max, format=yes, elapsed=600, interval=5
```

执行写入（带校验日志）：

```bash
# Linux
./vdbench -f write_verify.par -jn -o output_write

# Windows
vdbench.bat -f write_verify.par -jn -o output_write
```

**第三步：纯只读校验（推荐用 `-jro`）**

> **⚠️ 关键**：`-jro` 是只读校验，不产生新 IO，**`format` 必须设为 `no`**，否则会格式化掉预埋的数据！与第二步写入时的 `format=yes`/`restart` 不同，建议用同名配置复制一份校验专用 par 文件，将 `format` 改为 `no`：

校验专用配置文件 `verify_only.par`（基于写入配置文件，仅改 `format=no`）：

```bash
messagescan=no

fsd=fsd1, anchor=/mnt/test, depth=2, width=5, files=100, size=1G, openflags=directio, journal=/root/jn

fwd=fwd1, fsd=fsd1, operation=write, fileio=sequential, xfersize=1M, threads=16

rd=rd1, fwd=fwd1, fwdrate=max, format=no, elapsed=600, interval=5
```

执行校验：

```bash
# Linux — 只校验，不打 IO
./vdbench -f verify_only.par -jro -o output_verify

# Windows
vdbench.bat -f verify_only.par -jro -o output_verify
```

**第四步：解读校验结果**

校验通过：

```
Data Validation: all blocks OK
No data validation errors detected.
```

校验失败时会输出具体错误的 LBA、偏移、预期值和实际值，可直接定位损坏位置：

| 错误类型 | 说明 | 可能原因 |
|----------|------|---------|
| **LBA mismatch** | 地址错乱，数据写到了错误位置 | 存储固件 bug、多路径混乱 |
| **Key mismatch** | 写入序号不匹配，读到旧数据 | 覆盖写丢失、快照回滚不当 |
| **Content error** | 数据内容损坏 | 磁盘坏块、RAID 故障、内存 bit-flip |

#### 实战注意事项

1. **SD/FSD 必须配置 `journal` 且提前创建目录**：无论块设备还是文件系统模式，使用校验功能都必须在 `sd`/`fsd` 中指定 `journal=/path/to/jn`，且该目录必须 `mkdir -p` 预先创建好。缺少该参数或目录不存在，校验日志写入失败。
2. **优先用 `-jn`**：兼顾性能与可靠性，绝大多数场景足以胜任；对数据安全要求极致严格时再用 `-j`。
3. **校验完用 `-jro`**：压测结束后单独跑 `-jro` 做全量校验，不打额外 IO，不影响性能指标准确性。
4. **Journal 文件大小**：日志文件与测试数据量正相关，大容量测试需预留足够本地磁盘空间。
5. **配置文件不变原则（参数级别）**：写入和校验使用同一份 `sd`/`fsd` 定义和 `size`，改动这些会导致校验签名不匹配。但 `format` 参数必须区分：写入阶段用 `yes`/`restart`，`-jro` 校验阶段用 `no`，建议复制一份配置文件单独改为 `format=no`。
6. **RoCE / 分布式存储场景**：推荐 `-jn` 异步模式避免日志同步写拖慢链路性能；校验阶段用 `-jro` 离线执行。
7. **校验 ≠ 性能测试**：开启校验会增加 CPU 开销（签名计算与比对），建议流程："`-jn` 写数据 → 关校验测性能 → `-jro` 验数据"。

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

## 十、常见问题与解决方案

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

## 十一、总结

Vdbench 是一款功能强大、灵活度高的企业级存储测试工具。通过合理配置参数，可以模拟各种真实的业务负载，全面评估存储系统的性能和可靠性。

### 核心要点回顾

1. **`openflags=o_direct` / `directio` 是第一铁律**：不加缓存绕过的测试结果等于自欺欺人。除非你明确在测试缓存效果，否则一律绕缓存。
2. **块设备 vs 文件系统**：块设备测的是"磁盘能跑多快"，文件系统测的是"应用在文件系统上能跑多快"。两者回答的问题不同，不可互相替代。
3. **数据校验不可忽视**：性能测试只能告诉你"有多快"，数据校验才能告诉你"有多可靠"。静默数据损坏是存储领域最危险的隐形杀手。
4. **Linux / Windows 脚本关注点**：本质都是 Java 程序，差异只在启动脚本（`vdbench` vs `vdbench.bat`）、设备路径格式和依赖（Linux 需要 `csh`）。

### 使用建议

1. 从简单的单线程顺序读写开始，逐步增加复杂度
2. 每次只改变一个参数，便于分析参数对性能的影响
3. 多次运行测试，取平均值以减少误差
4. 结合其他工具（如 `iostat`、`nmon`、`perfmon`）进行全方位监控
5. 测试完成后，详细记录测试环境和参数，便于后续对比分析

---

> **声明**：本文基于 Vdbench 5.04.06 官方文档编写，旨在提供中文操作指南。具体参数请以官方 `vdbench.pdf` 为准。

# iostat 磁盘 IO 性能监控与瓶颈分析实战：从字段解读到优化落地

---

## 一、iostat 命令基础

`iostat` 是 Linux `sysstat` 工具包中的磁盘 IO 监控命令，用于实时查看块设备的读写负载、延迟和吞吐量。

### 1.1 安装

```bash
# Debian/Ubuntu
apt install sysstat

# RHEL/CentOS
yum install sysstat
```

### 1.2 常用参数组合

```bash
# 基础用法：每秒输出一次，共输出 5 次
iostat 1 5

# 推荐用法：显示扩展指标 + 单位 MB + 时间戳，每秒刷新
iostat -xmt 1
```

| 参数 | 含义 |
|------|------|
| `-x` | 显示扩展统计信息（包含 `await`、`%util`、`aqu-sz` 等关键字段） |
| `-m` | 吞吐量以 MB/s 显示（默认是 KB，数据量大时不便阅读） |
| `-t` | 每条输出带时间戳，方便事后对照日志排查 |
| `-d` | 只显示磁盘设备统计（不显示 CPU 行） |
| `-p` | 指定磁盘设备，如 `iostat -xmt -p nvme0n1 1` |
| `-k` | 以 KB/s 显示（默认） |
| `1` | 采样间隔 1 秒 |
| `5` | 共采样 5 次，不写则持续输出 |

### 1.3 输出结构

`iostat -xmt 1` 输出分为两部分：

```
第一部分：avg-cpu 行 → 整体 CPU 使用率分布
第二部分：Device 行  → 每块磁盘的 IO 详细指标
```

`avg-cpu` 各列含义：

| 字段 | 含义 |
|------|------|
| `%user` | 用户态 CPU 占用 |
| `%system` | 内核态 CPU 占用 |
| `%iowait` | CPU 空闲 + 有未完成 IO 请求的时间占比 |
| `%idle` | CPU 完全空闲占比 |

---

## 二、Device 行核心字段详解

`iostat -x` 输出的 Device 行字段最多，以下按排查优先级从高到低排列。

### 2.1 负载类指标（回答"盘在干什么"）

| 字段 | 含义 | 评判要点 |
|------|------|---------|
| `r/s` | 每秒读请求数（读 IOPS） | 配合 `w/s` 判断业务读写比例。值越高 IOPS 压力越大，但没有固定阈值，需要跟 fio 压测基线对比 |
| `w/s` | 每秒写请求数（写 IOPS） | 同上。如果 `w/s` 远大于 `r/s`，业务偏写入密集型 |
| `rMB/s` | 每秒读取数据量（读带宽） | 参考磁盘标称带宽。NVMe Gen4 单盘读上限约 7000MB/s，Gen3 约 3500MB/s，SATA SSD 约 550MB/s，HDD 约 150MB/s |
| `wMB/s` | 每秒写入数据量（写带宽） | 同上。持续接近硬件上限说明带宽瓶颈，否则更多是 IOPS 瓶颈 |
| `rkB/s` / `wkB/s` | 每秒读写 KB 数 | `-m` 参数下显示为 `rMB/s` / `wMB/s`，两者二选一 |

**带宽和 IOPS 的关系：**

```
平均 IO 大小 = 带宽 / IOPS

示例：
rMB/s = 50MB/s，r/s = 13000
平均读 IO 大小 = 50 * 1024 / 13000 ≈ 4KB
```

如果平均 IO 大小很小（<16KB），说明大量随机小 IO——这是最常见的 IOPS 杀手。

### 2.2 延迟类指标（回答"盘响应快不快"）

| 字段 | 含义 | 评判要点 |
|------|------|---------|
| `r_await` | 读请求平均等待时间（ms） | **核心指标。** 包含排队等待 + 硬件处理。NVMe 空闲时 <0.1ms，SATA SSD <0.5ms，HDD <5ms。持续上升说明排队加重 |
| `w_await` | 写请求平均等待时间（ms） | **核心指标。** 同上。注意：写入受 page cache 影响，`direct=1` 的 IO 更能反映真实延迟 |
| `await` | 读写请求平均等待时间（合并值） | 不如 `r_await` / `w_await` 有区分度，但可用于快速扫一眼 |

**延迟判断经验值（NVMe 设备）：**

| `await` 范围 | 状态 | 说明 |
|-------------|------|------|
| < 0.2ms | 正常 | 设备空闲或轻载 |
| 0.2 ~ 1ms | 轻度排队 | IO 请求开始积压 |
| 1 ~ 5ms | 明显瓶颈 | 需要排查原因 |
| > 5ms | 严重瓶颈 | 应用层已能感知卡顿，必须立即处理 |

### 2.3 饱和度指标（回答"盘扛不扛得住"）

| 字段 | 含义 | 评判要点 |
|------|------|---------|
| `aqu-sz` | 平均 IO 队列长度 | **最值得盯的指标之一。** 值表示平均有多少 IO 请求在排队。NVMe 空闲时为 0，持续 >1 说明有稳定积压，>5 严重拥堵 |
| `%util` | 磁盘繁忙时间占比 | 传统指标，在 SSD/NVMe 上有局限（见下文）。HDD 接近 100% 是硬瓶颈，NVMe 需要结合 `await` 和 `aqu-sz` 综合判断 |
| `svctm` | 平均每次 IO 硬件服务时间（ms） | **man iostat 明确标注不可靠，不应用于性能分析。** 需要准确的设备级服务时间请使用 blktrace + btt |
| `avgqu-sz` | 平均 IO 队列长度（含正在处理和排队的请求） | 与 `aqu-sz` 含义相近，不同版本 sysstat 命名可能不同 |
| `wareq-sz` / `rareq-sz` | 平均每次读写 IO 大小（KB） | 反映 IO 模式：值小（<16KB）= 随机小 IO，值大（>128KB）= 顺序大 IO |

### 2.4 %util 的局限性（重要）

**传统理解：** `%util` 是磁盘繁忙时间占比，接近 100% = 磁盘打满了。

**实际在 NVMe/SSD 上的表现：**

- 机械盘：单队列处理，`%util` 直接反映是否满负载，准确
- SATA SSD：支持 NCQ（Native Command Queuing），队列深度通常 32，`%util` 仍然有一定参考价值
- NVMe：支持多队列并行（最多 64K 个独立队列），内核统计 `%util` 只看"设备有没有 IO 在飞"，大量并发小 IO 可以轻松把 util 打到 100%，但此时的带宽利用率可能不到 10%

**正确的 NVMe 瓶颈判定方法：三个条件同时满足：**

1. `%util` 持续 ≈ 100%
2. `await`（尤其是 `w_await`）持续上升
3. `aqu-sz` 持续 > 1 且趋势增长

只满足第一个条件的情况，磁盘只是"正在工作"，不等于"达到极限"。三个都满足才是真正的硬件瓶颈。

---

## 三、实战：一份大压力 iostat 数据的逐字段分析

以下结合一份 4 块 NVMe 磁盘高负载场景的 iostat 数据进行逐字段解读。

> 截图场景：服务器配置 4 块 NVMe 磁盘（nvme4n1 / nvme0n1 / nvme2n1 / nvme3n1），外加一块 SATA 系统盘 sda。连续多次采样，四块 NVMe 盘 `%util` 均接近 100%。

### 3.1 CPU 行分析

```text
avg-cpu:  %user   %nice   %system   %iowait   %steal   %idle
           12.45   0.00     8.32     0.11      0.00    79.12
```

| 字段 | 值 | 判断 |
|------|-----|------|
| `%iowait` | 0.11% | **极低。** 在没有阻塞 IO 或 CPU 持续繁忙的场景下，iowait 不具备指示磁盘压力的能力 |
| `%idle` | 79.12% | CPU 大量空闲，说明瓶颈不在计算层 |
| `%system` | 8.32% | 内核态占用偏高，跟大量 IO 系统调用有关 |

**关键结论：** CPU 空闲充足但 iowait 极低，说明业务进程采用的是异步 IO 模型（`libaio` 或 `io_uring`），发完 IO 请求不阻塞等待，CPU 切去干别的事。这种场景下 **iowait 完全不能反映磁盘压力**。

### 3.2 四块 NVMe 盘汇总指标

| 指标 | 数值范围 | 分析 |
|------|---------|------|
| 总读 IOPS（r/s） | 10000 ~ 13000 | 每秒一万多次读请求 |
| 总写 IOPS（w/s） | 14000 ~ 18000 | 写请求比读更多，写密集型负载 |
| 读带宽（rMB/s） | 40 ~ 55 MB/s | 远未达到 NVMe 带宽上限 |
| 写带宽（wMB/s） | 140 ~ 240 MB/s | 同上 |

**IO 模式判断：**

```
平均 IO 大小 ≈ 55MB / 13000 IOPS ≈ 4KB
```

典型的小随机 IO 模式，每秒发出极高数量的 IO 请求，但每次请求的数据量非常小。这类负载 IOPS 先行触及瓶颈，而带宽远有余量。

### 3.3 延迟与饱和度

```text
r_await ≈ 0.09ms
w_await ≈ 0.15 ~ 0.26ms
aqu-sz   ≈ 1.5 ~ 2.7
%util    ≈ 100%
```

逐个解读：

- **`r_await = 0.09ms`：** NVMe 的正常延迟范围，读请求尚未出现明显排队。
- **`w_await = 0.15~0.26ms`：** 写延迟略高于读，可能与写请求更多有关（`w/s` > `r/s`），但数值本身仍处于可接受范围。
- **`aqu-sz = 1.5~2.7`：** 队列长度稳定、持续存在。说明 IO 请求到达速度略高于处理速度，已形成稳定的轻度积压。**这是"刚好顶住"的状态——再增加 20%~30% 负载，await 可能从 0.2ms 级别快速跳到 1ms 级别。**
- **`%util = 100%`：** 四块盘全部持续满载，配合 `aqu-sz > 1`，确认磁盘侧确实是当前系统的瓶颈。

**综合判断：** 磁盘 IO 已饱和，处于临界状态。当前延迟尚可接受，但容量已经见顶，继续增加负载会导致延迟快速恶化。

### 3.4 sda（SATA 系统盘）忽略

sda 的 `%util` 极低，说明根文件系统和系统日志没有大量 IO 活动，瓶颈集中在四块 NVMe 业务盘。

---

## 四、进程级定位：找到 IO 来源

iostat 告诉你"磁盘压力大"，下一步需要知道"谁在产生压力"。

### 4.1 定位进程

```bash
# iotop：交互式显示进程 IO 排行（需要 root）
iotop -oP

# pidstat：非交互式，适合脚本采集
pidstat -d 1
```

输出示例：

```text
PID      kB_rd/s   kB_wr/s   kB_ccwr/s  Command
18245    0         45236     0          java
9211     1240      320       0          mysqld
```

关注点：
- `kB_rd/s` 和 `kB_wr/s` 最高的进程
- 是否是你预期的业务进程？如果出来一个不在预期范围内的进程，排查优先级立刻提高
- 同一进程号的 IO 量是否跟业务 QPS 正相关（高峰期高、低峰期低）？

### 4.2 定位文件

```bash
# 查看进程打开了哪些文件
lsof -p <PID> | grep -E 'REG|DIR'

# 抓系统调用统计，看具体在读写什么
strace -p <PID> -e trace=read,write,pread,pwrite,readv,writev -c
```

`strace -c` 输出会统计各系统调用的次数和耗时，快速定位 IO 热点。

### 4.3 深入：块设备层分析

iostat 给的是汇总数据，如果想看每次 IO 在块设备层的完整生命周期，需要使用 blktrace：

```bash
# 抓取 30 秒
blktrace -d /dev/nvme0n1 -o trace_output

# 解析
blkparse -i trace_output -d parsed.bin

# 统计分析
btt -i parsed.bin -l nvme0n1_latency.txt
```

`btt` 输出中的关键字段：

| 字段 | 含义 | 用途 |
|------|------|------|
| Q2C | 从 IO 入队到完成的总时间 | 最接近应用感知延迟 |
| Q2G | IO 在队列中等待的时间 | 排队占比：Q2G/Q2C 高 = 主要瓶颈在排队 |
| D2C | NVMe 硬件本身的服务时间 | NVMe 正常 < 0.1ms，高了考虑硬件问题 |

典型判断：如果 Q2G 占 Q2C 的 70% 以上，瓶颈在 IO 调度和排队（软件侧）；如果 D2C 占比高，考虑磁盘硬件或驱动问题。

---

## 五、性能优化思路与方案

### 5.1 优化前先分类：正常负载 vs 异常负载

确认 iostat 数据和进程来源后，判断负载性质：

| 特征 | 属于 | 优化思路 |
|------|------|---------|
| IO 量与业务 QPS 正相关、无突刺 | 正常业务负载 | 优化 IO 模式、扩容 |
| IO 量跟业务无关、周期尖刺 | 异常行为 | 定位根因、修 bug/调配置 |

### 5.2 正常业务负载的优化方案

**方案一：减少 IO 次数（批量化）**

大量小 IO 是 IOPS 的最大杀手。把多次小 IO 合并为一次大 IO，效果立竿见影。

```text
改前：每次写 1 行日志就 flush → 每秒 2000 次 write
改后：攒到 64KB 再批量写入   → 每秒 30 次 write
IOPS 降幅：~98%
```

适用场景：
- 日志框架配置（Log4j2 的 `immediateFlush=false` + `bufferSize`）
- 数据库批量操作（insert batch size）
- 消息队列的批量提交

**方案二：调整 IO 调度器**

```bash
# 查看当前调度器
cat /sys/block/nvme0n1/queue/scheduler

# NVMe 设备推荐 none（内核旁路，由硬件自己调度）
echo none > /sys/block/nvme0n1/queue/scheduler
```

NVMe 设备的内核 IO 调度器几乎不发挥作用，设置为 `none`（或 `mq-deadline`）减少不必要的内核开销。

**方案三：脏页参数调优**

```bash
# 查看当前值
sysctl vm.dirty_ratio vm.dirty_background_ratio vm.dirty_expire_centisecs

# 大内存服务器可适当调小，让刷盘更分散
# 注意：调太小会导致频繁刷盘，小 IO 反而增多
# 建议在测试环境验证后再上线
```

| 参数 | 默认值 | 调优建议 |
|------|--------|---------|
| `vm.dirty_background_ratio` | 10% | 内存 ≥ 64G 时可降至 5% |
| `vm.dirty_ratio` | 20% | 保持与 dirty_background_ratio 2~3 倍关系 |
| `vm.dirty_expire_centisecs` | 3000（30s） | 有 UPS 的服务器可适当增大，减少刷盘频率 |

**方案四：业务拆分 / 磁盘扩容**

如果以上优化后 IOPS 仍处于 70%~80% 基线，考虑：
- 将不同业务的 IO 拆分到不同磁盘组，避免互相干扰
- 增加磁盘数量，使用 RAID0 或 JBOD 分摊 IOPS
- 日志、数据库、临时文件使用不同的物理盘

### 5.3 异常负载的排查思路

**元凶一：脏页回写风暴**

现象：`w/s` 突然飙升，与业务正常写量不匹配。

```bash
# 实时查看脏页量
watch -n 1 'grep -E "Dirty|Writeback" /proc/meminfo'
```

如果 `Dirty` 值持续在 dirty_ratio 阈值附近波动，说明系统在频繁触发大规模回写。

**元凶二：日志框架逐行刷盘**

现象：大量 4KB 以下的 `write` 系统调用。

```bash
# 确认进程的 write 调用频率和大小
strace -e write -p <PID> 2>&1 | head -100
```

**元凶三：定时任务 / 备份 / 快照**

```bash
# 列出所有定时任务
crontab -l
ls /etc/cron.*

# systemd 定时器
systemctl list-timers --all
```

**元凶四：数据库 checkpoint 或 autovacuum**

```bash
# MySQL
SHOW ENGINE INNODB STATUS\G

# PostgreSQL
SELECT * FROM pg_stat_progress_vacuum;
```

### 5.4 fio 基线压测：量化磁盘极限

在扩容或优化决策之前，需要知道磁盘的极限在哪，避免盲目操作。

```bash
# 4KB 随机读 IOPS 极限（适合模拟数据库查询场景）
fio --name=randread \
    --ioengine=libaio \
    --iodepth=32 \
    --rw=randread \
    --bs=4k \
    --direct=1 \
    --size=4G \
    --numjobs=4 \
    --runtime=60 \
    --group_reporting \
    --filename=/dev/nvme0n1

# 4KB 随机写 IOPS 极限
fio --name=randwrite \
    --ioengine=libaio \
    --iodepth=32 \
    --rw=randwrite \
    --bs=4k \
    --direct=1 \
    --size=4G \
    --numjobs=4 \
    --runtime=60 \
    --group_reporting \
    --filename=/dev/nvme0n1
```

> ⚠️ 随机写测试会覆盖数据，不要在有数据的盘上直接跑 `/dev/nvme0n1`，用测试文件路径替代。

跑完后读结果：

```text
read: IOPS=450k, BW=1760MiB/s (1846MB/s)
```

把这个 IOPS 值作为**极限基线**。当线上 iostat 显示的 IOPS 达到基线的 70%~80% 时，启动扩容评估；达到 90% 以上时，延迟已经开始恶化，需要立即行动。

---

## 六、常见误区

**误区 1：NVMe 设备 %util=100% 就是带宽打满了**

NVMe 多队列并行架构下，大量小随机 IO 可以打满 util 但带宽占比极低。判断瓶颈需要 `%util` + `await` + `aqu-sz` 三者一起看。

**误区 2：iowait 低说明磁盘没压力**

当业务使用异步 IO（`libaio` / `io_uring`）或 CPU 一直有活干时，iowait 不会升高。本文的实战数据 `iowait=0.11%`、`%util=100%` 就是最好的反例。

**误区 3：await 低就表示没问题**

本文数据中 `r_await=0.09ms`，但 `aqu-sz=2.7` 表明队列已经稳定存在。排队曲线是非线性的——当请求量超过服务能力的临界点，await 会从 0.1ms 级瞬间跳到 ms 级。关注 `aqu-sz` 的趋势比关注 `await` 的当前值更有预判价值。

**误区 4：直接用 iostat 的 svctm 做性能分析**

`man iostat` 明确说明 `svctm` 字段不可靠，不要用于性能评估。真实的服务时间应使用 `blktrace + btt`。

**误区 5：IO 压力大时 drop_caches**

```bash
# 不推荐在 IO 压力大时执行
echo 3 > /proc/sys/vm/drop_caches
```

这会清空 page cache，导致后续读请求全部穿透到磁盘，IO 负载瞬间翻倍。

---

## 七、排查路径速查

| 步骤 | 命令 | 关注点 |
|------|------|--------|
| 1. 确认瓶颈层 | `iostat -xmt 1` | `%util`、`await`、`aqu-sz` 三个一起看；`r/s` + `w/s` + 带宽算 IO 大小 |
| 2. 定位进程 | `iotop -oP` 或 `pidstat -d 1` | IO 量最高的进程是否预期内 |
| 3. 定位文件 | `lsof -p PID` / `strace -e trace=file -c -p PID` | 具体在读/写什么文件 |
| 4. 深度分析 | `blktrace + btt` | Q2G/Q2C 比例判断瓶颈在排队还是硬件 |
| 5. 判断性质 | 对比业务 QPS、crontab、脏页量 | 正常负载还是异常行为 |
| 6. 建立基线 | `fio` 随机读写压测 | 知道磁盘 IOPS/带宽上限 |
| 7. 执行优化 | 批量 IO / 调内核参数 / 拆盘 / 扩容 | 对症下药 |

---

## 八、总结

`iostat` 是磁盘 IO 排查的入口工具，但解读逻辑在 NVMe 时代已经和机械盘时代完全不同。核心原则：

1. **不用孤立的指标判断瓶颈**——`%util`、`await`、`aqu-sz` 三个一起看，缺一不可
2. **算 IO 大小**——带宽 / IOPS，判断是 IOPS 瓶颈还是带宽瓶颈
3. **先区分正常负载和异常负载**——优化方案完全不同
4. **建立 fio 基线**——没有基线，看到的 IOPS 就是个数字，不知道盘还能扛多少
5. **iowait 低不代表磁盘没事**——异步 IO 模型下 iowait 与磁盘压力的相关性很弱

---

> **关键词：** iostat 命令详解、Linux 磁盘 IO 监控、NVMe 性能分析、%util await aqu-sz、iotop pidstat 进程 IO 排查、blktrace 块设备分析、fio 磁盘压测、脏页优化、IO 瓶颈排查

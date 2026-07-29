# 存储协议 05 — 网络篇：千兆/万兆/RDMA/RoCE/IB/Bond 怎么选

> 存储性能的瓶颈已经从磁盘转移到了网络。一块 NVMe SSD 顺序读轻松 7GB/s，但如果你还用千兆网卡连存储，实际到手 125MB/s，SSD 90% 的性能被你浪费了。这篇把存储网络相关的网卡速率、RDMA 原理、RoCE vs InfiniBand、以及 Bond 多网卡捆绑一次性讲透。

---

## 一、为什么存储离不开网络

存储系统不是一块盘挂在服务器主板上就结束了。但凡你用过 NFS 共享目录、iSCSI 块存储、或者 Ceph 集群，数据都得先穿过网络，才能从存储端到达你的服务器。

一张简化链路：

```
应用读写 → 文件系统/SCSI层 → 存储协议 → 网络协议栈 → 网卡 → 交换机 → 存储
```

当你用千兆网卡连全闪存阵列的时候，问题就来了：**盘的速度是网络的 50 倍**。网络成了木桶最短的那块板。

| 存储介质 | 顺序读吞吐 | 对比千兆网（125MB/s） | 对比万兆网（1.25GB/s） |
|---------|-----------|---------------------|----------------------|
| SATA SSD | ~550MB/s | 网络是瓶颈（差 4 倍） | 够用 |
| NVMe SSD Gen3 | ~3.5GB/s | 网络是瓶颈（差 28 倍） | 网络是瓶颈（差 3 倍） |
| NVMe SSD Gen5 | ~14GB/s | 网络是瓶颈（差 112 倍） | 网络是瓶颈（差 11 倍） |

所以搞存储的人，迟早得搞网络。下面从最基础的网卡速率讲起，一路讲到 RDMA 和 Bond。

---

## 二、网卡速率分级：从千兆到 400G

### 2.1 各速率一览

| 速率 | 理论带宽 | 线速吞吐(单向) | 存储场景定位 |
|------|---------|---------------|-------------|
| 1GbE（千兆） | 1 Gbps | ~125 MB/s | 管理网络、备份归档、小规模 NFS |
| 10GbE（万兆） | 10 Gbps | ~1.25 GB/s | iSCSI 中小规模、NFS 通用场景 |
| 25GbE | 25 Gbps | ~3.1 GB/s | 单节点全闪存储接入、Ceph OSD |
| 40GbE | 40 Gbps | ~5 GB/s | QSFP+ 时代产物，正被 50/100G 替代 |
| 50GbE | 50 Gbps | ~6.25 GB/s | NVMe-oF 入门、分布式存储后端 |
| 100GbE | 100 Gbps | ~12.5 GB/s | 当前主流高性能存储网络 |
| 200GbE | 200 Gbps | ~25 GB/s | AI 训练集群、HPC |
| 400GbE | 400 Gbps | ~50 GB/s | 超大规模 AI/HPC 互连 |

**带宽和吞吐不是一回事**。1 Gbps 除以 8 是 125 MB/s，再扣掉 TCP 头开销、帧间隙、流控开销，实际可用大概 115-118 MB/s。到 100G 级别，协议开销吃掉 3%-5% 不奇怪。

### 2.2 存储流量看的不只是带宽

存储网络和 Web 流量最大的区别在于，它要求的是**三个指标同时达标**：

1. **吞吐（Throughput）**：大块顺序读写能跑满带宽，这考验的是带宽本身
2. **IOPS（小包转发率）**：数据库随机 4K 读写，一秒几十万个小包，考验的是网卡 PPS（Packet Per Second）
3. **尾延迟（P99/P999 Tail Latency）**：分布式存储一个写请求可能拆成多个子请求同时发给不同节点，只要最慢的那个没回来，整个请求就被挂着。所以**平均延迟没意义，尾延迟才是天花板**

一个 10GbE 网卡跑 4K 随机读，PPS 大概能到 300K，如果换成 25GbE，同样的包大小 PPS 能翻 2.5 倍。这就是为什么分布式存储后端通常用 25G+ 而不是 10G——不一定是带宽不够，是 IOPS 撑不住。

---

## 三、TCP/IP 协议栈：存储网络的天花板

Linux 内核网络协议栈是为通用性设计的，放在存储场景里，有三个核心开销：

### 3.1 三个致命开销

**上下文切换**：数据从网卡到达，触发硬中断 → 软中断（ksoftirqd）→ 内核协议栈处理 → 拷贝到用户态 buffer → 唤醒应用进程。一路下来至少两次上下文切换。

**数据拷贝**：网卡 DMA → 内核 socket buffer → 用户态 buffer。如果要写盘，还有用户态 → 内核 block layer → 驱动 → 磁盘。一份数据在内存里搬了三四次。

**中断风暴**：高 IOPS 场景下，每秒几十万个中断。每个中断都在抢 CPU 时间——你的 CPU 不是在处理存储数据，而是在处理"该怎么处理存储数据"这件事。

### 3.2 万兆以上的 CPU 困境

实测数据（来源公开社区测试，非精确值，仅供参考数量级）：

| 网络速率 | 纯 TCP 吞吐 | CPU 占用（单核） | 问题 |
|---------|------------|----------------|------|
| 10GbE | ~9.4 Gbps | ~30-40% | 可接受 |
| 25GbE | ~23 Gbps | ~60-70% | 一核勉强，多流需要 RSS 多队列 |
| 40GbE | ~35 Gbps | ~80-90% | 一核基本跑不满 |
| 100GbE | ~55-70 Gbps（单流） | 一核打满 | **单流跑不满线速** |

到了 25GbE 以上，TCP 协议栈本身就成了瓶颈——不是网卡不够快，是 Linux 内核处理不过来。这就是 RDMA 存在的意义。

---

## 四、RDMA：让网卡绕开 CPU 直接读写内存

### 4.1 RDMA 的三个核心能力

RDMA（Remote Direct Memory Access）做的事情一句话：**让一台服务器的网卡直接把数据写到另一台服务器的内存里，CPU 和内核全程不参与。**

三个关键词：

| 能力 | 含义 | 存储场景意义 |
|------|------|-------------|
| Kernel Bypass | 数据路径不经过内核协议栈 | 没有上下文切换开销 |
| Zero Copy | 网卡 DMA 直接读写用户态内存 | 数据不用在内核/用户态之间搬 |
| CPU Offload | 协议处理在网卡硬件里完成 | CPU 用来跑业务，不用处理网络 |

### 4.2 两种传输语义：双边 vs 单边

**SEND/RECV（双边）**：跟 TCP 的 send/recv 类似。发送方 SEND，接收方要提前 POST RECV 缓冲区才能接收。接收方 CPU 需要参与，但不需要内核。

**READ/WRITE（单边）**：这才是 RDMA 的杀手锏。发送方可以直接读取或写入远程内存，**远程 CPU 完全不知道这件事发生**。对于存储来说，客户端可以直接 WRITE 数据到存储节点的内存里，存储节点 CPU 该干嘛干嘛。

分布式存储里大量用到单边 RDMA——Ceph 的 OSD 间数据复制、Lustre 的 LNET 传输层、DAOS 的整个 I/O 路径，全在利用单边 WRITE。

### 4.3 延迟对比

| 传输方式 | 端到端延迟 | 说明 |
|---------|-----------|------|
| 10GbE TCP | ~50-100 μs | 内核协议栈开销 |
| 10GbE DPDK | ~10-20 μs | 用户态 TCP，旁路内核 |
| RDMA (RoCE/IB) | ~2-5 μs | 网卡硬件直接处理 |
| 本地 NVMe IO | ~80-100 μs | 包括块层和驱动 |

RDMA 的微秒级延迟意味着：**网络不再是存储延迟的主要贡献者**。以前是"网络慢，盘快"，上了 RDMA 之后是"网络和盘差不多快"。

### 4.4 RDMA 的三条技术路线

RDMA 是一种能力，不是一个协议。实现 RDMA 的网络协议有三种：

| 协议 | 链路层 | IP 路由 | 特点 |
|------|--------|---------|------|
| **InfiniBand（IB）** | IB 自有链路层 | 不支持 | 全栈自闭环，性能最强，专网专用 |
| **RoCE v1** | 以太网（GRH） | 不支持 | 只能在同一广播域内通信 |
| **RoCE v2** | 以太网（UDP/IP） | 支持 | 可跨子网，数据中心主流 RDMA 方案 |
| **iWARP** | 以太网（TCP/IP） | 支持 | 走 TCP，对丢包容忍但性能不如前两种 |

目前数据中心存储的主流选择是 **RoCE v2**。下面分两节分别讲 InfiniBand 和 RoCE。

---

## 五、InfiniBand：HPC 存储网络的王者

### 5.1 IB 是什么

InfiniBand 是完全独立于以太网的一套网络架构。从物理层的光模块、线缆、到链路层的帧格式、到传输层的流控，全部自成体系。**它不管什么 TCP/IP、以太网交换机，整个协议栈从头设计，目标只有一个——极致性能。**

### 5.2 核心机制

**Credit-based 流控（天然无损）**

IB 链路层用 Credit 机制做端到端流控：接收方告诉发送方"我有 X 个 buffer"，发送方发出去的包数不能超过 X。接收方的 buffer 不够了就暂停发 Credit，发送方自然停下来。整个过程**不会丢包，也不需要重传**。

对比以太网：TCP 靠丢包来感知拥塞（丢包后才减速），RoCE 靠 PFC（暂停帧）来防丢包——两者都不如 Credit 机制优雅。

**Virtual Lane（VL，虚拟通道）**

IB 支持最多 15 条虚拟通道（VL0-VL14），每条 VL 独立缓冲、独立流控。存储数据走 VL1，管理流量走 VL0，互不干扰。这在存储层面意味着**控制流量和数据流量不会互相踩踏**。

### 5.3 速率演进

| 代际 | 信号速率 | 单端口吞吐（4x） | 典型部署时间 |
|------|---------|-----------------|-------------|
| FDR | 14 Gbps/lane | 56 Gbps | ~2013 |
| EDR | 25 Gbps/lane | 100 Gbps | ~2016 |
| HDR | 50 Gbps/lane | 200 Gbps | ~2019 |
| NDR | 100 Gbps/lane | 400 Gbps | ~2022 |
| XDR | 200 Gbps/lane | 800 Gbps | 规划中 |

### 5.4 运维代价

IB 有独立的：
- **子网管理器（Subnet Manager，SM）**：相当于以太网的"交换机 + 路由器 + DNS"三位一体，必须在子网内运行，否则整个 IB 网络不可用
- **GUID/MAC 体系**：不是以太网的 MAC 地址
- **诊断工具链**：`ibstat`、`ibstatus`、`ibdiagnet`、`perfquery`、`ibtracert`——全部独立于以太网工具

一个会以太网的网管，面对 IB 网络基本要从头学。

### 5.5 适用场景

- **TOP500 超算**：绝大多数用 IB（或厂商自研高速互联）
- **NVIDIA GPU 集群（NCCL）**：IB 是 NCCL 的原生首选传输层
- **Lustre 后端存储网络**：LLNL、ORNL 等国家实验室的 Lustre 都跑在 IB 上
- **对延迟极端敏感的场景**：微秒级抖动都不能接受

---

## 六、RoCE：以太网上的 RDMA

### 6.1 RoCE v1 vs v2 的区别

| 维度 | RoCE v1 | RoCE v2 |
|------|---------|---------|
| 封装方式 | IB 传输层直接封装在以太网帧里 | IB 传输层封装在 UDP/IP 里 |
| EtherType | 0x8915 | UDP 端口 4791 |
| IP 层 | 无 IP 头 | 有 IP 头 |
| 可路由 | 否（同一二层域） | 是（可跨子网） |
| 当前使用 | 几乎淘汰 | 主流方案 |

一句话：**现在说 RoCE，默认指 RoCE v2**。v1 只在 2010 年代短暂用过。

### 6.2 以太网跑 RDMA 的代价：必须配无损网络

RDMA 假设网络不丢包——丢了包就得重传，重传走 Go-Back-N，性能会断崖式下跌。但以太网天生是"尽力而为"的，拥塞了就丢包。

要让以太网不丢包，得靠 **DCB（Data Center Bridging）** 三件套：

**PFC（Priority Flow Control，IEEE 802.1Qbb）**

按 802.1p 优先级分别做暂停。给 RDMA 流量分配一个优先级（比如 Priority 3），这个队列满了就发 Pause 帧暂时停掉前方的发送，等有空 buffer 了再恢复。其他优先级（比如 TCP 普通流量）不管，照常通。

**ECN（Explicit Congestion Notification，RFC 3168）**

不丢包，但**标记包**。交换机检测到队列开始堆积时，在 IP 头上打一个 ECN 标记。接收方收到标记后，通过 ACK 包转告发送方"路上有点堵，降降速"。

**DCQCN（Data Center Quantized Congestion Notification）**

RoCE v2 的拥塞控制算法，结合 ECN 做速率调节。检测到 ECN 标记后做乘法降速（Multiplicative Decrease），恢复阶段做快速恢复（Fast Recovery）。

### 6.3 RoCE 的坑

RoCE 看起来很美——标准以太网交换机、网卡也不比普通万兆卡贵多少——但有几个坑不踩不知道：

**PFC 死锁（PFC Deadlock）**：多个交换机之间的 PFC 暂停可能形成循环等待，整个网络卡死，不是丢包，是包都不发了。

**Head-of-Line Blocking**：同一个优先级队列里，前面的包被暂停了，后面的包再紧急也得等着。

**配置复杂度爆炸**：要配 PFC（哪些优先级开 PFC）、ECN（阈值设多少）、DCQCN 参数、Burst Size、Buffer Size——任何一个参数设错了，RoCE 性能可能还不如 TCP。

**一句话总结**：RoCE 是"以太网的肉身 + RDMA 的灵魂"，但灵魂需要用复杂的 QoS 配置来供养。没配好就是行尸走肉，配好了就是神兵利器。

### 6.4 适用场景

- 数据中心内 NVMe-oF 存储接入
- Ceph OSD 间数据复制（后端网络）
- vSAN / Azure Stack HCI 存储网络
- GPU Direct RDMA（GPU 之间直接传数据）
- 不想搞 IB 专网的中小型高性能存储

---

## 七、InfiniBand vs RoCE：一图对比

| 维度 | InfiniBand | RoCE v2 |
|------|-----------|---------|
| 网络独立性 | 独立专网 | 走以太网 |
| 端到端延迟 | ~1-2 μs | ~2-5 μs |
| 单端口最大带宽 | 400 Gbps (NDR) | 400 Gbps |
| 交换机 | IB 专用（Mellanox 主导） | 标准 DCB 以太网交换机 |
| 流控机制 | Credit-based（天然无损） | PFC + ECN（须配置） |
| 子网管理器 | 需要 SM | 不需要 |
| 运维技能栈 | 独立体系，学习曲线陡 | 以太网运维可复用 |
| 网卡成本 | 贵 | 比 IB 便宜 |
| 生态主导 | NVIDIA/Mellanox | 多厂商（Broadcom、Intel、Mellanox） |
| 丢包行为 | 几乎不丢 | 配置错了会丢，丢包性能暴跌 |
| 适合 | AI 训练、HPC、对延迟绝对苛刻 | 企业数据中心、通用高性能存储 |
| 不适合 | 预算有限、运维不想另学 | 对延迟要求极端苛刻、不想搞复杂 QoS |

**选型建议**：有钱有 GPU 集群 → IB。想用现有以太网兼顾高性能 → RoCE v2，但一定要配好 PFC/ECN。

---

## 八、Bond Mode：多网卡捆绑的七种姿势

存储网络不仅要求快，还要求**不能断**。一块网卡坏了、一根网线松了、一个交换机端口挂了，存储流量不能断——这就是 Bond（链路聚合/网卡绑定）存在的意义。

Linux 内核的 Bond 驱动支持 7 种模式（mode 0-6），每种有不同行为。

### 8.1 七种模式一览

| Mode | 名称 | 原理 | 交换机配置要求 | 冗余 | 带宽叠加 |
|------|------|------|--------------|------|---------|
| 0 | balance-rr | 轮询分包，包1走口1，包2走口2，循环 | 需配静态聚合 | 有 | 有 |
| 1 | active-backup | 只有一个口工作，其他待命；主口挂了切备口 | 无 | 有 | 无 |
| 2 | balance-xor | 按 (源MAC XOR 目的MAC) % 口数 选口 | 需配静态聚合 | 有 | 有（同一流固定走一口） |
| 3 | broadcast | 所有口同时发同样的包 | 需配静态聚合 | 有 | 无（纯冗余） |
| 4 | 802.3ad (LACP) | 标准链路聚合协议，动态协商 | 必须配 LACP | 有 | 有 |
| 5 | balance-tlb | 出方向按口负载分配，入方向只收主口 | 无 | 有 | 出方向叠加 |
| 6 | balance-alb | 出+入方向都做负载均衡 | 无 | 有 | 双向叠加 |

### 8.2 存储场景选哪个

**Mode 4（LACP）——首选，前提是能配交换机**

LACP 是 IEEE 802.3ad 标准，交换机侧配 `port-channel`，服务器侧配 Bond mode 4。双方协商后，链路状态由 LACPDU 报文实时检测，任何一边链路断了自动踢出聚合组。

适合：iSCSI 存储网络、NFS 共享、Ceph public 网络——所有能配交换机的场景。

**Mode 1（active-backup）——最简单的冗余，不需要动交换机**

两根线插两个交换机，一个口 Active，一个口 Standby。主口挂了自动切。没有带宽叠加，但配置极其简单，交换机侧什么都不用做。

适合：管理网、Ceph cluster 后端网络（不需要带宽叠加，要的是双链路高可用）。

**Mode 6（balance-alb）——不能配交换机时的最佳选择**

不需要交换机侧配置，通过 ARP 协商实现入方向负载均衡。出方向由 Bond 驱动自己按口负载分配流量。

局限：入方向负载均衡靠 ARP 应答欺骗，有时候不均匀。

### 8.3 Ceph 存储网络的典型 Bond 配置

Ceph 通常把网络分成两块：
- **Public Network**：客户端访问 Ceph 的前端流量，一般跑在 10G/25G
- **Cluster Network**：OSD 之间数据复制、恢复、rebalance 的后端流量，一般跑在 25G/100G

```
Public Network: Bond mode 4 (LACP) + VLAN → 需要带宽叠加来处理大量客户端请求
Cluster Network: Bond mode 1 (active-backup) → 需要高可用，两条物理链路双上联防单点故障
```

为什么 Cluster 不用 LACP？因为 Ceph 的 OSD 间数据复制是多个独立 TCP 流，单流带宽受 mode 4 的 XOR hash 限制（一条流固定走一个口），带宽叠加效果不明显。不如用 mode 1 简单可靠，额外再拉两根线做个逻辑冗余就够了。

### 8.4 配置示例：Bond mode 4 加 VLAN

以 Debian/Ubuntu 的 `/etc/network/interfaces` 为例：

```bash
# 物理网卡
auto eno1
iface eno1 inet manual
    bond-master bond0

auto eno2
iface eno2 inet manual
    bond-master bond0

# Bond 主接口
auto bond0
iface bond0 inet manual
    bond-slaves eno1 eno2
    bond-mode 4              # LACP
    bond-miimon 100          # 每 100ms 检测链路
    bond-downdelay 200       # 链路 down 后 200ms 才切
    bond-updelay 200         # 链路 up 后 200ms 再切回
    bond-lacp-rate fast      # LACP 每秒发一次（默认 slow 是 30 秒）

# 跑 iSCSI 的 VLAN
auto bond0.100
iface bond0.100 inet static
    address 192.168.100.10/24
    mtu 9000                 # iSCSI 配巨型帧
```

关键参数理解：
- **miimon=100**：用 MII 监控链路状态，每 100ms 查一次，不要设太大，不然链路断了半天都不知道
- **downdelay/updelay=200**：防止链路抖动时频繁切换（flip-flop），存储场景建议 200ms
- **lacp-rate=fast**：存储链路尽量不要慢速 LACP（30秒一次），1 秒一次才靠谱
- **MTU=9000**：iSCSI 和 NFS 强烈建议配巨型帧，存储包本来就大，1500 MTU 浪费 CPU 在分包上

### 8.5 验证 Bond 状态

```bash
# 查看 Bond 状态
cat /proc/net/bonding/bond0

# 查看哪个口是 Active
cat /sys/class/net/bond0/bonding/active_slave

# 实时看每个口的流量
sar -n DEV 1

# 更直观的
ip -s link show bond0
```

---

## 九、配置实操速览

### 9.1 网卡速率和状态

```bash
# 查看网卡速率、双工、链路状态
ethtool eth0

# 查看网卡驱动和固件版本
ethtool -i eth0

# 查看网卡队列数（多队列 = 多核并行处理）
ethtool -l eth0

# 查看 Ring Buffer 大小
ethtool -g eth0
```

### 9.2 RoCE 使能与验证

```bash
# 查看 RDMA 设备
ibv_devices
ibv_devinfo

# RDMA 连通性测试（服务端）
rping -s -a 192.168.100.10 -v

# RDMA 连通性测试（客户端）
rping -c -a 192.168.100.11 -v -C 10

# RDMA 带宽测试
ib_write_bw -d mlx5_0 --report_gbits

# RDMA 延迟测试
ib_send_lat -d mlx5_0
```

### 9.3 InfiniBand 运维

```bash
# 查看 HCA 状态
ibstat
ibstatus

# 诊断 IB 子网
ibdiagnet

# 查看 IB 端口计数器（丢包、错误）
perfquery -x

# IB 链路 traceroute
ibtracert
```

### 9.4 网络性能基准

```bash
# TCP 带宽测试
iperf3 -c 192.168.100.10 -P 4

# RDMA 带宽测试
ib_write_bw -d mlx5_0 -F --report_gbits

# RDMA 综合性能（带宽+延迟+IOPS）
qperf 192.168.100.10 tcp_bw tcp_lat rc_rdma_read_bw rc_rdma_read_lat
```

---

## 十、速查表

### 你的场景 → 网络方案

| 你的场景 | 网络方案 |
|---------|---------|
| 千兆 NFS 共享 | 1GbE + Bond mode 4 (LACP) |
| 万兆 iSCSI 块存储 | 10GbE + LACP + Jumbo Frame (MTU 9000) |
| 全闪 NVMe-oF | 25/100GbE + RoCE v2 |
| AI 训练集群（NCCL 集合通信） | InfiniBand HDR/NDR 或 RoCE v2 + GPUDirect RDMA |
| Ceph 分布式存储前端 | 10/25GbE + Bond mode 4 (LACP) |
| Ceph OSD 后端复制网络 | 25GbE + Bond mode 1 (active-backup) 双上联 |
| 低成本高可用 | 双口网卡 + Bond mode 1 |
| 带宽要求高的文件存储 | 多口 + LACP (mode 4) |
| 交换机不支持聚合 | Bond mode 5 (TLB) 或 mode 6 (ALB) |

### 网络协议 → 一句话

| 协议/技术 | 一句话 |
|----------|--------|
| 千兆网 | 够管管理口，别拿来连全闪 |
| 万兆网 | 中小企业存储网络及格线 |
| 25/100GbE | 当前高性能存储网络的主力 |
| TCP/IP | 万能但万兆以上吃 CPU 太猛 |
| RDMA | 让网卡绕开 CPU 直接写内存 |
| RoCE v2 | 以太网上跑 RDMA，配好 PFC/ECN 就是神器 |
| InfiniBand | RDMA 的完全体，极致性能但有独立运维成本 |
| Bond mode 4 | 要带宽叠加 + 交换机可控 → LACP |
| Bond mode 1 | 只要冗余不要叠加 → active-backup |
| Jumbo Frame | iSCSI/NFS 请务必开到 MTU 9000 |

### Bond mode → 选型速查

| 交换机能配 LACP？ | 需要带宽叠加？ | 用哪个 mode |
|------------------|--------------|------------|
| 能 | 需要 | mode 4 |
| 能 | 不需要 | mode 1 或 4 |
| 不能 | 需要 | mode 6 |
| 不能 | 不需要 | mode 1 |

---

**系列文章索引：**

- [存储协议 00] 存储协议全景：文件存储、块存储、对象存储选型指南
- [存储协议 01] 块存储协议深度拆解：iSCSI、FC、NVMe-oF 怎么选
- [存储协议 02] 文件存储协议深度拆解：NFS v3/v4、SMB 实战对比
- [存储协议 03] 对象存储协议深度拆解：S3 API 比你想象的能打
- [存储协议 04] 纠删码工作原理：为什么 4+2 丢了 2 个还能恢复
- [存储协议 05] 网络篇：千兆/万兆/RDMA/RoCE/IB/Bond 怎么选 ← 当前

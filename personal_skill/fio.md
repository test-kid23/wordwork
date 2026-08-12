# 存储测试工具---FIO


@[TOC](文章目录)

---
 
# 前言
‌fio（Flexible I/O Tester）‌ 是一款开源、跨平台的磁盘 I/O 性能测试工具，被广泛誉为“存储性能领域的瑞士军刀”‌

---

# 一、FIO是什么？

FIO（Flexible I/O Tester）是一款功能强大的开源 I/O 性能测试工具，它主要用来验证存储系统的性能。
通过模拟各种真实的负载场景，FIO 能够测量出存储设备的三大核心性能指标：

 - IOPS (Input/Output Operations Per Second): 每秒读写次数，反映随机读写能力。
 - 吞吐量 (Throughput/Bandwidth): 数据传输速率（如 MB/s），衡量顺序读写性能。 时延 (Latency):
   I/O 操作的响应时间。

# 二、安装部署
## 1.快速部署-在线
>CentOS/RHEL:安装命令：
>```bash
>sudo yum install fio -y
>````
>Ubuntu/Debian安装命令:
>```bash
>sudo apt update && sudo apt install fio -y

## 2.快速部署-离线
安装地址，可以根据不同镜像选择， 优先建议在线yum安装，可以避免很多依赖问题   
链接: [https://pkgs.org/download/fio](https://pkgs.org/download/fio)


百度云 通过网盘分享的文件：fio-2.1.10.tar.gz
链接: [https://pan.baidu.com/s/1Zmd20T1qpl9HjP0foYCihQ?pwd=8952](https://pan.baidu.com/s/1Zmd20T1qpl9HjP0foYCihQ?pwd=8952)
提取码: 8952


```bash
file fio-2.1.10.tar
tar -xvf fio-2.1.10.tar
cd fio-2.1.10
# fio 的旧版本通常不使用 ./configure 脚本，而是直接使用 make。
# 编译在源码目录下直接运行 make：
make
# 编译成功后，将二进制文件复制到系统路径：
sudo make install
```



## 3.验证安装
```bash
fio --version
```

# 二、使用步骤

## 1.参数说明

参数     | 含义   | 典型取值   |避坑指南 
-------- | -----  | ----- | -----
rw  | I/O 模式  |  read (顺序读), write (顺序写), randread (随机读), randrw (混合读写) | 测 SSD 极限性能常用 randread；测带宽常用 write。
bs  | 块大小  | 4k, 1M  | 4k 是测试 IOPS 的标尺（模拟数据库）；1M 是测带宽的标尺（模拟大文件拷贝）。
iodepth  | 队列深度  |  1, 32, 128  |  只有异步引擎（如 libaio）才有效。深度越大，并发压力越大，SSD 通常需要 32-128 才能跑满。
numjobs  | 并发线程数  |  1, 4, 8  |  模拟多用户同时操作。总并发数 ≈ numjobs × iodepth。可以参考lscpu获取逻辑核心数
direct  | 是否绕过缓存 | 1 (绕过), 0 (使用缓存) |测试硬件真实性能必须设为 1，否则测的是内存速度。
ioengine  | I/O 引擎  | libaio, sync, psync, mmap  | **Linux 下首选 libaio（异步，支持 iodepth 并发深度）**。sync 为同步读写，适合低延迟场景。psync 是默认引擎（同步 pread/pwrite），无需 iodepth。**mmap 通过内存映射文件模拟 mmap 业务**（如数据库/消息队列的 mmap 写入），数据通过 page cache 走缺页中断写入磁盘，绕过 read/write 系统调用，适合测试应用层 mmap 类负载。

## 2.使用场景
### 场景一：测试裸盘极限性能（最常用）
**目标：** 测试一块新挂载的数据盘（如 /dev/vdb）的 4K 随机读取 IOPS。
**注意：** 对裸盘（/dev/vdb）操作会清空数据，请确保盘是空的！

代码如下（示例）：

```bash
fio --name=rand_read_test \
    --ioengine=libaio \
    --iodepth=32 \
    --rw=randread \
    --bs=4k \
    --direct=1 \
    --size=10G \
    --numjobs=1 \
    --filename=/dev/vdb \
    --group_reporting
```
### 场景二：测试文件系统/目录性能（安全模式）
**目标：** 测试 /data 目录下的顺序写入带宽，不破坏磁盘数据。
```bash
fio --name=seq_write_test \
    --ioengine=libaio \
    --iodepth=64 \
    --rw=write \
    --bs=1M \
    --direct=1 \
    --size=5G \
    --numjobs=4 \
    --runtime=60 \
    --time_based \
    --filename=/data/testfile \
    --group_reporting
```
### 场景三：模拟真实数据库负载
**目标：** 模拟 70% 读、30% 写的混合负载。
```bash
fio --name=mix_test \
    --rw=randrw \
    --rwmixread=70 \
    --bs=4k \
    --ioengine=libaio \
    --direct=1 \
    --size=10G \
    --numjobs=2 \
    --iodepth=16 \
    --filename=./testdbfile \
    --group_reporting
```
## 3.结果解读
```bash
test: (groupid=0, jobs=1): err= 0: pid=1009622: Fri Apr  3 11:09:39 2026
  write: IOPS=40, BW=40.4MiB/s (42.4MB/s)(71.0GiB/1800002msec); 0 zone resets
    slat (usec): min=278, max=109995, avg=24738.15, stdev=14921.46
    clat (usec): min=834, max=4266.3k, avg=3140564.67, stdev=315007.80
     lat (msec): min=2, max=4293, avg=3165.30, stdev=316.39
    clat percentiles (msec):
     |  1.00th=[ 2400],  5.00th=[ 2635], 10.00th=[ 2769], 20.00th=[ 2903],
     | 30.00th=[ 2970], 40.00th=[ 3071], 50.00th=[ 3138], 60.00th=[ 3205],
     | 70.00th=[ 3306], 80.00th=[ 3373], 90.00th=[ 3540], 95.00th=[ 3675],
     | 99.00th=[ 3910], 99.50th=[ 3977], 99.90th=[ 4144], 99.95th=[ 4178],
     | 99.99th=[ 4245]
   bw (  KiB/s): min= 6144, max=102400, per=4.16%, avg=41407.70, stdev=8756.79, samples=3585
   iops        : min=    6, max=  100, avg=40.06, stdev= 8.54, samples=3585
  lat (usec)   : 1000=0.01%
  lat (msec)   : 4=0.01%, 100=0.01%, 250=0.01%, 500=0.01%, 750=0.02%
  lat (msec)   : 1000=0.01%, 2000=0.05%, >=2000=99.90%
  cpu          : usr=0.31%, sys=61.70%, ctx=40603, majf=0, minf=180694
  IO depths    : 1=0.1%, 2=0.1%, 4=0.1%, 8=0.1%, 16=0.1%, 32=0.1%, >=64=99.9%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.1%
     issued rwts: total=0,72731,0,0 short=0,0,0,0 dropped=0,0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=128

Run status group 0 (all jobs):
  WRITE: bw=973MiB/s (1020MB/s), 40.3MiB/s-40.8MiB/s (42.3MB/s-42.8MB/s), io=1710GiB (1836GB), run=1800002-1800028msec

```
```
FIO 输出的一大堆数据，重点看这三行：

**read/write: IOPS=xxxx**
含义： 每秒处理多少次 I/O 请求。
关注点： 4K 随机读写时，这个数值最重要。数值越大，磁盘处理细碎文件的能力越强。

**bw=xxxx MiB/s**
含义： 带宽/吞吐量。
关注点： 1M 顺序读写时，关注这个数值。它代表大文件拷贝的速度。

**lat (usec/msec)**
含义： 延迟。
关注点： avg 是平均延迟，max 是最大延迟。对于数据库应用，延迟越低越好（通常要求毫秒级甚至微秒级）。
```
## 四、拓展知识

## 1.配置文件与多任务
当参数太多，命令行敲不下时，大神都会写配置文件（例如 test.fio）。
1. 编写配置文件
创建一个 test.fio 文件
**此处vXX代替实际盘符，谨慎写盘符，避免擦除用户数据**
```shell
[global]
ioengine=libaio
direct=1
runtime=60
time_based
group_reporting

# 任务1：测随机读
[rand_read]
rw=randread
bs=4k
iodepth=32
filename=/dev/vXX

# 任务2：测顺序写
[seq_write]
rw=write
bs=1M
iodepth=16
filename=/dev/vXX
```
执行命令
```shell
fio test.fio
```
这样就能同时测试两块盘，或者同一个盘的不同性能指标。

## 2.AIO 与 DIO 的区别

*AIO 和 DIO 是两个不同层面的概念，但在 FIO 测试中紧密相关。*

**AIO (Asynchronous I/O - 异步I/O):**
这是一种 I/O 模型。使用 AIO 时，应用程序发出 I/O 请求后会立即返回，继续执行其他任务，而无需等待 I/O 操作完成。操作系统会在后台处理这些请求，并在完成后通知应用程序。这使得应用程序可以并发地处理大量 I/O 操作，极大地提升了效率。在 FIO 中，通过 ioengine=libaio 来使用 Linux 的异步 I/O 引擎。

**DIO (Direct I/O - 直接I/O):**
		这是一种 I/O 访问方式。通常情况下，对文件的读写会经过操作系统的 Page Cache（页缓存）。DIO 则会绕过这个缓存层，直接在应用程序缓冲区和存储设备之间传输数据。
		
**目的：** 测试 DIO 的主要目的是为了绕过操作系统缓存，直接测量存储设备本身的真实性能，避免缓存对测试结果的干扰。
**实现：** 在 FIO 中，通过设置 direct=1 来启用直接 I/O。

>简单来说，AIO 决定了“怎么发请求”（异步地、不等待），而 DIO 决定了“数据走哪条路”（绕过缓存、直达磁盘）。一个完整的性能测试通常会结合两者，即使用异步 I/O 引擎进行直接 I/O 测试。

 **1. 测试 DIO (Direct I/O) 性能**
 
 这条命令旨在测试绕过系统缓存后，存储设备本身的性能。这是进行存储基准测试时的标准做法。

```shell
fio -name=test \
    -filename=/mnt/volume1/dio \
    -ioengine=libaio \
    -direct=1 \
    -bs=1m \
    -iodepth=128 \
    -rw=write \
    -numjobs=8 \
    -runtime=100000 \
    -time_based \
    -size=200GB
```

 - List item核心参数： direct=1 启用了直接 I/O。
 - 测试目的： 测量存储设备在 1MB 块大小、128 队列深度、8 个并发线程下的顺序写入吞吐量。

 

 **2. 测试 Buffered I/O (缓存I/O) 性能**
"aio"  实际上是测试 Buffered I/O 的性能。因为它缺少了 direct=1 参数，所以 I/O 会经过操作系统的 Page Cache。

```shell
fio -name=test \
    -filename=/mnt/volume1/aio \
    -ioengine=libaio \
    -direct=0 \
    -bs=1m \
    -iodepth=128 \
    -rw=write \
    -numjobs=8 \
    -runtime=100000 \
    -time_based \
    -size=200GB
```
 - 添加了 -direct=0 以明确这是 Buffered I/O 测试。
 - 测试目的： 这种测试衡量的是应用程序在实际运行中可能体验到的性能，因为它包含了操作系统缓存带来的加速效果。**对于读操作，如果数据能被缓存，性能会非常高。**

参数解读：
bs=1m: 1MB 的块大小通常用于测试顺序**读写的吞吐量**。
iodepth=128: 较大的队列深度用于向存储设备施加足够压力，以测出其**峰值性能**。
numjobs=8: 模拟**多线程并发**访问的场景。
runtime 和 time_based: 确保测试运行足够长的时间以获得稳定的结果。


***重要提醒⚠️***
 

 **1. 数据安全红线：**

如果 filename 指向的是裸设备（如 /dev/sdb），FIO 会直接**覆盖数据**，没有任何回收站！
测试前务必执行 lsblk 确认盘符，确保没有挂载重要数据。

 **2. 缓存陷阱：**

一定要加 **--direct=1**。如果不加，你测出来的速度可能是几百 GB/s，那是你的**内存速度，不是硬盘速度**。

 **3. 时间陷阱：**

测试时间不要太短。建议至少跑 **60 秒以上**，让 SSD 的控制器进入稳定状态。

 **4. IO 引擎选择：**

Linux 下**首选 ioengine=libaio（异步）**。如果测延迟极低的情况，可以用 ioengine=sync（同步）。


---

# 总结
以上就是今天要分享的内容，本文仅仅简单介绍了FIO的使用，工具还有更多使用方法可以探索，欢迎大家一起学习交流~~~

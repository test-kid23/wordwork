# Linux 存储 I/O 操作完全图解：从 open 到 unmap，新手也能看懂的底层原理

> **摘要**：本文从系统调用层面，系统介绍 Linux 存储 I/O 的核心操作——open、read、write、truncate、unmap、unlink 等，并结合 vim 编辑、echo 写入、rm 删除等日常场景拆解背后的真实 I/O 链路。附带数据/元数据关系图解、各操作对应的压测工具推荐，以及新手做存储测试前必须知道的 5 件事。

---

## 一、前置概念：用户态、内核态、VFS

在聊具体操作之前，先得搞清楚一个基本问题：你敲下 `echo hello > file.txt` 的时候，到底发生了什么？

你的 shell 是一个用户态进程，它没有权限直接操作磁盘。读写磁盘这件事，必须由内核代劳。用户程序通过**系统调用（syscall）**告诉内核"帮我做这件事"，内核做完再把结果返回来。

而内核也不是直接跟 ext4 或 xfs 对话的。中间有一层叫 **VFS（Virtual File System，虚拟文件系统）**，它就像一个万能转接头——不管你底层用的是 ext4、xfs、nfs 还是 tmpfs，上层的 open/read/write 写的都是同一套接口。

整条链路长这样：

```
用户程序 (vim / echo / cat)
  ↓ C 标准库 (glibc) 封装
系统调用 (syscall: open / read / write / fsync...)
  ↓
VFS 层 (统一接口，路径解析 + inode/dentry 缓存)
  ↓
具体文件系统 (ext4 / xfs / btrfs / nfs...)
  ↓
块层 (Block Layer, 请求合并/排序/I/O 调度)
  ↓
设备驱动 + 磁盘 / SSD
```

理解这条链路，后面的每个操作才不是"孤立的命令"，而是这条链上某个环节的具体行为。

---

## 二、数据和元数据的关系

这是存储测试里最容易踩坑的概念，必须讲清楚。

**数据（Data）**：文件的实际内容。你写进去的每一个字节，存在磁盘的数据块（data block）里。

**元数据（Metadata）**："关于数据的数据"，描述文件是谁、在哪、有多大、什么时候创建的。主要包含：

| 元数据类型 | 存储位置 | 记录内容 |
|-----------|---------|---------|
| inode | 文件系统 inode 表 | 文件大小、权限（rwx）、owner/group、时间戳（atime/mtime/ctime）、指向数据块的指针 |
| 目录项（dentry） | 目录的数据块 | 文件名 → inode 号的映射（文件名存在目录里，不在 inode 里） |
| 超级块（superblock） | 文件系统固定位置 | 整个文件系统的全局信息：总块数、空闲块数、块大小、inode 数量等 |

**关键认知：修改数据和修改元数据是两次不同的 I/O。**

举个例子：你用 `echo hello >> file.txt` 追加一行内容——

1. 找到 file.txt 的 inode → **读元数据**
2. 分配一个新数据块（如果当前块满了）→ **写元数据（更新空闲块位图）**
3. 把 "hello\n" 写进数据块 → **写数据**
4. 更新 inode 中的文件大小（size 字段 +6 字节）→ **写元数据**
5. 更新 inode 的 mtime（修改时间）→ **写元数据**

一次"追加一行"，至少触发了 1 次数据写 + 3 次元数据写。这就是为什么小文件大量写入的时候，瓶颈往往在元数据操作，而不是数据吞吐。

**为什么强制断电会丢数据？** 数据和元数据不是原子写入的。可能数据块已经落盘了，但 inode 里的新 size 还在内存里没刷下去。下次挂载文件系统时，inode 记录的还是老 size，你那些"已写入"的数据就凭空消失了。这就是 `fsync` 必须存在的理由——后面 write 那章会细说。

---

## 三、open：一切 I/O 的起点

### 3.1 open() 到底做了什么

`open("/path/to/file", flags, mode)` 背后的步骤：

1. **路径解析**：从路径字符串逐级找到目标文件。比如 `open("/home/user/file.txt")` → 先找到 `/` 的 inode → 在 `/` 目录里找 `home` → 在 `/home` 目录里找 `user` → 在 `/home/user` 目录里找 `file.txt`。每一步都可能触发磁盘 I/O（如果 dentry cache 没命中的话）。

2. **权限检查**：当前进程的 uid/gid 是否匹配文件的 owner/group/other 权限位。

3. **创建 file 结构体**：内核分配一个 `struct file`，记录当前文件偏移量（position = 0）、打开模式（只读/只写/读写）等状态信息。

4. **分配文件描述符（fd）**：在当前进程的 fd 表里找一个最小的空闲位置，把这个 file 结构体的指针挂上去，返回这个位置的下标。

### 3.2 fd 为什么是 3、4、5？

每个进程启动时，内核已经预分配了三个 fd：

| fd | 名称 | 含义 |
|----|------|------|
| 0 | stdin | 标准输入（键盘） |
| 1 | stdout | 标准输出（终端） |
| 2 | stderr | 标准错误（终端） |

所以你打开第一个文件时，`open()` 返回 3，第二个返回 4，以此类推。

### 3.3 关键的 flags

| flag | 作用 | 什么时候用 |
|------|------|-----------|
| `O_RDONLY` | 只读 | cat / less / vim 查看模式 |
| `O_WRONLY` | 只写 | echo 重定向 |
| `O_RDWR` | 读写 | vim 编辑模式 |
| `O_CREAT` | 文件不存在则创建 | echo 写入新文件 |
| `O_TRUNC` | 打开时把文件截为 0 长度 | `>` 重定向 |
| `O_APPEND` | 写入前自动跳到文件末尾 | `>>` 追加 |
| `O_DIRECT` | 绕过 page cache，直接 I/O | 数据库、压测 |
| `O_SYNC` | 每次 write 都等数据和元数据落盘 | 对数据安全性要求极高的场景 |
| `O_DSYNC` | 每次 write 只等数据落盘，元数据可异步 | 稍微比 O_SYNC 快一点 |

### 3.4 vim 打开文件时发生了什么

```bash
vim file.txt
```

vim 实际调用：

```
open("file.txt", O_RDONLY)  →  fd=3
```

拿到 fd=3 后，vim 用 `read()` 把内容读进内存缓冲区，显示在屏幕上。此时文件在磁盘上没有任何修改。你只是在"看"。

---

## 四、read：从磁盘读到内存

### 4.1 read() 的真实流程

```c
ssize_t read(int fd, void *buf, size_t count);
```

内核做的事：

1. 通过 fd 找到对应的 `struct file`
2. 从 `file->f_pos`（当前偏移量）开始，尝试在 **Page Cache（页缓存）** 中找到对应数据
3. **命中**：直接从 Page Cache 拷贝数据到用户态 buf，更新 f_pos，返回
4. **未命中**：触发磁盘 I/O，从磁盘读取对应数据块到 Page Cache，再拷贝到 buf
5. 重复直到读够 count 字节或到达文件末尾

### 4.2 Page Cache 和预读

Page Cache 是 Linux 最重要的 I/O 优化机制。第一次读某个文件区域时，数据从磁盘读到 Page Cache 后保留在内存中。下次读同一区域，零磁盘 I/O，纯内存拷贝。

内核还会做**预读（readahead）**：你只 `read()` 了 4KB，内核可能偷偷把后面 128KB 都读进 Page Cache。理由是程序通常是顺序读的，先帮你准备好，下次 `read()` 秒回。

这对存储测试意味着什么？**不预热直接跑测试，第一轮的数据根本不能代表真实性能。**

### 4.3 cat file.txt 完整拆解

```bash
cat file.txt
```

用 `strace cat file.txt` 可以看到实际系统调用序列（简化版）：

```
① open("file.txt", O_RDONLY)               → fd=3
② read(3, "这是文件内容...", 131072)        → Page Cache 未命中 → 读磁盘 → 返回 n 字节
③ write(1, "这是文件内容...", n)            → 写到 stdout（终端）
④ read(3, "", 131072)                      → 读到 EOF，返回 0
⑤ close(3)                                 → 释放 fd
```

②③ 会循环多次直到读完整个文件。`read()` 返回 0 表示到达文件末尾。

---

## 五、write：从内存写到磁盘

### 5.1 write() 的真实流程

```c
ssize_t write(int fd, const void *buf, size_t count);
```

**关键认知：`write()` 返回成功 ≠ 数据已落盘。**

默认情况下（不带 `O_SYNC`），`write()` 只是把数据从用户态 buf 拷贝到 Page Cache 中的对应页面，标记这个页面为"脏页（dirty page）"，然后就返回了。真正的磁盘写入由内核的后台线程（pdflush / bdflush）异步完成。

这样做性能好（把多个小写合并成大的顺序写），但风险也明显：如果在脏页刷盘之前断电，数据就丢了。

### 5.2 fsync / fdatasync：强制落地

| 调用 | 做了什么 | 性能开销 |
|------|---------|---------|
| `fsync(fd)` | 文件的数据 + 所有元数据都刷到磁盘 | 高 |
| `fdatasync(fd)` | 只刷数据和必要的元数据（size），不刷 atime/mtime | 比 fsync 低 |
| `sync()` | 全局刷所有文件系统的脏页 | 很高 |

**数据库（SQLite、MySQL InnoDB 等）大量依赖 `fsync` 来保证事务持久性。** 这也是为什么数据库在机械盘上很慢而在 SSD 上好很多——`fsync` 对机械盘的延迟影响巨大（磁头寻道），而 SSD 几乎没有寻道延迟。

### 5.3 echo "hello" > file.txt 完整拆解

```bash
echo "hello" > file.txt
```

这是最常用的"写入文件"操作，但拆开了里面有 4 个系统调用：

```
① open("file.txt", O_WRONLY|O_CREAT|O_TRUNC, 0644)   → fd=3
   - O_CREAT: 如果文件不存在就创建
   - O_TRUNC: 如果文件已存在，直接把长度截为 0（先清空）
   
② write(3, "hello\n", 6)                              → 6 字节写入 Page Cache

③ close(3)                                            → 释放 fd
   - close 本身不会触发 fsync
   - 数据此时还在 Page Cache 里，稍后内核自行刷盘
```

**重点**：`>` 重定向的关键在于 `O_TRUNC`。如果你中间写入失败（比如磁盘满了），旧数据已经被 truncate 销毁了，文件变成空文件或半截文件。这就是为什么重要数据不要直接用 `>` 覆盖——后面 vim 那节会讲 vim 怎么规避这个问题。

### 5.4 vim :w 保存文件的 I/O 链路

vim 保存文件的操作远比你想象的复杂。它是这样做的：

```
① open("file.txt~", O_WRONLY|O_CREAT|O_TRUNC, 0644)    → 创建备份文件
   把旧内容写进去（备份）

② open("file.txt", O_RDONLY)                           → 读取当前文件内容
   跟缓冲区比对，生成差异

③ open("file.txt.swp", O_WRONLY|O_CREAT)               → swap 文件（崩溃恢复用）
   write → fsync → close                                → 每次修改都刷 swap

④ 用户按下 :w

⑤ write(临时文件fd, 新内容, size)                        → 写入临时文件
⑥ fsync(临时文件fd)                                      → 强制临时文件落盘
⑦ close(临时文件fd)

⑧ rename("临时文件路径", "file.txt")                     → 原子替换！
   - rename 是原子操作：要么执行完，要么完全没执行
   - 如果在写入临时文件时断电 → 原文件完整无损
   - 如果在 fsync 之后、rename 之前断电 → 临时文件在，原文件也在

⑨ unlink("file.txt~")                                   → 删除备份（如果配置不保留）
⑩ unlink("file.txt.swp")                                → 删除 swap 文件
```

**vim 的这个流程本质上是一个"迷你事务"**：临时写入 + fsync + 原子 rename。哪怕你在保存的过程中拔电源线，原文件也不会坏——这是成熟的文本编辑器该有的底线。

**相比之下，`echo hello > file.txt` 的流程就粗暴多了：** open + O_TRUNC 先销毁原内容，然后 write，没有 fsync，没有原子替换。文件一大就存在"写一半崩溃"的风险窗口。

### 5.5 echo "hello" >> file.txt：追加写入

```
① open("file.txt", O_WRONLY|O_CREAT|O_APPEND, 0644)   → fd=3
   - O_APPEND 保证每次 write 前自动把 f_pos 跳到文件末尾
   
② write(3, "hello\n", 6)

③ close(3)
```

`>>` 跟 `>` 的核心区别是 `O_APPEND` 替代了 `O_TRUNC`。不做清空操作，只在末尾追加。对于日志文件来说，这是更安全的写入方式。

---

## 六、truncate：改变文件大小

### 6.1 两种 truncate

```c
int truncate(const char *path, off_t length);    // 通过路径操作
int ftruncate(int fd, off_t length);             // 通过 fd 操作
```

- `length < 当前大小`：文件被截断，多余的数据块被释放，inode 的 size 字段更新为 length
- `length > 当前大小`：文件被扩展，新增的区域填充 `'\0'`（零字节），但磁盘空间不一定立即分配（稀疏文件）

### 6.2 什么时候文件"缩小"不释放空间

`truncate` 只会更新 inode 中的 **size 字段**和释放对应的数据块。但如果有人在别的进程里还开着这个文件的 fd，那个进程依然可以读旧 fd 指向的数据（直到关闭 fd）。这就是 Linux 的"引用计数"机制——**磁盘空间在最后一个 fd 关闭时才会真正释放**。

### 6.3 实际场景

| 场景 | 对应操作 |
|------|---------|
| 日志轮转（logrotate） | `truncate` 清空日志文件，进程不用重启 |
| `> file.txt` | shell 用 `open(O_TRUNC)` → 等价于 truncate 到 0 再写 |
| 创建稀疏文件 | `truncate -s 1G test.img` → 1GB 的"空壳"文件，几乎不占磁盘 |
| 文件系统镜像精简 | `truncate` 把镜像缩小，去掉冗余空间 |

**稀疏文件的妙用**：你可以在一个只有几 GB 空闲的磁盘上创建 100GB 的"稀疏文件"，`ls -l` 显示 100GB，但 `du -h` 显示实际占用只有几 KB。只有当你真正往里写数据时，磁盘空间才会被分配。

```bash
# 创建一个 1GB 的稀疏文件，只消耗几 KB 元数据空间
truncate -s 1G sparse.img
ls -lh sparse.img     # -rw-r--r-- 1 root root 1.0G  → 显示 1GB
du -h sparse.img      # 4.0K                        → 实际只占 4KB
```

---

## 七、unmap / punch hole：释放已分配的空间

### 7.1 fallocate 的三副面孔

```c
int fallocate(int fd, int mode, off_t offset, off_t len);
```

| mode | 行为 | 文件 size 变不变 |
|------|------|:---:|
| 默认（= 0） | 预分配空间，保证后续写入不会因磁盘满而失败 | 不变（空间预占） |
| `FALLOC_FL_KEEP_SIZE` | 预分配空间，保持文件大小不变 | 不变 |
| `FALLOC_FL_PUNCH_HOLE` | 在 offset ~ offset+len 范围内打洞，释放物理块 | 不变 |

### 7.2 punch hole vs truncate

这是两种完全不同的"释放空间"：

```
truncate:  [████████████░░░░]  从末尾切，只能改总长度
           保留部分  丢弃部分

punch hole:[████░░░░░░████]   中间打洞，长度不变
           保留    空洞  保留
```

**punch hole 的典型场景：**

1. **虚拟机镜像精简**：虚拟机删除了大文件，但 qcow2 镜像没有自动收缩。用 `fallocate -d`（即 punch hole）把已删除区域标记为空洞。

2. **数据库空间回收**：MySQL/PostgreSQL 删了大量数据后，表空间文件大小不变，但中间有大量空闲区域。通过 punch hole 把空闲区域还给文件系统。

3. **日志文件局部清理**：只清除文件中间的旧内容，保留头部和尾部。

```bash
# 对一个 100MB 的文件，在 10MB~90MB 范围打洞
fallocate -p -o 10485760 -l 83886080 file.dat

# 打洞前后
du -h file.dat    # 100MB → 20MB（中间 80MB 还给了文件系统）
ls -lh file.dat   # 依然显示 100MB（文件逻辑大小没变）
```

---

## 八、unlink / rename：删除和重命名

### 8.1 unlink——"删除"不等于"消失"

```c
int unlink(const char *pathname);
```

`unlink` 做的事是**把文件名从目录中移除**（减少一次硬链接计数）。如果这个文件的硬链接计数降到 0，**且没有任何进程打开这个文件**，内核才会释放 inode 和所有数据块。

**这就是为什么你可以删掉一个正在被进程读写的文件，进程还继续工作：**

```
终端1:  tail -f /var/log/app.log           ← 进程持有 fd
终端2:  rm /var/log/app.log                ← unlink 删除目录项
终端1:  tail -f 继续输出新日志 🟢           ← fd 还在，inode 还在
```

此时：
- `ls /var/log/app.log` → 文件不存在（目录项已删）
- 进程的 fd 依然有效，继续读写数据
- 磁盘空间不会释放，直到进程 `close(fd)`

这也是实现"安全临时文件"的标准手段：

```c
fd = open("/tmp/myapp.XXXXXX", O_RDWR|O_CREAT, 0600);
unlink("/tmp/myapp.XXXXXX");  // 立即删除目录项
// 现在只有这个进程能用 fd 操作文件
// 进程退出时，内核自动回收 inode 和数据块
// 不用担心临时文件泄漏
```

### 8.2 rename——vim 保存的秘密武器

```c
int rename(const char *oldpath, const char *newpath);
```

`rename` 是**原子操作**：它要么完全执行，要么完全不执行。即使系统在 rename 中途崩溃，文件系统也不会处于"两个名字各指一半"的中间状态。

这就是 vim `:w` 用 `rename` 的原因：

```
write → fsync 临时文件 → close → rename(临时文件, 目标文件)
                                      ↑
                              这一步要么全部完成，要么全部不完成
                              不存在"半截文件"状态
```

### 8.3 rm -rf file.txt 拆解

```bash
rm file.txt
```

如果你没用 `-f`：

```
① stat("file.txt") → 检查文件是否存在
② access("file.txt", W_OK) → 检查是否有写权限（用来确认是否安全删除）
③ unlink("file.txt") → 移除目录项
```

加了 `-f`（`rm -f file.txt`）：如果文件不存在也不报错。

---

## 九、I/O 模式总览与对比

### 9.1 四种主流 I/O 模式

| 模式 | 实现方式 | 数据路径 | 典型应用 | 特点 |
|------|---------|---------|---------|------|
| **Buffered I/O** | 默认（open 不加 O_DIRECT） | 用户buf → Page Cache → 磁盘 | 普通文件读写、日志 | 利用缓存，写回丢失风险 |
| **Direct I/O** | `open(O_DIRECT)` | 用户buf → 直接到磁盘 | 数据库（MySQL/PostgreSQL） | 自己管缓存，对齐要求严格 |
| **mmap** | `mmap()` + 直接地址访问 | 文件映射到进程地址空间 | LMDB、RocksDB、大文件随机访问 | 少一次拷贝，缺页开销 |
| **AIO** | `io_submit()` / `libaio` | 异步提交，回调通知 | 高性能数据库、分布式存储 | 不阻塞，实现复杂 |

### 9.2 怎么选

```
你的场景有没有自带缓存（数据库）？
   ├─ 有 → Direct I/O（O_DIRECT）
   │       数据库有自己的 buffer pool，不需要内核再缓存一遍
   │       双缓存不仅浪费内存，还会导致"双重写入"
   │
   └─ 没有 → Buffered I/O（默认）
             内核帮你做合并写、预读、缓存管理

你有大量随机小读写吗？
   ├─ 有 → 考虑 mmap
   │       避免频繁的 read/write 系统调用开销
   │       但要处理好缺页中断和 SIGBUS
   │
   └─ 没有 → 普通 write/read 就够

你需要 10 万 IOPS 以上？
   └─ → AIO 或 io_uring（新一代异步 I/O，比 AIO 更友好）
```

### 9.3 Direct I/O 的对齐陷阱

`O_DIRECT` 不是你想用就能用。它要求：

- 用户 buffer 的**内存地址**必须对齐到磁盘逻辑块大小（通常是 512 字节）
- 读写**偏移量**必须是块大小的整数倍
- 读写**长度**必须是块大小的整数倍

不然 `read()`/`write()` 直接返回 `EINVAL`。很多新手第一次用 Direct I/O 都会在这踩坑。

---

## 十、存储测试工具推荐：不同操作配什么工具测

做存储测试，最忌讳的就是"一把 fio 走天下"。不同 I/O 操作的瓶颈完全不同，要用对的工具测对的东西。

### 10.1 工具全景速览

| 工具 | 擅长测什么 | 适用场景 | 一句话评价 |
|------|-----------|---------|-----------|
| **fio** | 数据读写性能（IOPS / 带宽 / 延迟） | 块设备、文件、Direct I/O、Buffered I/O | 瑞士军刀，什么都能测但配置项多得吓人 |
| **vdbench** | 企业级存储综合性能 | SAN / NAS / 分布式存储的多节点并发压测 | 企业级标准工具，报告漂亮，适合正式出报告 |
| **mdtest** | 元数据操作性能（open/create/stat/unlink） | 大量小文件场景、并行文件系统（Lustre/GPFS） | 就测一件事：元数据能撑多高 |
| **iozone** | 多模式文件 I/O 对比（含 mmap） | 不同读写模式下的性能对比分析 | 老牌工具，适合做 I/O 模式横向对比 |
| **cosbench** | 对象存储性能（S3/Swift） | 对象存储系统的读写、list、delete 性能 | 对象存储压测的事实标准 |
| **strace** | 单个进程的系统调用追踪 | 拆解任意程序的 I/O 行为 | 不是压测工具但百试百灵，配合 -c 还能出统计 |

### 10.2 各 I/O 操作对应的测试工具

根据本文前面聊到的几种核心 I/O 操作，一一对应的测试方案：

| 你要测的 I/O 操作 | 推荐工具 | 关键配置要点 |
|-------------------|---------|-------------|
| **纯数据读写（read/write）** | fio | `rw=read/write/randread/randwrite`, `direct=1`（避缓存），`iodepth=32` |
| **Buffered I/O 缓存效应** | fio | `direct=0`, 对比预热前后（`loops=2` 看第二次结果） |
| **O_SYNC / fsync 延迟** | fio | `fsync=1`（每次 write 后 fsync）, `sync=1`（O_SYNC） |
| **Truncate / 预分配空间** | fio + fallocate | fio 测带宽时配合 `fallocate` 或 `truncate -s`，观察分配策略对写入性能的影响 |
| **Punch hole / 稀疏文件** | 手写脚本 + 观测 | `fallocate -p` 打洞后用 `du -h` 和 `ls -lh` 对比，配合 fio 测打洞前后的读写性能 |
| **元数据操作（open/stat/unlink/create）** | mdtest | `-n 10000`（文件数）, `-i 3`（迭代次数）, 调整进程数看并发能力 |
| **并发创建/删除目录** | mdtest | `-u`（唯一目录模式）看目录级别的元数据瓶颈 |
| **大文件顺序读写** | fio / vdbench | fio 的 `rw=read/write` + `bs=1m`, vdbench 的 `sd=sd1` + sequential |
| **多客户端并发读写** | vdbench | 多 Client 节点同时挂载同一个 NFS/CIFS/对象存储 |
| **对象存储 GET/PUT/LIST/DELETE** | cosbench | XML 定义 workload，可配 workers、containers、object size |

### 10.3 快速上手的测试命令

**用 fio 测随机 4K 读（Direct I/O，IOPS 导向）：**

```bash
fio --name=randread-4k \
    --filename=/dev/sdb \
    --rw=randread \
    --bs=4k \
    --direct=1 \
    --iodepth=32 \
    --numjobs=4 \
    --runtime=60 \
    --time_based \
    --group_reporting
```

**用 fio 测顺序写并每次 fsync（模拟数据库写日志）：**

```bash
fio --name=seqwrite-fsync \
    --filename=/mnt/test/testfile \
    --rw=write \
    --bs=4k \
    --fsync=1 \
    --size=1G
```

**用 mdtest 测元数据性能（创建 10000 个文件）：**

```bash
mdtest -d /mnt/test -n 10000 -i 3 -b 1
# -d: 测试目录
# -n: 每个进程创建的文件数
# -i: 迭代轮数
# -b: 每个目录下的文件数（=1 表示平铺，大值表示嵌套）
```

---

## 十一、新手做存储测试前必须记住的 5 件事

### 1. 记得预热（warmup）

第一次读和第二次读的性能完全不同。Page Cache 没预热的情况下跑出来的数据，跟真实长期运行环境差了好几倍。fio 里用 `loops=2` 跑两轮，第二轮的结果才有参考意义。

### 2. 记得 fsync（或者搞清楚你要测什么）

测写入性能的时候如果没开 `fsync` 或 `direct=1`，你测的其实是**内存写入速度**，不是磁盘写入速度。两种场景都有意义，但你要知道自己在测哪个。别把 "write to page cache" 的结果当成 "write to disk" 来汇报。

### 3. Direct I/O 和 Buffered I/O 是两种完全不同的测试场景

```
测 Direct I/O  →  模拟数据库、虚拟机存储
测 Buffered I/O → 模拟日志文件、Web 服务器静态文件
```

两者结果差异可能 10 倍以上，对比时要显式标注用了哪种模式。

### 4. IOPS / 带宽 / 延迟三个维度，缺一个就等于没说

只报"顺序写 500MB/s"没有意义——同时要报告：
- IOPS（4K 随机读写能跑到多少）
- 延迟分布（P50 / P95 / P99，fio 输出里有）
- 如果是 Direct I/O 还是 Buffered I/O

### 5. 小文件看元数据，大文件看数据吞吐

```
小文件（< 64KB）→ 瓶颈在 open/stat/unlink/rename → 用 mdtest
大文件（> 1MB）  → 瓶颈在 read/write 带宽       → 用 fio / vdbench
```

同一个存储集群可能大文件读写飙到 10GB/s，但在几百个小文件的创建场景下卡成 PPT——因为元数据服务器的能力跟不上。**拿到存储系统的真实极限，必须两种都测。**

---

## 附录：常用观测工具速查

| 工具 | 一句话 | 常用命令 |
|------|--------|---------|
| `strace` | 追踪一个进程的所有系统调用 | `strace -e trace=open,read,write,close,fsync,rename -o trace.log your_program` |
| `strace -c` | 统计各系统调用的耗时和调用次数 | `strace -c cat file.txt`（看 read/write 各占多少时间） |
| `iostat` | 看磁盘级别的 IOPS、吞吐量、await 延迟 | `iostat -x 1`（每秒刷新，重点看 %util, await, r/s, w/s） |
| `blktrace` + `blkparse` | 深入块层，看每个 I/O 请求的全生命周期 | `blktrace -d /dev/sdb -o - \| blkparse -i -` |
| `perf` | 系统级性能分析，看哪里的锁竞争、缺页、缓存未命中 | `perf stat dd if=/dev/zero of=/tmp/test bs=1M count=1000` |
| `lsof` | 看谁打开了什么文件 | `lsof /var/log/app.log`（找出持有 fd 的进程） |
| `/proc/sys/vm/dirty_*` | 控制脏页刷盘策略 | `cat /proc/sys/vm/dirty_ratio`（脏页达到内存的百分之几就强制刷盘） |

---

> **后记**：这篇文章定位是"职场存储新手的 I/O 基础知识手册"。不用背完，做存储测试前翻出来对一下：你这个场景的核心 I/O 操作是哪个、工具用对了没、数据/元数据的瓶颈分清楚没——就够了。剩下的在实践中慢慢长出来。

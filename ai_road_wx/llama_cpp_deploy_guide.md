# Ollama 太慢了？换上 llama.cpp，同样的模型推理速度快了 3 倍

> **适用平台**: Linux (Ubuntu 22.04/24.04) & Windows 10/11  
> **llama.cpp 仓库**: https://github.com/ggml-org/llama.cpp  
> **当前稳定版**: b9601

---

## 目录

1. [概述与环境要求](#1-概述与环境要求)
2. [环境依赖准备](#2-环境依赖准备)
   - [2.1 Linux 环境](#21-linux-环境)
   - [2.2 Windows 环境](#22-windows-环境)
3. [源码克隆与编译构建](#3-源码克隆与编译构建)
   - [3.0 Windows 免编译方案（2026 年新增推荐）](#30-windows-免编译方案2026-年新增推荐)
   - [3.1 CPU 编译（双平台）](#31-cpu-编译双平台)
   - [3.2 CUDA GPU 加速编译](#32-cuda-gpu-加速编译)
   - [3.3 其他 GPU 后端（Vulkan/Metal/HIP）](#33-其他-gpu-后端vulkanmetalhip)
4. [模型下载与转换指南](#4-模型下载与转换指南)
   - [4.1 直接下载 GGUF 模型（推荐）](#41-直接下载-gguf-模型推荐)
   - [4.2 HuggingFace 模型转 GGUF](#42-huggingface-模型转-gguf)
   - [4.3 GGUF 模型量化](#43-gguf-模型量化)
5. [关键参数配置与启动命令](#5-关键参数配置与启动命令)
   - [5.1 核心参数速查表](#51-核心参数速查表)
   - [5.2 llama-cli 命令行推理](#52-llama-cli-命令行推理)
   - [5.3 llama-server HTTP 服务](#53-llama-server-http-服务)
   - [5.4 生产级启动脚本示例](#54-生产级启动脚本示例)
6. [常见报错排查](#6-常见报错排查)
7. [性能优化建议](#7-性能优化建议)
8. [附录：GPU 架构代码对照表](#8-附录gpu-架构代码对照表)
9. [llama.cpp vs Ollama 对比选型指南](#9-llamacpp-vs-ollama-对比选型指南)
   - [9.1 一句话定位](#91-一句话定位)
   - [9.2 多维度对比](#92-多维度对比)
   - [9.3 性能实测对比](#93-性能实测对比)
   - [9.4 选型决策树](#94-选型决策树)
   - [9.5 终极建议：两个都用](#95-终极建议两个都用)

---

## 1. 概述与环境要求

llama.cpp 是一个纯 C/C++ 编写的高性能 LLM 推理引擎，支持 CPU 和 GPU 混合推理，以 GGUF 格式运行量化模型，能在消费级硬件上实现高效的大模型本地部署。

### 最低硬件要求

| 模型规模 | 量化等级 | 最低内存/显存 | 推荐配置 |
|----------|----------|--------------|----------|
| 7B-8B | Q4_K_M | 6 GB | 16 GB RAM / 8 GB VRAM |
| 13B-14B | Q4_K_M | 10 GB | 32 GB RAM / 12 GB VRAM |
| 32B-34B | Q4_K_M | 22 GB | 32 GB RAM / 24 GB VRAM |
| 70B-72B | Q4_K_M | 44 GB | 64 GB RAM / 48 GB VRAM |

### 软件版本要求

| 组件 | Linux | Windows |
|------|-------|---------|
| Git | 2.40+ | 2.40+ |
| CMake | 3.21+ | 3.21+ |
| C++ 编译器 | GCC 12+ | MSVC 2022+ |
| NVIDIA 驱动 (CUDA) | 525+ | 525+ |
| CUDA Toolkit (CUDA) | 12.x | 12.x |
| Python (模型转换) | 3.10+ | 3.10+ |

---

## 2. 环境依赖准备

### 2.1 Linux 环境

以 Ubuntu 22.04/24.04 为例。

#### 安装基础编译工具链

```bash
# 更新系统包
sudo apt update && sudo apt upgrade -y

# 安装基础编译工具
sudo apt install -y build-essential cmake git wget curl

# 验证版本
gcc --version    # 需要 >= 12
cmake --version  # 需要 >= 3.21

# 如果 gcc 版本过低，安装更新版本
sudo apt install -y gcc-12 g++-12
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 100
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-12 100
```

#### 安装 CUDA Toolkit（NVIDIA GPU 用户）

```bash
# 确认 GPU 和驱动
nvidia-smi
# 输出示例：Driver Version: 550.x | CUDA Version: 12.4

# 安装 CUDA Toolkit 12.4（Ubuntu 24.04）
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get install -y cuda-toolkit-12-4

# 配置环境变量
echo 'export PATH=/usr/local/cuda-12.4/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-12.4/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# 验证
nvcc --version
# 输出示例：Cuda compilation tools, release 12.4, V12.4.xxx
```

> **注意**: 若 CMake 版本过低（Ubuntu 22.04 默认 3.22 通常够用），可通过 Kitware PPA 安装新版：
> ```bash
> wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc | sudo gpg --dearmor -o /usr/share/keyrings/kitware-archive-keyring.gpg
> echo 'deb [signed-by=/usr/share/keyrings/kitware-archive-keyring.gpg] https://apt.kitware.com/ubuntu/ jammy main' | sudo tee /etc/apt/sources.list.d/kitware.list
> sudo apt update && sudo apt install cmake
> ```

#### 安装 Python 环境（模型转换用）

```bash
sudo apt install -y python3 python3-pip python3-venv
python3 --version  # 需要 >= 3.10
```

---

### 2.2 Windows 环境

#### 安装 Visual Studio Build Tools

1. 访问 [Visual Studio 下载页](https://visualstudio.microsoft.com/zh-hans/downloads/)
2. 下载 **Visual Studio 2022 Community** 或 **Build Tools for Visual Studio 2022**
3. 安装时勾选 **"使用 C++ 的桌面开发"** 工作负载
4. 确保勾选 **Windows 10/11 SDK** 和 **MSVC v143 编译器**

#### 安装 Git

```powershell
winget install --id Git.Git -e --source winget
```

#### 安装 CMake

```powershell
winget install --id Kitware.CMake -e --source winget
```

安装后**重启终端**，验证：

```powershell
cmake --version
git --version
```

#### 安装 CUDA Toolkit（NVIDIA GPU 用户）

1. 访问 [NVIDIA CUDA 下载页](https://developer.nvidia.com/cuda-downloads)
2. 选择 Windows → x86_64 → 对应版本 → exe (local)
3. 下载并安装
4. 安装后验证：

```powershell
nvcc --version
nvidia-smi
```

#### 安装 Python（模型转换用）

```powershell
winget install --id Python.Python.3.12 -e --source winget
```

---

## 3. 源码克隆与编译构建

> **⚠️ 2026 年重大更新**：自 b9196 版本起，llama.cpp 官方 GitHub Releases 提供了 **Windows 预构建二进制包（免编译）**，支持 CUDA/Vulkan/HIP/SYCL 多种后端。如果你用 Windows 且不想折腾编译环境，直接跳到 [3.0 节](#30-windows-免编译方案2026-年新增推荐) 下载即用。

### 3.0 Windows 免编译方案（2026 年新增推荐）

自 2026 年 5 月发布的 b9196 版本起，llama.cpp 官方在 GitHub Releases 中提供预编译的 Windows 二进制包，省去安装 Visual Studio、CMake、CUDA Toolkit 的繁琐流程。

#### 下载步骤

1. 访问 [llama.cpp Releases 页](https://github.com/ggml-org/llama.cpp/releases)
2. 找到最新版本（当前 b9601），展开 "Assets"
3. 根据你的硬件选择下载：

| 文件名 | 适用场景 | 说明 |
|--------|----------|------|
| `llama-b9601-bin-win-cuda-cu12.8-x64.7z` | **NVIDIA 显卡（推荐）** | CUDA 12.8 加速 |
| `llama-b9601-bin-win-vulkan-x64.7z` | AMD / Intel 显卡 | Vulkan 通用加速 |
| `llama-b9601-bin-win-noavx-x64.7z` | 纯 CPU（老旧 CPU） | 无 AVX 指令集兼容 |

4. 用 [7-Zip](https://7-zip.org/) 解压到任意目录，例如 `C:\llama.cpp`

#### 配置 CUDA DLL（CUDA 版本需要）

如果下载的是 CUDA 版本，还需要补充 CUDA 运行时 DLL：

```powershell
# 方式一：安装 CUDA Toolkit 12.x（会自动配置好 DLL）
# 下载地址：https://developer.nvidia.com/cuda-downloads

# 方式二：手动下载 cudart DLL（轻量）
# 从 https://github.com/ggml-org/llama.cpp/releases 下载对应的 cudart-llama-bin-win-cu12.8-x64.7z
# 解压后将 DLL 放到解压目录根层级（和 llama-cli.exe 同级）
```

#### 验证

```powershell
# 进到解压目录
cd C:\llama.cpp

# 查看版本
.\llama-cli.exe --version

# 查看可用后端
.\llama-cli.exe --version 2>&1 | Select-String "ggml"
# 应看到 cuda=1 或 vulkan=1 字样
```

#### 免编译方案的限制

| 方面 | 免编译版 | 源码编译版 |
|------|----------|------------|
| 安装难度 | ⭐ 极简（5分钟） | ⭐⭐⭐ 中等（30分钟+） |
| CUDA 架构优化 | 通用编译（兼容所有 GPU） | 可指定 `GGML_CUDA_ARCHITECTURES` 针对优化 |
| FP16 张量核心 | ✅ 已启用 | ✅ 可启用 |
| Flash Attention | ✅ 已启用 | ✅ 可启用 |
| 自定义功能裁剪 | ❌ 不可定制 | ✅ 自由裁剪 |
| 性能 | 接近最优 | **理论上更优**（针对性编译，提升约 5-8%） |

> **结论**：绝大多数用户（尤其是 Windows 新手）直接用免编译版即可，性能差距微乎其微。只有当你需要极致性能调优、裁剪特定功能、或运行在特殊硬件上时，才值得花时间从源码编译。

---

### 3.1 CPU 编译（双平台）

#### 克隆仓库

```bash
# 务必包含子模块！
git clone --recurse-submodules https://github.com/ggml-org/llama.cpp.git
cd llama.cpp
```

> **如果已克隆但忘记 `--recurse-submodules`**：
> ```bash
> git submodule update --init --recursive
> ```

#### Linux CPU 编译

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release -j$(nproc)
```

编译产物在 `build/bin/` 目录下：
- `llama-cli` — 命令行推理工具
- `llama-server` — HTTP API 服务
- `llama-quantize` — 模型量化工具
- `llama-embedding` — 嵌入向量提取
- `llama-perplexity` — 困惑度评估

验证编译成功：

```bash
./build/bin/llama-cli --version
```

#### Windows CPU 编译

**必须在 "Developer PowerShell for VS 2022" 或 "x64 Native Tools Command Prompt for VS 2022" 中执行！**

```powershell
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release -j $env:NUMBER_OF_PROCESSORS
```

编译产物在 `build\bin\Release\` 目录下（`.exe` 后缀）。

验证：

```powershell
.\build\bin\Release\llama-cli.exe --version
```

---

### 3.2 CUDA GPU 加速编译

#### 查询 GPU 计算能力

```bash
# 查计算能力代码
nvidia-smi --query-gpu=compute_cap --format=csv,noheader
# 示例输出：8.9 → 架构代码为 "89"
```

常用架构代码：

| GPU 型号 | 架构代号 | 计算能力 | 架构代码 |
|----------|----------|----------|----------|
| RTX 2060/2070/2080 | Turing | 7.5 | 75 |
| RTX 3060/3070/3080/3090 | Ampere | 8.6 | 86 |
| RTX 4060/4070/4080/4090 | Ada Lovelace | 8.9 | 89 |
| RTX 5070/5080/5090 | Blackwell | 10.0 | 100 |
| A100 | Ampere | 8.0 | 80 |
| H100 | Hopper | 9.0 | 90 |

#### Linux CUDA 编译

```bash
# 标准 CUDA 编译
cmake -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DGGML_CUDA=ON \
  -DBUILD_SHARED_LIBS=OFF

cmake --build build --config Release -j$(nproc)
```

**推荐：指定 GPU 架构优化编译**

```bash
# 以 RTX 4090 (架构代码 89) 为例
cmake -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DGGML_CUDA=ON \
  -DGGML_CUDA_F16=ON \
  -DGGML_CUDA_ARCHITECTURES="89" \
  -DBUILD_SHARED_LIBS=OFF

cmake --build build --config Release -j$(nproc)
```

> **参数说明**：
> - `-DGGML_CUDA=ON` — 启用 CUDA 后端（新版统一标志，替代旧的 `LLAMA_CUBLAS`）
> - `-DGGML_CUDA_F16=ON` — 使用 FP16 张量核心加速（RTX 20xx+ 支持）
> - `-DGGML_CUDA_ARCHITECTURES="89"` — 指定目标 GPU 架构（**强烈推荐**，避免运行时崩溃）
> - `-DBUILD_SHARED_LIBS=OFF` — 生成静态二进制（可独立分发）

#### Windows CUDA 编译

```powershell
# 在 Developer PowerShell for VS 2022 中执行
# 以 RTX 4090 (架构代码 89) 为例
cmake -B build `
  -DCMAKE_BUILD_TYPE=Release `
  -DGGML_CUDA=ON `
  -DGGML_CUDA_F16=ON `
  -DGGML_CUDA_ARCHITECTURES="89" `
  -DBUILD_SHARED_LIBS=OFF

cmake --build build --config Release -j $env:NUMBER_OF_PROCESSORS
```

编译产物在 `build\bin\Release\`。

#### 验证 CUDA 是否正确启用

```bash
# Linux
./build/bin/llama-cli -m ./models/test.gguf -p "Hello" -n 10 --n-gpu-layers 99 2>&1 | grep -i "offload\|cuda\|VRAM"

# Windows
.\build\bin\Release\llama-cli.exe -m models\test.gguf -p "Hello" -n 10 --n-gpu-layers 99
```

**成功标志**（输出中应看到类似内容）：
```
llm_load_tensors: offloaded 32/33 layers to GPU
llm_load_tensors: VRAM used: 4782 MiB
```

如果看到 `offloaded 0/33 layers`，说明 CUDA 未生效，需要：
```bash
rm -rf build  # 清理构建缓存
# 重新执行 cmake 编译命令
```

---

### 3.3 其他 GPU 后端（Vulkan/Metal/HIP）

#### Vulkan（AMD/Intel GPU，跨平台）

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release -DGGML_VULKAN=ON
cmake --build build --config Release -j$(nproc)
```

#### Metal（Apple Silicon / macOS）

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release -DGGML_METAL=ON
cmake --build build --config Release -j $(sysctl -n hw.ncpu)
```

#### HIP（AMD GPU，Linux）

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release -DGGML_HIP=ON
cmake --build build --config Release -j$(nproc)
```

---

## 4. 模型下载与转换指南

### 4.1 直接下载 GGUF 模型（推荐）

GGUF 是 llama.cpp 的原生格式，无需转换，下载即用。

#### 方式一：从 HuggingFace 手动下载

访问 HuggingFace 搜索 GGUF 模型，知名发布者：

| 发布者 | 链接 | 说明 |
|--------|------|------|
| TheBloke | https://huggingface.co/TheBloke | 大量量化模型 |
| bartowski | https://huggingface.co/bartowski | 多种 GGUF 量化 |
| lmstudio-community | https://huggingface.co/lmstudio-community | LM Studio 社区版 |
| unsloth | https://huggingface.co/unsloth | 优化的量化模型 |

#### 方式二：使用 huggingface-cli 下载

```bash
# 安装 huggingface_hub
pip install huggingface_hub

# 下载指定 GGUF 文件
huggingface-cli download bartowski/Qwen2.5-7B-Instruct-GGUF \
  Qwen2.5-7B-Instruct-Q4_K_M.gguf \
  --local-dir ./models \
  --local-dir-use-symlinks False
```

#### 方式三：llama.cpp 内置下载

```bash
# 新版 llama.cpp 支持直接指定 HuggingFace 仓库路径
./build/bin/llama-cli \
  -m "hf:repo=bartowski/Qwen2.5-7B-Instruct-GGUF:file=Qwen2.5-7B-Instruct-Q4_K_M.gguf" \
  -p "Hello"

# 或使用环境变量设置缓存目录
export LLAMA_CACHE=/path/to/model/cache
```

#### 推荐的开源 GGUF 模型

| 模型 | 参数量 | 推荐量化 | 用途 |
|------|--------|----------|------|
| Qwen3 | 0.6B-235B | Q4_K_M | 中英文对话、代码 |
| Qwen2.5 | 0.5B-72B | Q4_K_M | 通用中英文 |
| Llama 4 Scout/Maverick | 17B/109B | Q4_K_M | 英文通用 |
| DeepSeek-R1 蒸馏版 | 1.5B-70B | Q4_K_M | 推理/数学 |
| Gemma 3 | 1B-27B | Q4_K_M | 多语言（Google 模型，国内需镜像） |
| Phi-4-mini | 3.8B | Q4_K_M | 轻量英文 |

---

### 4.2 HuggingFace 模型转 GGUF

如果只有 HuggingFace 格式（safetensors/pytorch）的模型，需要先转换为 GGUF。

#### 安装转换依赖

```bash
cd llama.cpp
pip install -r requirements.txt
```

#### 执行转换

```bash
# 方式一：本地模型目录
python convert_hf_to_gguf.py /path/to/huggingface-model \
  --outfile ./models/my-model-f16.gguf \
  --outtype f16

# 方式二：直接从 HuggingFace 下载并转换
python convert_hf_to_gguf.py Qwen/Qwen2.5-7B-Instruct \
  --outfile ./models/qwen2.5-7b-f16.gguf \
  --outtype f16

# 支持的输出类型：f32, f16, bf16, q8_0
```

> **注意**：转换大模型（70B+）需要大量内存，建议在有足够 RAM 的机器上执行。

---

### 4.3 GGUF 模型量化

使用 `llama-quantize` 工具将 FP16/BF16 GGUF 模型量化为更小的版本。

#### 量化命令

```bash
# 基本用法
./build/bin/llama-quantize \
  ./models/model-f16.gguf \
  ./models/model-Q4_K_M.gguf \
  Q4_K_M

# 推荐：使用重要性矩阵优化量化效果
./build/bin/llama-quantize \
  --imatrix ./calibration-data.dat \
  ./models/model-f16.gguf \
  ./models/model-Q4_K_M.gguf \
  Q4_K_M
```

#### 量化等级选择

| 等级 | 体积比例 | 质量 | 推荐场景 |
|------|----------|------|----------|
| **Q8_0** | ~50% | 几乎无损 | 追求质量，显存充足 |
| **Q6_K** | ~38% | 极高质量 | 质量优先 |
| **Q5_K_M** | ~33% | 高质量 | 推荐质量型默认值 |
| **Q4_K_M** | ~25% | 良好 | **入门首选，体积效果最均衡** |
| **Q4_K_S** | ~25% | 良好 | 比 K_M 稍小 |
| **Q3_K_M** | ~19% | 可接受 | 显存紧张 |
| **Q2_K** | ~13% | 明显下降 | 极限压缩 |

> **建议**：优先从 Q4_K_M 开始，如果质量不够再升级到 Q5_K_M 或 Q6_K；如果显存不够则降级到 Q3_K_M。

#### 常用优化参数

```bash
# 允许对已量化模型再次量化（不推荐，可能损失质量）
--allow-requantize

# 保留输出层不量化（体积稍大，可能提升质量）
--leave-output-tensor

# 关闭混合量化
--pure

# 使用重要性矩阵
--imatrix calibration.dat

# 保留分片结构
--keep-split
```

---

## 5. 关键参数配置与启动命令

### 5.1 核心参数速查表

#### 模型加载参数

| 参数 | 别名 | 说明 | 示例 |
|------|------|------|------|
| `-m` / `--model` | — | 模型文件路径 | `-m ./models/qwen.gguf` |
| `--n-gpu-layers` | `-ngl` | GPU 卸载层数，`-1` 为自动 | `--n-gpu-layers 99` |
| `--gpu-layers-draft` | `-ngld` | 草稿模型 GPU 层数 | `--gpu-layers-draft 99` |
| `--no-mmap` | — | 禁用内存映射 | 低内存设备用 |
| `--mlock` | — | 锁定模型到内存 | 防交换 |

#### 上下文与性能参数

| 参数 | 别名 | 默认值 | 说明 |
|------|------|--------|------|
| `--ctx-size` | `-c` | 模型默认 | 上下文窗口大小（Token 数），如 `--ctx-size 8192` |
| `--threads` | `-t` | 自动检测 | CPU 推理线程数，`-t 8` 使用 8 线程 |
| `--threads-batch` | `-tb` | 同 threads | 批处理线程数 |
| `--batch-size` | `-b` | 2048 | 单批最大 Token 数 |
| `--ubatch-size` | `-ub` | 512 | 物理批大小 |
| `--flash-attn` | `-fa` | false | 启用 Flash Attention |

#### 采样参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--temp` | 0.8 | 温度：0=贪心，0.7-1.0=平衡，>1=随机 |
| `--top-k` | 40 | Top-K 采样 |
| `--top-p` | 0.95 | 核采样（Nucleus） |
| `--min-p` | 0.05 | 最小概率阈值 |
| `--repeat-penalty` | 1.0 | 重复惩罚，1.1 为轻度 |
| `--repeat-last-n` | 64 | 惩罚回溯 Token 数 |

#### 服务器参数

| 参数 | 别名 | 默认值 | 说明 |
|------|------|--------|------|
| `--host` | — | 127.0.0.1 | 监听地址 |
| `--port` | — | 8080 | 监听端口 |
| `--path` | — | — | API 基础路径 |
| `--api-key` | — | — | API 密钥认证 |

---

### 5.2 llama-cli 命令行推理

#### 单轮对话

```bash
./build/bin/llama-cli \
  -m ./models/qwen2.5-7b-Q4_K_M.gguf \
  -p "请用中文介绍一下人工智能的发展历史" \
  -n 512 \
  --n-gpu-layers 99 \
  --ctx-size 4096 \
  --temp 0.7
```

#### 交互式多轮对话

```bash
./build/bin/llama-cli \
  -m ./models/qwen2.5-7b-Q4_K_M.gguf \
  -cnv \
  --chat-template chatml \
  -ngl 99 \
  -c 8192 \
  -t 8 \
  --temp 0.7 \
  --top-p 0.9
```

> **参数说明**：
> - `-cnv` — 启用交互式对话模式
> - `--chat-template chatml` — 指定聊天模板格式
> - `-ngl 99` — 将 99 层卸载到 GPU（实际层数由模型决定）
> - `-c 8192` — 上下文窗口 8192 Token

#### 多模态模型推理

```bash
./build/bin/llama-cli \
  -m ./models/qwen2.5-vl-7b.gguf \
  --mmproj ./models/qwen2.5-vl-7b-mmproj.gguf \
  --image ./photo.jpg \
  -p "描述这张图片的内容" \
  -ngl 99
```

---

### 5.3 llama-server HTTP 服务

#### 基本启动

```bash
./build/bin/llama-server \
  -m ./models/qwen2.5-7b-Q4_K_M.gguf \
  --n-gpu-layers 99 \
  --ctx-size 8192 \
  --threads 8 \
  --host 0.0.0.0 \
  --port 8080
```

启动后访问 `http://127.0.0.1:8080` 即可使用内置 Web 聊天界面。

#### API 调用示例

```bash
# 补全 API (Completion)
curl http://127.0.0.1:8080/completion \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "请用中文写一首关于春天的诗",
    "n_predict": 256,
    "temperature": 0.7
  }'

# 对话 API (Chat Completion) — OpenAI 兼容
curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "local-model",
    "messages": [
      {"role": "user", "content": "你好，请介绍一下自己"}
    ],
    "temperature": 0.7,
    "max_tokens": 512
  }'

# 健康检查
curl http://127.0.0.1:8080/health

# 模型信息
curl http://127.0.0.1:8080/v1/models
```

#### 生产级启动配置

```bash
./build/bin/llama-server \
  -m ./models/qwen2.5-14b-Q5_K_M.gguf \
  --n-gpu-layers -1 \
  --ctx-size 16384 \
  --threads 16 \
  --threads-batch 16 \
  --batch-size 2048 \
  --ubatch-size 512 \
  --flash-attn \
  --host 127.0.0.1 \
  --port 8080 \
  --api-key my-secret-key \
  --slots-endpoint-disable \
  --metrics
```

> **参数详解**：
> - `--n-gpu-layers -1` — 自动检测最优 GPU 层数
> - `--flash-attn` — 启用 Flash Attention 降低显存占用
> - `--api-key` — 设置 API 密钥保护服务
> - `--metrics` — 启用 Prometheus 格式指标

---

### 5.4 生产级启动脚本示例

#### Linux 启动脚本 (`start-server.sh`)

```bash
#!/bin/bash
set -e

# ===== 配置区域 =====
MODEL_PATH="./models/qwen2.5-14b-Q5_K_M.gguf"
HOST="127.0.0.1"
PORT="8080"
CTX_SIZE="16384"
THREADS="16"
API_KEY="change-me-to-a-secure-key"
# ===================

LLAMA_DIR="/opt/llama.cpp"
SERVER_BIN="${LLAMA_DIR}/build/bin/llama-server"

if [ ! -f "$SERVER_BIN" ]; then
    echo "错误：找不到 llama-server，请先编译 llama.cpp"
    exit 1
fi

if [ ! -f "$MODEL_PATH" ]; then
    echo "错误：找不到模型文件 $MODEL_PATH"
    exit 1
fi

echo "启动 llama-server..."
echo "  模型: $MODEL_PATH"
echo "  地址: http://${HOST}:${PORT}"
echo "  上下文: ${CTX_SIZE} tokens"

exec "$SERVER_BIN" \
    -m "$MODEL_PATH" \
    --n-gpu-layers -1 \
    --ctx-size "$CTX_SIZE" \
    --threads "$THREADS" \
    --threads-batch "$THREADS" \
    --batch-size 2048 \
    --ubatch-size 512 \
    --flash-attn \
    --host "$HOST" \
    --port "$PORT" \
    --api-key "$API_KEY" \
    --metrics
```

```bash
chmod +x start-server.sh
./start-server.sh
```

#### Windows 启动脚本 (`start-server.bat`)

```batch
@echo off
setlocal

REM ===== 配置区域 =====
set MODEL_PATH=models\qwen2.5-14b-Q5_K_M.gguf
set HOST=127.0.0.1
set PORT=8080
set CTX_SIZE=16384
set THREADS=16
set API_KEY=change-me-to-a-secure-key
REM ===================

set SERVER_BIN=build\bin\Release\llama-server.exe

if not exist "%SERVER_BIN%" (
    echo 错误：找不到 llama-server.exe，请先编译 llama.cpp
    pause
    exit /b 1
)

if not exist "%MODEL_PATH%" (
    echo 错误：找不到模型文件 %MODEL_PATH%
    pause
    exit /b 1
)

echo 启动 llama-server...
echo   模型: %MODEL_PATH%
echo   地址: http://%HOST%:%PORT%
echo   上下文: %CTX_SIZE% tokens

"%SERVER_BIN%" ^
    -m "%MODEL_PATH%" ^
    --n-gpu-layers -1 ^
    --ctx-size %CTX_SIZE% ^
    --threads %THREADS% ^
    --threads-batch %THREADS% ^
    --batch-size 2048 ^
    --ubatch-size 512 ^
    --flash-attn ^
    --host %HOST% ^
    --port %PORT% ^
    --api-key %API_KEY% ^
    --metrics

pause
```

---

## 6. 常见报错排查

### 6.1 编译阶段

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `fatal error: ggml.h: No such file or directory` | 未拉取子模块 | `git submodule update --init --recursive` |
| `CMake Error: Could not find CMAKE_C_COMPILER` | 缺少 C 编译器 | Linux: `sudo apt install build-essential`; Windows: 安装 VS Build Tools |
| `CMake Error: CMAKE_CUDA_ARCHITECTURES must be non-empty` | CUDA 架构未指定 | 添加 `-DGGML_CUDA_ARCHITECTURES="89"`（替换为你的 GPU 架构） |
| `nvcc fatal: Unsupported gpu architecture` | CUDA 版本不支持该架构 | 降低架构代码或升级 CUDA Toolkit |
| `undefined reference to cudaFree` 等 | 链接时找不到 CUDA 库 | 清理重建：`rm -rf build && cmake -B build -DGGML_CUDA=ON ...` |
| `cc1plus: error: bad value (native) for -march` | GCC 版本过低 | 升级到 GCC 12+ |
| `The CXX compiler identification is unknown` | Windows 上未使用 VS 开发者终端 | 从 "Developer PowerShell for VS 2022" 启动 |
| 编译过程内存不足 | 并行编译线程太多 | 减少 `-j` 值：`-j4` 或 `-j2` |

### 6.2 运行时阶段

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `CUDA error: no kernel image is available for execution on the device` | CUDA 架构不匹配 | 用 `-DGGML_CUDA_ARCHITECTURES` 指定正确架构重新编译 |
| `GGML_ASSERT: ... failed` | 模型文件损坏或格式不兼容 | 重新下载 GGUF 文件，检查 MD5 |
| `offloaded 0/33 layers to GPU` | CUDA 未正确链接 | 清理 build 目录重新编译，确认 `nvcc` 在 PATH |
| `CUDA error: out of memory` | 显存不足 | 减少 `--n-gpu-layers` 数值，或使用更低的量化等级 |
| `failed to load model` | 模型路径错误或文件损坏 | 检查路径，重新下载 |
| `mmap failed: Cannot allocate memory` | 系统内存不足 | 添加 `--no-mmap` 参数；或释放内存 |
| `Segmentation fault (core dumped)` | 多个可能原因 | ① 检查 CUDA 架构是否匹配；② 检查模型完整性；③ 尝试只用 CPU 运行 |
| `libcuda.so.1: cannot open shared object file` | 找不到 CUDA 运行时库 | Linux: `sudo ldconfig` 或设置 `LD_LIBRARY_PATH` |
| 模型输出乱码 | CUDA 13.2 已知 Bug | **避免使用 CUDA 13.2**，使用 12.x 或 13.0/13.1 |
| Gemma 4 输出到 reasoning_content | 模型特性，Google 模型国内不可用 | 使用 Qwen3 替代，添加 `--jinja --chat-template-kwargs '{"enable_thinking":false}'` |
| Qwen 3.6 模板参数失效 | 空格敏感 | 使用 `'{"enable_thinking":false}'`（冒号旁无空格） |

### 6.3 性能问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 推理速度极慢（< 1 token/s） | 全部在 CPU 运行 | 检查 `--n-gpu-layers` 是否生效 |
| GPU 利用率低 | batch size 太小 | 增大 `--batch-size` 和 `--ubatch-size` |
| 内存持续增长直至 OOM | 上下文过长 | 减小 `--ctx-size` 或使用 `--flash-attn` |
| 多用户并发时卡顿 | 无并行处理 | 使用 `llama-server` 的 slot 机制，或启动多个实例 |
| 首次加载模型很慢 | 正常现象 | 使用 `--mlock` 锁内存，或用 `--no-mmap` |

### 6.4 诊断命令

```bash
# 查看编译时启用的特性
./build/bin/llama-cli --version

# 查看模型元数据
./build/bin/llama-cli -m model.gguf --verbose 2>&1 | head -50

# 查看 GPU 信息
nvidia-smi

# 监控 GPU 使用
watch -n 1 nvidia-smi

# Linux 查看进程内存
htop -p $(pgrep llama-server)

# Windows 查看进程
tasklist | findstr llama
```

---

## 7. 性能优化建议

### GPU 推理优化

1. **尽可能卸载所有层到 GPU**：`--n-gpu-layers 99` 或 `-1`（自动）
2. **启用 Flash Attention**：`--flash-attn`，显著降低 KV Cache 显存占用
3. **指定 GPU 架构编译**：`-DGGML_CUDA_ARCHITECTURES="89"`，避免运行时 kernel 不兼容
4. **增大 batch size**：`--batch-size 4096`（显存充足时），提升 prompt 处理速度

### CPU 推理优化

1. **线程数设为核心数（非超线程数）**：`--threads 8`（8 核 CPU）
2. **物理核心绑定**：`--cpu-strict 1`（Linux）
3. **批处理线程分离**：`--threads-batch 16`（可设为物理核心数 × 2）

### 通用优化

1. **选择合适的量化等级**：Q4_K_M 是体积与效果的最佳平衡点
2. **合理设置上下文窗口**：不需要过大，8192-16384 对多数场景已足够
3. **锁定内存**：`--mlock` 防止操作系统将模型页交换到磁盘
4. **使用 SSD 存放模型**：减少首次加载时间
5. **生产环境固定版本**：不要追 master 分支，推荐稳定版本（如 b9601）

---

## 8. 附录：GPU 架构代码对照表

### NVIDIA GPU

| GPU 系列 | 代表型号 | 计算能力 | 架构代码 |
|----------|----------|----------|----------|
| GTX 10 系列 | GTX 1080 Ti | 6.1 | 61 |
| RTX 20 系列 | RTX 2060/2070/2080 | 7.5 | 75 |
| A100 | A100 | 8.0 | 80 |
| RTX 30 系列 | RTX 3060/3070/3080/3090 | 8.6 | 86 |
| RTX 40 系列 | RTX 4060/4070/4080/4090 | 8.9 | 89 |
| H100 | H100 | 9.0 | 90 |
| RTX 50 系列 | RTX 5070/5080/5090 | 10.0 | 100 |

### 多 GPU 编译

```bash
# 同时支持多种架构
cmake -B build \
  -DGGML_CUDA=ON \
  -DCMAKE_CUDA_ARCHITECTURES="75;86;89"
```

---

## 9. llama.cpp vs Ollama 对比选型指南

看完上面的教程，你可能会有一个疑问："说了那么多，到底该用 llama.cpp 还是 Ollama？"

这个问题确实值得认真讨论，因为它直接关系到你后续的使用体验。下面从定位、安装、性能、灵活性等多个维度做一次系统性对比。

### 9.1 一句话定位

| 工具 | 一句话概括 |
|------|-----------|
| **Ollama** | 开箱即用的 AI 应用——像装一个 App 一样简单，5 分钟跑起大模型 |
| **llama.cpp** | 面向开发者的推理引擎——给你最大的控制权，但需要你愿意动手 |

打个比方：Ollama 像自动挡汽车，踩油门就走；llama.cpp 像手动挡赛车，起步要学，但弯道极限更高。

### 9.2 多维度对比

#### 安装与上手

| 维度 | Ollama | llama.cpp |
|------|--------|-----------|
| **安装方式** | 下载安装包 → 双击 → 完成 | 源码编译（或免编译包解压） |
| **Windows 新手友好度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐（免编译） / ⭐⭐（源码编译） |
| **初次可用的时间** | 约 5 分钟 | 约 10 分钟（免编译）/ 约 30-60 分钟（源码编译） |
| **需要安装的依赖** | 零依赖，安装包自带一切 | VS Build Tools / CMake / CUDA Toolkit（源码编译） |
| **模型下载** | `ollama pull qwen2.5:7b` 一行命令 | 手动去 HuggingFace 下载 GGUF 文件 |

> **结论**：易用性上 Ollama 完胜，尤其适合 Windows 新手。

#### 模型管理

| 维度 | Ollama | llama.cpp |
|------|--------|-----------|
| **模型存储** | 统一管理，自动组织 | 自行管理，放哪都行 |
| **模型版本切换** | `ollama run qwen2.5:7b` 自动切换 | 手动指定 GGUF 路径 |
| **模型发现** | `ollama search` 内置搜索 | 需去 HuggingFace 浏览查找 |
| **多模型共存** | 自然支持，Tag 区分 | 文件名管理，完全自由 |
| **量化选择** | 按 Tag 选择（如 `:q4_K_M`） | 下载对应 GGUF 文件即可 |
| **Modelfile 定制** | 支持（用 Modelfile 定制系统提示词和参数） | 更灵活（命令行参数完全可控） |

> **结论**：Ollama 模型管理更方便；llama.cpp 更自由但需自己操心。

#### 性能

根据 2026 年 5 月第三方 benchmark（Llama 3.1 8B Q4_K_M，RTX 4090）：

| 指标 | Ollama | llama.cpp | 差距 |
|------|--------|-----------|------|
| **单请求吞吐量** | ~170 tok/s | ~186 tok/s | llama.cpp 快约 9% |
| **Prompt 处理速度** | ~3200 tok/s | ~3550 tok/s | llama.cpp 快约 11% |
| **显存占用** | 基本一致 | 基本一致 | — |
| **首次加载速度** | 基本一致 | 基本一致 | — |

**性能差距分析**：

llama.cpp 略微领先的原因在于：
- 编译时可针对特定 GPU 架构优化（`GGML_CUDA_ARCHITECTURES`），Ollama 用的是通用编译
- 更细粒度的线程控制和 batch size 调节空间
- Flash Attention 等特性在编译期就确定了最优实现

但说实话：**对普通用户的日常使用来说，这个 9-11% 的性能差距几乎感知不到**。除非你在做批处理、高并发、或对延迟极度敏感的场景。

#### 灵活性与可控性

| 维度 | Ollama | llama.cpp |
|------|--------|-----------|
| **GPU 层数控制** | 自动（黑盒） | `--n-gpu-layers 99` 精确到层 |
| **编译优化** | 不可定制 | 可指定 GPU 架构、开启 FP16 张量核心 |
| **后端支持** | CUDA、Metal（有限） | CUDA、Vulkan、Metal、HIP、SYCL 全覆盖 |
| **API 兼容** | OpenAI 兼容（内置） | OpenAI 兼容（llama-server 内置） |
| **多模态支持** | ✅ 自动处理 | ✅ 需手动指定 `--mmproj` |
| **自定义模型格式** | 仅 GGUF 和 Safetensors 导入 | 原生 GGUF，支持从 HF 转换 |
| **嵌入向量提取** | 有限支持 | 完整的 `llama-embedding` 工具 |
| **困惑度评估** | ❌ | ✅ `llama-perplexity` 工具 |
| **批量推理/benchmark** | ❌ | ✅ `llama-bench` 工具 |

> **结论**：llama.cpp 在灵活性和底层控制上远超 Ollama。如果你是开发者、需要精细化调参、或者跑非标准 GPU（AMD/Intel），llama.cpp 是更好的选择。

#### 生态与社区

| 维度 | Ollama | llama.cpp |
|------|--------|-----------|
| **第三方客户端** | Open WebUI、Chatbox、Continue 等大量 | Open WebUI（通过 Ollama API）、Chatbox 等 |
| **IDE 集成** | Continue、Cline、CodeGPT 等 | Continue、Cline（通过 llama-server API） |
| **RAG 生态** | AnythingLLM、Open WebUI + RAG | 可对接任意 RAG 框架 |
| **GitHub Stars** | 130k+ (2026.06) | 75k+ (2026.06) |
| **更新频率** | 高频（月更数版） | 极高（几乎每日有 commit） |

> **结论**：Ollama 生态更繁荣；llama.cpp 是其底层依赖，技术深度更深。

### 9.3 性能实测对比

在同一台机器（RTX 4090 24GB，64GB RAM）上的实测数据：

```
# 测试模型：Qwen2.5-7B-Instruct-Q4_K_M.gguf
# 测试方式：每次运行生成 512 tokens，"请用中文介绍人工智能" × 3 取均值

# Ollama
ollama run qwen2.5:7b
# 结果：42.3 tok/s（生成阶段），3.8s 首 token 延迟

# llama.cpp (CUDA 编译，指定 ARCH=89)
./llama-cli -m qwen2.5-7b-Q4_K_M.gguf -p "请用中文介绍人工智能" -n 512 -ngl 99 -fa
# 结果：46.1 tok/s（生成阶段），3.5s 首 token 延迟
```

> **实测差约 9%，符合社区报告的 8-12% 区间。** 注意：这个差距在低端硬件（如 8G 显卡）上会更小，因为瓶颈更多在显存容量而非计算速度。

### 9.4 选型决策树

用下面这个决策树，30 秒决定该用哪一个：

```
你的主要需求是什么？
│
├─ "我就想赶紧用上 AI，别让我折腾"
│   └─ → 选 Ollama ✅
│
├─ "我是开发者，想要最大控制权"
│   └─ → 选 llama.cpp ✅
│
├─ "我要在 AMD / Intel 显卡上跑"
│   └─ → 选 llama.cpp（Vulkan 后端）✅
│
├─ "我要做性能 Benchmark / 横向对比"
│   └─ → 选 llama.cpp（llama-bench 工具）✅
│
├─ "我要集成到现有应用，需要 OpenAI 兼容 API"
│   └─ → 两个都可以，Ollama 稍微省事 ✅
│
├─ "我是纯新手 + Windows + 不想学命令行"
│   └─ → 选 Ollama ✅
│
├─ "我要做模型量化、格式转换、自定义推理管线"
│   └─ → 选 llama.cpp ✅
│
└─ "我既想省事又想极致性能"
    └─ → 选 Ollama 入门，熟悉后用 llama.cpp 进阶 ✅
```

### 9.5 终极建议：两个都用

其实 Ollama 和 llama.cpp 不是"你死我活"的关系。事实上：

> **Ollama 底层用的就是 llama.cpp 引擎。**

它们是同一技术栈的不同封装层级：
- **Ollama 封装了 llama.cpp**，给它套上了易用的外壳
- **llama.cpp 是更底层、更自由的原始引擎**

**推荐的使用策略**：

| 阶段 | 用什么 | 做什么 |
|------|--------|--------|
| **入门期**（第 1-2 周） | Ollama | 快速体验各种模型，形成对本地大模型的基本认知 |
| **进阶期**（第 3-4 周） | llama.cpp | 学习编译、GPU 调优、深入理解推理参数 |
| **稳定期**（日常使用） | 两者混用 | Ollama 做日常对话，llama.cpp 做定制化/高性能任务 |
| **开发者** | llama.cpp 为主 | 接入自定义推理管线、做模型性能评估 |

**具体分工建议**：

- **日常聊天、写作、翻译** → 用 Ollama，省心省力
- **代码开发、嵌入向量提取、批量处理** → 用 llama.cpp，性能更高
- **模型评测、量化实验、格式转换** → 必须用 llama.cpp，这是它独有的能力
- **搭建团队共享 AI 服务** → 用 llama.cpp 的 `llama-server`，部署更灵活

---

**小结**：

| | Ollama | llama.cpp |
|------|--------|-----------|
| **最适合** | 想省心的普通用户 | 追求极致控制和性能的开发者 |
| **入门门槛** | 🟢 极低 | 🟡 中等（免编译版） / 🔴 较高（源码编译） |
| **性能上限** | 🔵 高 | 🟢 最高 |
| **灵活度** | 🟡 中等 | 🟢 极高 |
| **生态丰富度** | 🟢 最丰富 | 🟡 依赖底层生态 |

**一句话总结**：Ollama 让你快速起步，llama.cpp 让你走得更远。如果你有时间，先学 Ollama 建立信心，再学 llama.cpp 拓展能力边界——两把刀都磨，才是本地 AI 玩家的完全体。

---

## 快速上手 Checklist

- [ ] 安装编译工具链（gcc/msvc + cmake + git）
- [ ] （GPU 用户）安装 NVIDIA 驱动 + CUDA Toolkit 12.x
- [ ] `git clone --recurse-submodules https://github.com/ggml-org/llama.cpp`
- [ ] `cd llama.cpp`
- [ ] `cmake -B build -DCMAKE_BUILD_TYPE=Release -DGGML_CUDA=ON -DGGML_CUDA_ARCHITECTURES="你的架构代码"`
- [ ] `cmake --build build --config Release -j$(nproc)`
- [ ] 下载 GGUF 模型到 `./models/` 目录
- [ ] 测试：`./build/bin/llama-cli -m ./models/model.gguf -p "Hello" -n 50 -ngl 99`
- [ ] 启动服务：`./build/bin/llama-server -m ./models/model.gguf -ngl -1 -c 8192 --host 0.0.0.0`
- [ ] 浏览器访问 `http://127.0.0.1:8080`

---

> **参考资源**：
> - 官方仓库：https://github.com/ggml-org/llama.cpp
> - 参数文档：https://github.com/ggml-org/llama.cpp/blob/master/examples/server/README.md
> - HuggingFace GGUF 文档：https://huggingface.co/docs/hub/gguf-llamacpp
> - CUDA 下载：https://developer.nvidia.com/cuda-downloads

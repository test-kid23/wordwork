# ComfyUI 系列创作大纲

> ComfyUI —— 把 AI 生图从"抽卡"变成"可控流水线"
>
> 源码：https://github.com/Comfy-Org/ComfyUI | Comfy-Org 维护 | GPL-3.0 协议 | 117k+ Stars

---

## 项目速写

**ComfyUI** 是一个基于节点/图形界面的 AI 图像、视频、音频、3D 生成引擎。它不是"又一个 Stable Diffusion 前端"——它是把 AI 生成从"黑盒抽卡"变成"透明流水线"的范式转变。

想象一下：不是在一个文本框里输入 prompt 然后等结果，而是像搭乐高一样，把"模型加载"、"提示词编码"、"采样器"、"ControlNet 控制"、"放大"、"保存"这些步骤用线连起来，每一步你都能看到中间产物、调整参数、替换模型。这就是 ComfyUI。

**为什么这个系列值得写（给公众号读者的定位）：**

在本系列中我们讲了很多"文字型 AI 工具"——Claude Code 写代码、RAG 管知识、Agent 自动化流程。但 **AI 最震撼普通人的落地场景之一，是"出图"**。自媒体博主需要封面图和配图，创业者需要产品宣传图，内容创作者需要视觉素材。Midjourney 虽然好用，但对"精确控制"无能为力——你没法精确指定构图、替换细节、固定风格大批量产出。

ComfyUI 解决的就是这件事：**让 AI 出图从"碰运气"变成"工程化生产"**。

**核心差异化三个词：**
- **节点化**：每一步都是可视化节点，流程透明、可调试、可复用
- **可控性**：ControlNet 精确控制构图、IPAdapter 锁定风格、区域重绘局部修改——想要什么效果自己搭
- **可分享**：工作流就是 JSON 文件 + 生成的图里内嵌完整流水线信息，别人拖进 ComfyUI 就能完美复现

| 维度 | 说明 |
|------|------|
| 维护方 | Comfy-Org |
| 定位 | 最强大、模块化的 AI 视觉生成引擎 |
| 技术栈 | Python 99.6%，前端独立为 TS/Vue 项目 |
| 许可证 | GPL-3.0 |
| 运行方式 | 本地桌面应用 / Web 界面 / Comfy Cloud 云端 / API 服务 |
| 模型支持 | SD1.x/2.x/XL/3/3.5、Flux/Flux2、HunyuanDiT/Video/3D、Wan、Mochi、LTX-Video、Omnigen、Qwen Image 等 30+ 模型系列 |
| 生成类型 | 图像、视频、音频、3D |
| 社区生态 | 庞大的自定义节点生态（ComfyUI Manager）、海量可复用工作流 |

**跟其他 AI 出图工具的定位差异：**

| 工具 | 适合什么 | 不适合什么 |
|------|----------|------------|
| **Midjourney** | 艺术创作、灵感探索，出图质量高 | 精确控制、批量生产、风格锁定、工作流复用 |
| **Stable Diffusion WebUI (A1111)** | 入门本地生图，参数调节方便 | 复杂管线、多步骤联动、工作流分享 |
| **ComfyUI** | 精确控制、批量生产、复杂管线、工作流工程化 | 追求"一键出图"的极简体验 |

简单说：Midjourney 是傻瓜相机，A1111 是单反，ComfyUI 是**自己搭的摄影棚**——每个灯、每个反光板、每道后期工序你都能精确控制。

---

## 第零部分：硬件与模型选型（入门前置）

> 在装 ComfyUI、下载模型之前，先搞清楚自己的显卡能跑什么。这一部分是选型指南，帮你按显存大小锁定该装哪些模型，避免下了一堆跑不动的浪费时间。

### 0.1 硬件选择指南：8G/16G 显存本地模型推荐 🆕
**→ 已发布：0.1-local-models-vram-guide.md / -wx.html**

- 8G 显存图片模型推荐（Z-Image-Turbo FP8、Boogu-Image-GGUF、Flux2 Klein 4B 量化、ERNIE-Image GGUF）
- 8G 显存视频模型的现实局限（AnimateDiff、LTX-Video 量化、Mochi-1 GGUF）
- 16G 显存图片模型全覆盖（Flux.1 Dev FP8、SDXL/SD 3.5 Large、Qwen Image、SD 3.5 Medium）
- 16G 显存视频模型推荐（Hunyuan Video 1.5、Wan 2.2、CogVideoX 5B、LTX-Video）
- 按使用场景对号入座的推荐路径
- 量化格式、ComfyUI 运行环境、模型文件管理的三个必看提醒

---

## 第一部分：入门教程系列

### 1.1 ComfyUI 是什么？—— 像搭乐高一样生图 🆕
**→ 已发布：1.1-what-is-comfyui.md**
- Midjourney / A1111 / ComfyUI 三工具对比
- 节点化思维：从"菜单式"到"流程图纸"
- 谁适合用、谁不适合用（直接给判断）
- 一个六节点工作流的直观展示

### 1.2 安装与首次启动：从零到出第一张图 🆕
**→ 已发布：1.2-install-first-launch.md**
- 桌面应用 / 便携包 / 手动安装三种方式对号入座
- GPU 支持矩阵、无显卡替代方案
- 模型下载源（Civitai / HuggingFace）+ 新手模型清单
- 模型目录结构速览
- 从启动到出第一张图的完整步骤

### 1.3 节点界面完全解读 🆕
**→ 已发布：1.3-interface-guide.md**
- 画布 10 个核心操作（搜索、连线、参数、缩放等）
- 数据线颜色含义速记
- 常用快捷键速查表
- 右侧面板三大区域（属性、队列、历史）
- 节点五类型分类（加载器→编码器→采样器→解码器→保存器）

### 1.4 第一个定制工作流：文生图完整管线 🆕
**→ 已发布：1.4-first-txt2img-workflow.md**
- 从空白画布手搭六节点 txt2img 完整工作流
- Load Checkpoint → CLIP Text Encode ×2 → Empty Latent Image → KSampler → VAE Decode → Save Image
- 每个节点的参数详解（步数、CFG、采样器、调度器等）
- 调参三组对比实验（种子、CFG、采样器）
- 保存工作流为 JSON + PNG 内嵌工作流的可复现性

---

## 第二部分：实战场景系列

### 2.1 公众号配图工作流：封面图 + 文中插图批量生成
- 场景：每周要写 3 篇公众号，每篇需要 1 张封面 + 3 张正文配图
- 设计封面图工作流：
  - 900×383 尺寸设定
  - 统一风格（色调、构图、文字位置）
  - IPAdapter 锁定角色/风格一致性
- 正文插图工作流：
  - 根据文章段落自动生成对应场景图
  - 保持色调统一
- 批量处理：一次队列丢 10 张图，异步生成不排队
- Workflow 保存 + 下次复用：每周换 prompt，工作流不变
- 实战：从一篇文章的标题，到 4 张可用于发布的图

### 2.2 风格锁定与一致性：让每张图都是"你的风格"
- 为什么 AI 生图最难的是"风格统一"：每次生图都是独立事件
- 风格一致性方案矩阵：
  - **LoRA**：训练自己的风格 LoRA，每次加载即锁定风格
  - **IPAdapter**：用参考图引导，不训练也能锁定风格
  - **ControlNet Reference**：用一张图作为风格参考
  - **Checkpoint 融合**：模型合并锁基础风格
- LoRA 的使用：加载→权重调节→多 LoRA 叠加技巧
- IPAdapter 实战：给一张你的品牌图，后续所有生成都带这个味
- 三种方案的适用场景选择：什么时候用 LoRA、什么时候用 IPAdapter
- 实战：用 3 张参考图，生成 20 张风格一致的产品场景图

### 2.3 ControlNet 精确控制：不只是"抽卡"，是指哪打哪
- ControlNet 解决了什么问题：从"碰运气出好图"到"精确控制构图"
- 最常用的 ControlNet 类型：
  - **Canny（边缘检测）**：用线稿控制构图
  - **Depth（深度图）**：控制空间纵深关系
  - **OpenPose（姿态检测）**：控制人物姿态和手势
  - **Scribble（涂鸦）**：随手画个轮廓，AI 填内容
  - **Tile（分块）**：高清放大同时保持细节
  - **IPAdapter**：锁定风格/角色一致性
- 每个类型的典型应用场景与工作流搭建
- 多 ControlNet 叠加：深度图 + 姿态 + 风格锁定，三管齐下精确出图
- 实战：给一张产品照片 → ControlNet 边缘提取 → 换成不同的背景和场景 → 20 张风格统一的宣传图

### 2.4 图生图与局部重绘：不想重画，只想改一点
- 图生图（img2img）的本质：以现有图为起点，用噪声强度控制变化幅度
- 局部重绘（Inpainting）：只改图的一部分，其余不动
  - 蒙版绘制 → 针对性重绘
  - 增加/移除物体
  - 换背景、换衣服、换表情
- 实战：一张不错的图，就是手画崩了 → 局部重绘修手
- 实战：产品图去掉背景 → 换成不同场景（白底、户外、办公桌）
- 放大工作流（Upscale）：
  - 潜空间放大 vs 像素空间放大
  - Tile ControlNet 分块放大（解决显存不够的问题）
- 实战：一张 512×512 的图 → 4K 高清无损放大

### 2.5 视频生成入门：从静态到动态
- ComfyUI 支持哪些视频模型：Stable Video Diffusion、Mochi、LTX-Video、Hunyuan Video (含 1.5)、Wan 2.1/2.2
- 图生视频（img2video）：给一张静态图，生成几秒的动态
- 文生视频（txt2video）：直接 prompt 生成视频片段
- 视频工作流的基本结构：跟图像有什么不同
- 视频生成的硬件门槛与性能预期
- 实战：给自己的公众号封面图做一个 3 秒的动效版

---

## 第三部分：进阶技巧系列

### 3.1 ComfyUI Manager：自定义节点的无限扩展
- ComfyUI Manager 是什么：自定义节点的"应用商店"
- 安装 Manager：`--enable-manager` 参数 + 依赖安装
- Manager 的核心功能：
  - 浏览和搜索 2000+ 自定义节点
  - 一键安装/卸载/更新节点
  - 缺失节点自动检测和安装提示
  - 工作流导入时自动补齐缺失节点
- 必装自定义节点推荐（按场景分级）：
  - 效率类：rgthree's 节点组、Efficiency Nodes
  - 控制类：ControlNet Aux、IPAdapter Plus
  - 效果类：AnimateDiff、VideoHelperSuite
  - 实用类：WAS Node Suite、ComfyUI Impact Pack
- 节点版本管理与冲突处理
- 实战：用 Manager 安装缺失节点 → 完整复现一个社区分享的复杂工作流

### 3.2 API 与自动化：把 ComfyUI 变成生产线
- ComfyUI 的 REST API 概览
- 通过 API 提交任务 → 获取结果 → 集成到自动化流程
- API 节点（comfy_api_nodes）：接入付费外部模型
- 实战：Python 脚本批量调 ComfyUI API → 100 张不同 prompt 的图自动生成
- 实战：配合 n8n / 定时任务 → 每天早上自动生成一张当日主题图
- 生产级考量：队列管理、并发控制、WebSocket 监听进度
- Comfy Cloud 云端 API：不想自己跑服务器时的备选

### 3.3 高级采样与调度器深度解析
- 采样器（Sampler）类型全景：Euler、DPM++ 2M/3M、DDIM、LCM、UniPC……
- 调度器（Scheduler）：Karras、Exponential、Simple、Beta……
- 不同采样器的速度与质量对照：什么场景用什么组合
- LCM（Latent Consistency Model）：4 步出图的技术原理与实践
- TAESD 潜在预览：生成过程中实时看到模糊预览（需要先装解码器到 `models/vae_approx`）
- 实战：同一张图用 5 种采样器组合跑一遍，对比输出结果

### 3.4 智能内存管理与大模型策略
- ComfyUI 的智能内存管理原理：
  - 自动检测显存 → 智能卸载不用的模型
  - 最低仅需 1GB 显存就能跑大模型
- 内存管理参数调优：
  - `--lowvram`：强制低显存模式
  - `--novram`：极限低显存（速度很慢）
  - `--normalvram`：标准模式
- 大模型的拆分加载策略
- 多 GPU 配置
- 实战：8GB 显存跑 Flux (12B+ 参数) 的策略
- 异步队列的智能缓存：只重新执行变更部分，不改的节点不重跑

### 3.5 Flux 与新一代模型：ComfyUI 上的前沿体验
- Flux 系列是什么、为什么在 ComfyUI 上首发支持
- Flux vs SDXL vs SD3.5 的生成质量对比
- 国产模型在 ComfyUI 上的支持：
  - HunyuanDiT（混元文生图）
  - Hunyuan Video 1.5（混元视频）
  - Hunyuan3D 2.0（混元 3D）
  - Qwen Image / Qwen Image Edit（通义万相）
  - HiDream（智象）
  - Wan 2.1/2.2（万兴视频）
- 实战：在 ComfyUI 上用混元视频生成一段中文 prompt 的短视频
- 音频生成：Stable Audio、ACE Step

---

## 第四部分：踩坑与最佳实践

### 4.1 安装与环境配置常见问题
- Windows 下的常见坑：Python 版本、CUDA 版本不匹配、PATH 环境变量
- macOS Apple Silicon：MPS 后端 vs CPU 模式
- AMD 显卡：Linux ROCm 比 Windows 靠谱得多
- PyTorch 版本与 GPU 驱动的对应关系速查
- `comfy-cli` 命令行工具的安装与诊断
- 启动失败的排查清单（端口占用、模型路径、显存不足）
- 前端版本选择：稳定版 vs nightly 每日构建

### 4.2 模型管理与存储规划
- 模型文件都放哪：`folder_paths.py` 与 `extra_model_paths.yaml` 配置
- 模型下载后的校验：md5/sha256 检查
- 模型组织策略：按用途分类（基础模型 / LoRA / VAE / ControlNet / Upscale）
- 磁盘空间管理：模型去重、定期清理旧版本
- 跨项目共享模型：配置 `extra_model_paths.yaml` 避免重复下载
- 安全加载：safetensors vs ckpt 的安全差异

### 4.3 工作流管理与版本控制
- 工作流 JSON 文件的命名与组织规范
- 工作流中的相对路径处理
- Git 管理 ComfyUI 工作流的实践
- 模型更新后工作流失效的排查与修复
- 社区工作流的安全检查：恶意节点、隐藏脚本
- App 模式：把复杂工作流包装成简单 UI 给非技术人员用

### 4.4 性能优化与效率提升
- 显存使用监控与瓶颈分析
- 队列管理：批量处理、优先级排序
- 节点缓存策略：哪些中间结果值得缓存
- 采样迭代调优：在质量和速度之间找最优解
- 预览方法对比：TAESD vs 内置预览，哪个更省资源
- 实战：一个 50 张图批量任务的最优配置
- 云端 vs 本地：成本与效率的决策矩阵

### 4.5 综合案例：自媒体博主的 ComfyUI 生产线
- 场景设定：一个公众号博主，每周产出 3 篇图文
- 工具链全景：
  - 选题 + 大纲 → AI 写作工具（本系列其他工具）
  - 封面图 + 插图 → ComfyUI 批量生成
  - 发布 → 公众号后台
- ComfyUI 侧的具体配置：
  - 品牌风格 LoRA（训练 1 次）
  - 封面图工作流（复用每周）
  - 插图工作流（替换 prompt 即可）
  - 批量队列（周日晚统一跑下周的图）
- 从"每张图 30 分钟找素材 + PS"到"10 分钟跑 20 张选最佳"
- 复盘：节省了多少时间、提升了多少质量

---

## 附录

### A. 常用快捷键速查表
- 节点操作、画布操作、队列管理、工作流保存/加载

### B. 模型与资源推荐
- 新手入门推荐模型（按硬件分级）
- 必装自定义节点清单
- 优质工作流社区与资源站
- Civitai / HuggingFace 搜索技巧

### C. 术语对照表
- Checkpoint / LoRA / VAE / ControlNet / Latent / CFG / Sampling Steps / Scheduler
- 中文解释 + 英文原名，方便新人看懂英文社区内容

### D. 官方资源与社区索引
- GitHub：https://github.com/Comfy-Org/ComfyUI
- 官方网站：www.comfy.org
- 前端仓库：ComfyUI Frontend
- 官方文档
- Discord / Matrix 社区
- Comfy Cloud

### E. 更新日志
- 跟随 ComfyUI 版本更新持续同步（当前基准：v0.24.0，周发布节奏）

---

*本大纲基于 Comfy-Org/ComfyUI 官方仓库（github.com/Comfy-Org/ComfyUI）信息与个人实践理解编写，内容为独立理解与表述。具体文章写作中如需引用官方原文或示例，将注明出处。大纲随 ComfyUI 版本更新持续迭代。*
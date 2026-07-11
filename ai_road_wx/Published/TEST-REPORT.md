# html-anything 测试报告

## 环境状态

| 组件 | 状态 |
|------|------|
| pnpm | ✅ 已安装 |
| 项目依赖 | ✅ 已安装 (165 packages) |
| CLI 构建 | ✅ 已构建 |
| Web 界面 | ✅ 运行中 (http://localhost:3000) |
| Claude Code CLI | ✅ 已安装 (v2.1.183) |
| AI Agent 检测 | ✅ 检测到 claude + openclaw |
| Claude CLI 认证 | ⚠️ 模型名映射问题 |

## 测试文件

生成了 3 个测试文件，分别对应 html-anything 的不同模板风格：

| 文件 | 对应模板 | 风格 |
|------|---------|------|
| `test-kami-parchment.html` | doc-kami-parchment | 暖羊皮纸 + 墨蓝 accent，适合公众号长文 |
| `test-article-magazine.html` | article-magazine | 杂志封面 + 分节正文，视觉冲击强 |
| `test-card-xiaohongshu.html` | card-xiaohongshu | 5 张 1080×1440 卡片，莫兰迪色系 |

## Web 界面使用方式

1. 浏览器打开 http://localhost:3000
2. 顶栏会显示检测到的 AI Agent（claude / openclaw）
3. 左侧粘贴 Markdown 内容
4. 中间选择模板（doc-kami-parchment、card-xiaohongshu 等）
5. 点击生成，右侧 iframe 实时预览
6. 一键导出：公众号 / 小红书 / 下载 HTML / PNG

当前 CLI Agent 因模型名映射问题暂时无法正常调用，Web 界面同理。
一旦 Claude CLI 能正常调用，Web 界面即可完全工作。

## 临时解决方案

修复 Claude CLI 认证后使用：
```bash
cd D:\html-anything-main
node cli/dist/run.js convert 你的文章.md -t doc-kami-parchment -o 输出.html
```

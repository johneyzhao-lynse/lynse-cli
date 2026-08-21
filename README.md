# 灵光记 (Lynse CLI)

<div align="center">

**🎯 智能会议管理命令行工具**

[![npm version](https://badge.fury.io/js/%40lynse.ai%2Flynse-cli.svg)](https://www.npmjs.org/package/@lynse.ai/lynse-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

</div>

## ✨ 功能特色

- 📋 **会议管理** - 查询、搜索、整理会议记录
- 🤖 **AI 总结** - 智能会议总结和转写
- 📁 **智能整理** - 自动分类会议到文件夹
- ✅ **待办管理** - 管理和清理待办事项
- 📱 **设备管理** - 管理绑定设备
- 🔌 **MCP 服务** - 已拆分到独立仓库 [lynse-mcp](https://github.com/lynse-ai/lynse-mcp)

## 🚀 快速开始

### 安装

#### 安装为 Agent Skill（推荐）

把下面这段说明直接发给 Codex、Claude Code、Cursor 或其他支持 Agent Skills 的 Agent：

> 请将“灵光记/lynse-cli”安装为当前 Agent 可发现的全局 Skill，而不是只临时运行 CLI。
>
> ```bash
> npx -y skills add lynse-ai/lynse-cli --skill lynse-cli --global
> ```
>
> API 服务器地址：`https://api.lynse.cn`。请将 `LYNSE_API_HOST=https://api.lynse.cn` 写入当前 Agent 支持的环境配置或已安装 Skill 的 `.env`；不要在 `.env` 中写入 API Key。
>
> 请根据当前 Agent 选择它支持的 Skill 目录。安装前确认 Node.js/npm 和 Python 3.11+ 可用；安装后确认 Agent 能发现 `lynse-cli`，并在 Skill 目录运行只读的 `<Python 3.11+> lynse.py version` 验证。需要认证时，请在本机终端启动 `<Python 3.11+> lynse.py auth login --host https://api.lynse.cn`，提示用户只在终端的隐藏输入框中输入 API Key；不要在对话或日志中索取、显示或输出 API Key。

如果当前 Agent 不支持 Skill 或没有 Shell、网络、目录写入权限，应说明缺少的条件，不要绕过权限。

#### 临时运行或全局安装 CLI

```bash
# 临时运行 CLI；不会安装 Agent Skill
npx -y @lynse.ai/lynse-cli@latest --help

# 全局安装 CLI
npm install -g @lynse.ai/lynse-cli

# Python 项目复用同一 API 客户端
python3 -m pip install "git+https://github.com/lynse-ai/lynse-cli.git@v1.8.0"

# 或使用安装脚本
# macOS/Linux
./install.sh

# Windows PowerShell
.\install.ps1
```

**API 服务器地址**: `https://api.lynse.cn`

### 配置

```bash
# 配置 API 密钥
lynse auth login

# 查看个人信息
lynse me
```

## 💻 基本使用

```bash
# 查看最近的会议
lynse meetings list

# 获取会议总结
lynse meetings summary <会议ID>            # 默认返回第一篇；--all 返回全部总结

# 整理会议到文件夹
lynse meetings organize --execute

# 管理待办事项
lynse todos list
```

## 📖 详细文档

- 📚 [完整使用指南](USAGE.md) - 小白友好的详细教程
- 🔧 [安装指南](install-guide.md) - 详细安装说明
- 📋 [命令参考](SKILL.md) - 完整命令列表
- 🔄 [更新日志](CHANGELOG.md) - 版本更新记录
- 🔌 [MCP 服务仓库](https://github.com/lynse-ai/lynse-mcp) - 独立的 MCP 服务项目

## 🌟 主要功能

### 1. 会议查询
```bash
lynse meetings list --days 7          # 最近7天会议
lynse meetings month 2026-04           # 指定月份会议
lynse meetings search 关键词          # 搜索会议
```

### 2. AI 智能功能
```bash
lynse meetings summary <ID>            # 获取第一篇 AI 总结（--all 获取全部）
lynse meetings outline <ID>           # 获取会议大纲
lynse meetings transcript <ID>        # 获取完整转写
lynse meetings audio <ID>             # 获取音频下载信息
```

### 3. 自动整理
```bash
lynse meetings organize                # 预览整理计划
lynse meetings organize --execute      # 执行整理
```

### 4. 待办管理
```bash
lynse todos list                       # 查看待办
lynse todos clear                      # 清理已完成
lynse todos reschedule <ID> 2026-08-15 # 调整截止时间
```

## 🔧 系统要求

- Python 3.11 或更高版本
- Windows / macOS / Linux
- 网络连接

## ❓ 获取帮助

```bash
lynse --help                          # 查看帮助
lynse version                         # 查看版本
lynse doctor                         # 系统诊断
```

## 📞 支持与反馈

- 🐛 [问题反馈](https://github.com/lynse-ai/lynse-cli/issues)
- 🌐 [官方网站](https://www.lynse.ai)
- 📧 邮箱: support@lynse.ai

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

<div align="center">

**[灵光记 Lynse](https://www.lynse.ai)** - 让会议管理更智能

Made with ❤️ by lynse.ai

</div>

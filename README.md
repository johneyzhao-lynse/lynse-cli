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
- 🔧 **AI 模型** - 配置和管理 AI 模型
- 🔌 **MCP 服务** - 已拆分到独立仓库 [lynse-mcp](https://github.com/lynse-ai/lynse-mcp)

## 🚀 快速开始

### 安装

```bash
# 推荐使用 npx 一键安装
npx -y @lynse.ai/lynse-cli@latest

# AI 助手环境添加 skill（OpenClaw 等）
npx skills add lynse-ai/lynse-cli

# 或全局安装
npm install -g @lynse.ai/lynse-cli

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
lynse meetings summary <会议ID>

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
lynse meetings summary <ID>            # 获取 AI 总结
lynse meetings outline <ID>           # 获取会议大纲
lynse meetings transcript <ID>        # 获取完整转写
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

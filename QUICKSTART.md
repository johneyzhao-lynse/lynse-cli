# 灵光记 (Lynse CLI) 快速入门

## 🎯 5分钟上手指南

### 第1步：安装（1分钟）

**推荐使用 npx 一键安装：**
```bash
npx -y @lynse.ai/lynse-cli@latest
```

**其他安装方式：**

```bash
# AI 助手环境添加 skill（OpenClaw 等）
npx skills add lynse-ai/lynse-cli

# 使用 npm 全局安装
npm install -g @lynse.ai/lynse-cli

# macOS/Linux 用户（安装脚本）
curl -sS https://raw.githubusercontent.com/lynse-ai/lynse-cli/main/install.sh | bash

# Windows 用户（PowerShell 安装脚本）
irm https://raw.githubusercontent.com/lynse-ai/lynse-cli/main/install.ps1 | iex
```

**API 服务器地址**: `https://api.lynse.cn`

### 第2步：登录（30秒）

```bash
lynse auth login
# 输入你的 API 密钥（格式：dk_xxx）
```

**获取 API 密钥：** 登录 [灵光记管理后台](https://www.lynse.ai) 获取

### 第3步：验证（30秒）

```bash
lynse me
# 应该显示你的个人信息
```

### 第4步：开始使用（3分钟）

```bash
# 查看最近的会议
lynse meetings list

# 获取某个会议的总结
lynse meetings summary <会议ID>

# 查看待办事项
lynse todos list

# 自动整理会议到文件夹
lynse meetings organize --execute
```

## 🎯 常用命令速查

| 功能 | 命令 |
|------|------|
| 个人信息 | `lynse me` |
| 最近会议 | `lynse meetings list` |
| 会议总结 | `lynse meetings summary <ID>` |
| 待办列表 | `lynse todos list` |
| 整理会议 | `lynse meetings organize` |
| 设备列表 | `lynse devices list` |
| 获取帮助 | `lynse --help` |

## 💡 实用示例

### 查看本周会议
```bash
lynse meetings list --days 7 --table
```

### 搜索特定会议
```bash
lynse meetings search 项目讨论
```

### 批量清理待办
```bash
lynse todos list done    # 查看已完成
lynse todos clear        # 清理已完成
```

### 自动整理会议
```bash
# 先预览计划
lynse meetings organize

# 确认后执行
lynse meetings organize --execute --yes
```

## 🆘 遇到问题？

### 安装问题
```bash
lynse doctor    # 运行系统诊断
```

### 认证问题
```bash
lynse auth status    # 检查登录状态
lynse auth login     # 重新登录
```

### 网络问题
- 检查网络连接
- 确认 API 服务器地址：`api.lynse.cn`

## 📚 更多帮助

- **完整教程**: [USAGE.md](USAGE.md)
- **安装指南**: [install-guide.md](install-guide.md)
- **问题反馈**: [GitHub Issues](https://github.com/lynse-ai/lynse-cli/issues)

---

**现在就开始使用灵光记，让会议管理更简单！** 🚀
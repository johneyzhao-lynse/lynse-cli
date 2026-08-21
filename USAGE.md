# 灵光记 (Lynse CLI) 使用指南

## 📖 简介

灵光记 (Lynse CLI) 是一款功能强大的命令行工具，帮助你管理会议记录、待办事项、文件整理等。支持 Windows、macOS 和 Linux 系统。

**主要功能：**
- 📋 会议记录查询和管理
- 📝 AI 智能总结和转写
- 📁 文件夹自动整理
- ✅ 待办事项管理
- 📱 设备管理

## 🚀 快速开始

### 第一步：安装

**推荐方式：安装为 Agent Skill**

将下面整段说明直接发给 Codex、Claude Code、Cursor 或其他支持 Agent Skills 的 Agent：

> 请将“灵光记/lynse-cli”安装为当前 Agent 可发现的全局 Skill，而不是只临时运行 CLI。
>
> ```bash
> npx -y skills add lynse-ai/lynse-cli --skill lynse-cli --global
> ```
>
> API 服务器地址：`https://api.lynse.cn`。请将 `LYNSE_API_HOST=https://api.lynse.cn` 写入当前 Agent 支持的环境配置或已安装 Skill 的 `.env`；不要在 `.env` 中写入 API Key。
>
> 安装前确认 Node.js/npm 和 Python 3.11+ 可用。安装后确认 Agent 能发现 `lynse-cli`，并在 Skill 目录运行只读的 `<Python 3.11+> lynse.py version` 验证。需要认证时，请在本机终端启动 `<Python 3.11+> lynse.py auth login --host https://api.lynse.cn`，提示用户只在终端的隐藏输入框中输入 API Key；不要在对话或日志中索取、显示或输出 API Key。

**临时运行 CLI（不会安装 Agent Skill）**

```bash
npx -y @lynse.ai/lynse-cli@latest --help
```

**其他安装方式：**

#### 使用 npm 全局安装
```bash
npm install -g @lynse.ai/lynse-cli
```

#### macOS/Linux 用户（使用安装脚本）
```bash
# 下载并运行安装脚本
./install.sh
```

#### Windows 用户（使用安装脚本）  
```powershell
# 在 PowerShell 中运行安装脚本
.\install.ps1
```

**API 服务器地址**: `https://api.lynse.cn`

### 第二步：配置 API 密钥

安装完成后，需要配置你的 API 密钥：

```bash
# 推荐方式：交互式输入（密码隐藏）
python3 lynse.py auth login

# 或者直接指定密钥
python3 lynse.py auth login --api-key 你的API密钥
```

**获取 API 密钥：**
- 登录灵光记管理后台
- 在系统设置中获取 API 密钥（格式：`dk_xxx`）

**验证配置：**
```bash
python3 lynse.py auth status
```

### 第三步：开始使用

```bash
# 查看个人信息
python3 lynse.py me

# 查看最近的会议记录
python3 lynse.py meetings list
```

## 💻 基本使用

### 系统要求
- Python 3.11 或更高版本
- 网络连接

### 命令格式

```bash
# macOS/Linux 用户
python3 lynse.py <命令> [参数]

# Windows 用户
python lynse.py <命令> [参数]
# 或者
py lynse.py <命令> [参数]
```

## 📋 主要功能详解

### 1. 会议管理

#### 查看会议记录
```bash
# 查看最近7天的会议
python3 lynse.py meetings list --days 7

# 查看指定月份的会议
python3 lynse.py meetings month 2026-04

# 查看指定周的会议
python3 lynse.py meetings week 2026-W16

# 查看日期范围的会议
python3 lynse.py meetings range 2026-04-01 2026-04-30

# 搜索会议
python3 lynse.py meetings search 关键词
```

#### 获取会议详情
```bash
# 获取会议转写文本
python3 lynse.py meetings transcript <会议ID>

# 获取 AI 总结（默认第一篇；追加 --all 获取全部）
python3 lynse.py meetings summary <会议ID> [--all]

# 获取会议大纲
python3 lynse.py meetings outline <会议ID>

# 查看会议详细信息
python3 lynse.py meetings info <会议ID>
```

#### 自动整理会议到文件夹
```bash
# 预览整理计划（安全模式，不实际操作）
python3 lynse.py meetings organize

# 整理最近90天的会议
python3 lynse.py meetings organize --days 90

# 执行整理（非交互模式）
python3 lynse.py meetings organize --execute --yes
```

**整理功能说明：**
- 默认使用安全模式，只显示计划不执行
- 按会议主题自动分类到文件夹
- 重复使用现有文件夹，创建新文件夹（图标+6字符名称）
- 最多创建10个主题文件夹 + 1个"其他"文件夹

### 2. 待办事项管理

```bash
# 查看所有待办事项
python3 lynse.py todos list

# 只看未完成的待办
python3 lynse.py todos list open

# 只看已完成的待办
python3 lynse.py todos list done

# 删除指定待办事项
python3 lynse.py todos delete <待办ID>

# 清理所有已完成的待办
python3 lynse.py todos clear
```

### 3. 文件夹管理

```bash
# 列出所有文件夹
python3 lynse.py folders list

# 创建文件夹（JSON格式）
python3 lynse.py folders create '{"name":"项目文档","icon":"📁"}'

# 移动文件到文件夹
python3 lynse.py folders move '{"folderId":"xxx","fileIds":["id1","id2"]}'

# 删除空文件夹（命令会先用服务端统计和完整文件清单确认为空）
python3 lynse.py folders delete <文件夹ID>
```

`folders delete` 采用整批拒绝策略：只要任意目标文件夹非空、不存在、统计异常或无法确认，整批都不会发送删除请求。不能根据本地整理计划推断文件夹为空。

### 4. 设备管理

```bash
# 查看绑定的设备列表
python3 lynse.py devices list

# 查看设备详情
python3 lynse.py devices info <设备ID>

# 解绑设备
python3 lynse.py devices unbind <设备ID>
```

### 5. 账户和认证

```bash
# 查看个人信息
python3 lynse.py me

# 登录配置
python3 lynse.py auth login

# 查看认证状态
python3 lynse.py auth status

# 退出登录
python3 lynse.py auth logout

# 诊断认证问题
python3 lynse.py auth doctor
```

## 🎨 输出格式控制

```bash
# JSON 格式（默认管道输出）
python3 lynse.py meetings list --json

# 美化的 JSON（默认终端输出）
python3 lynse.py meetings list --pretty

# 文本格式摘要
python3 lynse.py meetings list --text

# 表格格式
python3 lynse.py meetings list --table

# 保存到文件
python3 lynse.py meetings list --output 会议列表.txt
```

**组合使用示例：**
```bash
# 以表格形式显示并保存到文件
python3 lynse.py meetings list --table --output 本周会议.txt
```

## 🔍 系统诊断

```bash
# 查看版本信息
python3 lynse.py version

# 完整环境诊断
python3 lynse.py doctor

# 更新说明
python3 lynse.py update
```

## ❓ 常见问题解答

### 安装问题

**Q: 提示 "python: command not found"？**

**macOS/Linux 解决方案：**
```bash
# 大多数现代系统使用 python3
python3 lynse.py me
```

无需修改任何 shell 启动文件。

**Windows 解决方案：**
```bash
# 使用 py 启动器
py lynse.py me

# 或重新安装 Python 并勾选 "Add Python to PATH"
```

### 认证问题

**Q: 提示 "API Key authentication failed"？**

```bash
# 1. 检查认证状态
python3 lynse.py auth status

# 2. 重新登录
python3 lynse.py auth login --api-key 你的正确密钥

# 3. 运行诊断
python3 lynse.py auth doctor
```

**Q: API 密钥格式？**

API 密钥格式为 `dk_` 开头，例如：`dk_abc123def456`

### 网络问题

**Q: 提示连接超时或网络错误？**

```bash
# 检查网络连接
ping api.lynse.cn

# 如果使用代理，配置环境变量
export LYNSE_API_HOST=https://api.lynse.cn
```

### 权限问题

**Q: Windows 上提示权限错误？**

```powershell
# 以管理员身份运行 PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📞 获取帮助

- **GitHub 问题反馈**: https://github.com/lynse-ai/lynse-cli/issues
- **官方网站**: https://www.lynse.ai
- **查看详细文档**: `python3 lynse.py doctor`

## 💡 使用技巧

### 1. 创建快捷命令（可选）

**macOS/Linux:**
```bash
# 仅在当前终端会话中创建临时函数
alias lynse='python3 lynse.py'

# 使用
lynse meetings list
lynse me
```

也可以通过 npm 安装后直接使用持久的 `lynse` 命令，无需修改 shell 配置。

**Windows:**
```powershell
# 在 PowerShell 配置文件中添加
function lynse { python C:\path\to\lynse.py $args }

# 使用
lynse meetings list
```

### 2. 批量操作

```bash
# 将会议列表导出为 CSV
python3 lynse.py meetings list --json > meetings.json

# 整理所有会议并查看计划
python3 lynse.py meetings organize --days 365
```

### 3. 定期维护

```bash
# 清理已完成待办
python3 lynse.py todos clear

# 查看设备绑定状态
python3 lynse.py devices list
```

## 🚨 错误代码说明

| 错误代码 | 含义 | 常见原因 | 解决方法 |
|---------|------|---------|----------|
| 0 | 成功 | 正常完成 | - |
| 1 | 参数错误 | 命令参数错误 | 检查命令语法 |
| 2 | 认证失败 | API密钥无效或过期 | 重新登录认证 |
| 3 | 网络错误 | 连接失败 | 检查网络连接 |
| 4 | 超时 | 请求超时 | 重试或检查网络 |
| 5 | 权限不足 | 没有操作权限 | 联系管理员 |
| 6 | 服务器错误 | API 服务异常 | 稍后重试 |

## 📚 相关文档

- [安装指南](install-guide.md) - 详细安装说明
- [开发文档](SKILL.md) - 技术参考文档
- [更新日志](CHANGELOG.md) - 版本更新记录
- [兼容性说明](compatibility.md) - 系统兼容性信息

## 🎉 开始使用

现在你已经了解了灵光记 CLI 的基本使用方法，开始体验智能会议管理吧！

```bash
# 查看最近的会议
python3 lynse.py meetings list --days 7 --table

# 查看你的待办事项
python3 lynse.py todos list

# 查看个人信息
python3 lynse.py me
```

---

**版本**: v1.6.3  
**更新日期**: 2026-06-29  
**官方支持**: https://www.lynse.ai

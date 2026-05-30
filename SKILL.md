---
name: lynse-cli
description: 灵光记 / Lynse / lynse-cli 通用技能，调用 lynse.ai 后端服务的 API。当用户需要查询灵光记或 Lynse 账户信息、文件、转写、总结、大纲、积分、待办/任务、设备、AI 模型、团队协作、消息时使用此技能。即使只是简单查个灵光记积分、待办或文件列表，也应使用此技能。
version: 1.3.5
metadata:
  openclaw:
    requires:
      env:
        - LYNSE_API_HOST
        - LYNSE_API_KEY
      bins:
        - python
        - python3
        - py
    platforms:
      - macOS
      - Linux
      - Windows
    primaryEnv: LYNSE_API_KEY
    homepage: https://www.lynse.ai
    emoji: "\U0001F4CB"
---

# 灵光记 / Lynse CLI Skill

✅ 跨平台支持 (v1.3.5) — Python 3.8+，原生支持 Windows/macOS/Linux

`灵光记 = Lynse = lynse-cli`。用户说"灵光记"就是在请求本技能。

**典型触发词：**
- "查一下灵光记文件 / 灵光记总结 / 灵光记转写 / 灵光记大纲"
- "整理灵光记待办 / 待办事项"
- "看看我的灵光记积分 / 账户信息 / 手机号"
- "Lynse files / Lynse todos / lynse-cli get conclusion"

> ⚠️ 内部技术名、目录名保持 `lynse-cli` / `lynse.py`，不要改成中文路径，以保证 Codex、Claude Code、OpenClaw、Hermes 等 agent 稳定发现。

---

## 目录

- [快速部署](#快速部署)
- [Agent 必读约束](#-agent-必读约束)
- [调用方式](#调用方式)
- [常用操作（速查）](#-常用操作速查)
- [端到端场景工作流](#-端到端场景工作流)
  - [场景 A：查账户信息](#场景-a用户查积分手机号账户信息)
  - [场景 B：查文件+转写/总结](#场景-b用户查文件看转写总结)
  - [场景 C：查看待办清单](#场景-c查看待办清单)
  - [场景 D：按截止时间整理待办](#场景-d按截止时间整理待办)
  - [场景 E：按负责人筛选待办](#场景-e按负责人筛选待办)
  - [场景 F：自动修改发言人名称](#场景-f自动修改发言人名称)
- [认证流程](#认证流程)
- [反例与黑名单](#-反例与黑名单)
- [实战踩坑记录（Pitfalls）](#-实战踩坑记录pitfalls)
- [文件结构](#文件结构)
- [更新日志](#更新日志)

---

## 快速部署

**🔴 CHECKPOINT：安装前先确认目标环境（macOS/Linux/Windows），选择下方对应命令。**

### 自动安装（推荐）

```bash
# macOS/Linux
./install.sh

# Windows PowerShell
.\install.ps1
```

安装脚本会：检测当前 AI 助手环境 → 复制文件到对应 skills 目录 → 创建 `.env` → 安装依赖 → 设置权限。

### 手动安装

1. 复制 `lynse-cli` 目录到目标实例的 `skills` 目录
2. 复制 `.env.example` 为 `.env`，填入 `LYNSE_API_HOST` 和 `LYNSE_API_KEY`
3. 运行 `pip install -r requirements.txt` 安装依赖

**各环境 Skills 目录：**

| 环境 | Skills 目录 |
|------|------------|
| Hermes | `~/.hermes/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |
| OpenClaw | `~/.openclaw/workspace/skills/` |

### Windows 专项

```powershell
# Python 安装：https://www.python.org/downloads/（勾选 Add Python to PATH）
python -c "import requests" 2>$null || pip install requests
python lynse.py getCurrentCustomer
```

> 若 `python` 找不到，用 `py -3` 替代。无需 Git Bash 或 WSL。

---

## ⚠️ Agent 必读约束

### 🌐 Base URL

`$LYNSE_API_HOST` — 通过环境变量配置，绝不硬编码。不要猜测或自行构造地址。

### 🔑 认证

Lynse 使用 **API Key + 临时 Token** 双层认证：

```
POST $LYNSE_API_HOST/api/auth/apikey/token
Header: X-API-Key: $LYNSE_API_KEY

→ 返回 accessToken（有效期 2 小时，自动刷新）
→ 后续调用 Header: Authorization: <accessToken>（不带 Bearer 前缀）
```

**🔴 CHECKPOINT：每次调用前检查 `$LYNSE_API_KEY` 和 `$LYNSE_API_HOST` 是否存在。**
- 不存在 → **🛑 STOP**，提示用户完成配置后再继续
- Token 过期（401）→ 自动刷新后重试
- Token 刷新失败 → **🛑 STOP**，提示检查 API Key

**环境变量配置方法：**
```bash
# macOS/Linux
export LYNSE_API_HOST="https://your-api-host/api"
export LYNSE_API_KEY="dk_your_api_key_here"

# Windows PowerShell
$env:LYNSE_API_HOST="https://your-api-host/api"
$env:LYNSE_API_KEY="dk_your_api_key_here"

# 或使用 .env 文件（所有平台通用）
cp .env.example .env    # macOS/Linux
copy .env.example .env  # Windows CMD
```

配置完成后再继续执行用户原本的请求。

### 🔐 Scope 权限

不同操作需要对应权限，权限由 API Key 绑定的角色决定：

| Scope | 说明 | 典型操作 |
|-------|------|----------|
| `customer.read` | 读取用户信息 | getCurrentCustomer, getUserInfo |
| `customer.write` | 编辑用户 | addUser, editUser, removeUser |
| `file.read` | 读取文件/转写/总结/待办 | listFiles, getFileInfo, getConclusion, getOutline, listTodos |
| `file.write` | 编辑文件内容 | editConclusion, editOutline, editTransRecord |
| `device.read` | 读取设备信息 | getDeviceInfo, getDevicePage |
| `device.manage` | 管理设备 | unbindDevice |
| `ai.read` | 查看 AI 模型 | getAiModels |
| `ai.manage` | 管理 AI 模型 | addModel, editModel, deleteModel, enableModel |
| `message.send` | 发送消息 | sendSms, sendEmail |
| `team.read` | 查看团队 | listMyTeam |
| `team.manage` | 管理团队 | createTeam, editTeam, removeTeamMember |

**🔴 CHECKPOINT：API 返回 403 时** → 回复「您的账户权限不足，请联系管理员升级权限」，不要尝试其他操作。

### 🔒 安全规则

- 不在群聊/公开场合主动展示用户手机号、积分等敏感字段
- 手机号默认脱敏显示：`138****1234`
- `LYNSE_OWNER_ID` 校验：当前用户 ID 不匹配时回复「抱歉，这是私密账户，我无法操作」
- Token 缓存文件权限必须为 600（仅所有者可读写）
- 创建/编辑操作间隔 1 分钟以上，避免触发服务端限流

### ⚠️ 错误处理规则（三段式：触发 → 一线修复 → 兜底）

| 触发条件 | 一线修复（自动） | 仍失败兜底（人工） |
|----------|-----------------|-------------------|
| 401 — Token 过期 | 自动用 API Key 刷新 Token 后重试 | 刷新失败 → **🛑 STOP** → 提示检查 `LYNSE_API_KEY` |
| 403 — 权限不足 | 停止当前操作，回复「权限不足，请联系管理员」 | 用户申请权限后重试 |
| 429 — 请求限流 | 自动等待 60 秒后重试 | 仍 429 → 提示「请求过于频繁，请稍后再试」 |
| 404 — 资源不存在 | 重新列举资源列表，确认 ID 是否正确 | 确认 ID 后仍 404 → 提示「请求的资源不存在」 |
| 500/502/503 — 服务器错误 | 等待 5 秒后重试 1 次 | 仍失败 → 提示「服务器暂时不可用，请稍后重试」 |
| Token 刷新失败 — API Key 无效 | 清除 Token 缓存，重新换取 | 仍失败 → **🛑 STOP** → 提示用户从控制台重新获取 API Key |
| 接口返回 `code != 200` | 读取错误信息，自动修复常见问题 | 无法自动修复 → 展示错误详情 + 解决建议 |

**错误响应格式：** 1️⃣ 说明错误 2️⃣ 分析原因 3️⃣ 提供解决建议

### 🎯 端到端场景工作流

以下是三种最常见用户请求的完整执行步骤。按序号依次执行。

#### 场景 A：用户查积分/手机号/账户信息

```
Step 1: 检查 LYNSE_API_HOST / LYNSE_API_KEY → 若不存在 → 🛑 STOP → 提示配置
Step 2: 确认用户意图——具体要查什么？
        2a. "积分" → python lynse.py getUserPoints
        2b. "手机号" → python lynse.py getUserPhone
        2c. "账户信息" → python lynse.py getCurrentCustomer
Step 3: 执行命令 → 成功 → 返回结果给用户 (手机号脱敏)
        执行命令 → 401 → 自动刷新 Token → 重试
        执行命令 → 其他错误 → 查错误处理表 → 执行修复
Step 4: 🛑 在群聊中 → 自动隐藏手机号/积分等敏感字段
```

#### 场景 B：用户查文件+看转写/总结

```
Step 1: 检查认证是否就绪 → 如未配置 → 🛑 STOP
Step 2: 用户指定了时间范围？
        是 → python lynse.py listFilesByTimeRange [天数]
        否 → python lynse.py listFiles (默认全部)
Step 3: 展示文件列表（文件名+ID+时间）→ 让用户选择具体文件
Step 4: 用户选了文件后，确认要做什么？
        4a. "转写" → python lynse.py getTranscriptionRecord <fileId>
        4b. "总结" → python lynse.py getConclusion <fileId>
                  ⚠️ 返回 HTML，需用正则提取纯文本（见 Pitfalls 节）
        4c. "大纲" → python lynse.py getOutline <fileId>
                  ⚠️ data 返回字典（非数组），见 Pitfalls 节
Step 5: 格式化输出 → 返回给用户
```

#### 场景 C：查看待办清单

用户说「看看我的待办/查待办/有什么待办」时：

```
Step 1: 检查认证 → 如未配置 → 🛑 STOP
Step 2: 确认用户要什么范围？
        2a. 只想看未完成的 → python lynse.py listTodos 100 open
        2b. 全部（含已完成）→ python lynse.py listTodos 100 all
        2c. 只看已完成的 → python lynse.py listTodos 100 done
Step 3: 展示待办列表
        格式：「[待办内容] — 负责人: [owner] — 截止: [时间] — 文件: [fileId]」
Step 4: 如用户问"某个待办详情" → 打开对应 fileId 查 getFileInfo + getOutline
```

#### 场景 D：按截止时间整理待办

用户说「整理待办/按时间分组/哪些快过期了」时：

```
Step 1: 调用 python lynse.py organizeTodos [all|open|done]
        响应示例（真实数据）：
        {
          "total": 27,           // 总待办数
          "summary": {
            "expired": 0,        // 已过期
            "nearWeek": 0,       // 未来7天
            "nearMonth": 0,      // 未来30天
            "future": 0,         // 30天后
            "noDate": 27         // 无截止时间
          },
          "groups": { ... }      // 每组内详细待办列表
        }
Step 2: 优先汇报过期和近期待办
        2a. expired > 0 → 🔴 红色高亮提醒用户
        2b. nearWeek > 0 → 🟡 橙色提示本周要处理
        2c. 全部在 noDate → 建议用户设置截止时间
Step 3: 提取每条待办的 todoContent、owner、fileId，方便用户跳转到原始会议
Step 4: 🛑 禁止从转写/总结中二次抽取待办

特殊情况处理：
- total = 0 → 提示「暂无待办事项」
- noDate 占比 > 80% → 建议用户在灵光记 APP 中补充截止时间
- 大量待办（>50条）→ 按 owner 分组展示，方便分配责任人
```

#### 场景 E：按负责人筛选待办

用户说「查某人的待办/看谁负责什么」时：

```
Step 1: python lynse.py listTodos 200 all
Step 2: 遍历结果，按 owner 字段分组
        示例：发言人的待办 → 哪些 owner="发言人1"，哪些是空的
Step 3: 按用户指定的负责人名筛选
        3a. 有明确负责人 → 只看该负责人的条目
        3b. 无负责人（owner=""）→ 提醒用户分配负责人
Step 4: 输出格式：
        「[负责人名] 共 N 条待办：
          1. [待办内容] — 文件: [fileId]
          2. ...」
Step 5: 可选：调用 python lynse.py countTodos 获得统计数据备用
```

#### 🔴 待办操作通用规则（所有场景通用）

| 场景 | 规则 |
|------|------|
| 待办来源 | 只读后端 `listTodos` / `organizeTodos` 数据，**绝不自作主张从转写中提取** |
| 数据量 | 默认每页 100 条，不够用 `listTodos 200 all` 扩页 |
| 敏感信息 | 不展示 `fileId` 以外原始路径，不推送待办内容到群聊之外 |
| 空数据 | `data: []` → 友好提示，不报错 |
| organizeTodos 分组结构 | `expired`(过期) / `nearWeek`(7天内) / `nearMonth`(30天内) / `future`(30天后) / `noDate`(无截止) |

#### 场景 F：自动修改发言人名称

用户说「把发言人XXX改成XXX/改发言人名字/发言人写错了」时：

```
Step 1: 确认用户要改的文件（会议）
        1a. 用户给了文件/会议名 → 查 listFiles 找到 fileId
        1b. 用户没指定 → 列出最近文件让用户选
Step 2: 🔴 CHECKPOINT：确认要改什么
        确认旧发言人名称（oldName）和新名称（newName）
Step 3: 执行改名
        python lynse.py renameSpeaker '{
          "meetingId": "<fileId>",
          "oldName": "发言人1",
          "newName": "张三"
        }'
Step 4: 验证结果
        调用 getTranscriptionRecord <fileId>
        检查 speakerInfoList 中是否已替换为新名称
Step 5: 返回确认信息给用户
```

`renameSpeaker` 高级用法：

| 参数 | 必填 | 示例 | 说明 |
|------|------|------|------|
| `meetingId` 或 `fileId` | ✅ | `"1993855667662958593_xxx"` | 会议/文件 ID |
| `oldName` | ✅ | `"发言人1"` | 要替换的旧发言人名称 |
| `newName` | ✅ | `"张三"` | 替换后的新名称 |
| `taskId` | ❌ | `"task_xxx"` | 可选，精确指定转写任务 |
| `teamId` | ❌ | `"team_xxx"` | 可选，指定团队空间 |

> 如需要更精细的批量修改，用 `editSpeakerInfo` 直接提交 speakerInfoList JSON。

🔴 安全规则：改发言人前先调用 `getTranscriptionRecord` 确认原始 speaker 列表，避免误改。**不要在群聊中直接展示原始转写内容**（仅展示 speaker 名称列表）。

- **lynse-cli-a**（基础版）：核心认证（login, register, token 管理）
- **lynse-cli-b**（增强版）：完整业务（文件、团队、AI、设备）

`lynse_cli.py` 自动检测并路由到可用版本。详见 [compatibility.md](compatibility.md)。

---

## 调用方式

**命令格式（所有平台通用）：**
```bash
python lynse.py <command> [参数...]
python3 lynse.py <command> [参数...]    # macOS/Linux 优先
py -3 lynse.py <command> [参数...]      # Windows 回退
python lynse_cli.py <command> [参数...]
```

> **不要求所有启动器都可用**——有 Python 3.8+ 即可运行。`python` 失败时换 `python3` 或 `py -3`。

**不要**使用 `./lynse_unified.sh` / `./api_wrapper.sh`——不兼容 Windows，仅保留向后兼容。

---

## 🔹 常用操作（速查）

### 用户信息
```bash
python lynse.py getCurrentCustomer          # 当前用户完整信息
python lynse.py getUserPhone                # 手机号
python lynse.py getUserPoints               # 积分（含已用）
python lynse.py getUserInfo <用户ID>         # 指定用户信息
python lynse.py getCurrentUser              # 当前系统用户
```

### 文件管理
```bash
python lynse.py listFiles                         # 所有文件列表
python lynse.py listFilesPaged [pageSize]         # 分页获取全部文件
python lynse.py listFilesByTimeRange [天数]       # 按时间范围（默认7天）
python lynse.py getFileInfo <fileId>              # 文件详情
python lynse.py getTranscriptionRecord <fileId>   # 转写记录
python lynse.py getConclusion <fileId>            # 文件总结（注意：返回HTML）
python lynse.py getOutline <fileId>               # 文件大纲
python lynse.py exportOutline <fileId>            # 导出大纲
python lynse.py renameSpeaker '<JSON>'            # 自动修改发言人名称（传 meetingId+oldName+newName）
python lynse.py editSpeakerInfo '<JSON>'          # 直接提交发言人批量更新
```

### 待办/任务整理
```bash
python lynse.py listTodos [pageSize] [all|open|done]   # 读取待办
python lynse.py countTodos                              # 统计待办
python lynse.py organizeTodos [all|open|done]           # 按截止时间分组
```

**🛑 STOP：待办能力只读取和整理后端已生成的待办，不从转写或总结中二次抽取。** 避免模型判断造成不稳定结果。

`organizeTodos` 分组结构：`expired`（已过期）/ `nearWeek`（7天内）/ `nearMonth`（30天内）/ `future`（30天后）/ `noDate`（无截止时间）

### AI 模型管理
```bash
python lynse.py getAiModels                        # 所有模型列表
python lynse.py addModel '<JSON>'                  # 添加模型
python lynse.py editModel '<JSON>'                 # 编辑模型
python lynse.py deleteModel <模型ID>                # 删除模型
python lynse.py enableModel <模型ID> <true/false>  # 启用/禁用
```

### 设备管理
```bash
python lynse.py getDevicePage <页码>      # 分页设备列表
python lynse.py getDeviceInfo <设备ID>     # 设备详情
python lynse.py unbindDevice <设备ID>      # 解绑设备
```

### 用户管理（需 customer.write 权限）
```bash
python lynse.py addUser '<JSON>'          # 添加用户
python lynse.py editUser '<JSON>'         # 编辑用户
python lynse.py removeUser <用户ID>        # 删除用户
```

### 认证（推荐 API Key 自动认证）
```bash
python lynse.py login <用户名> <密码>              # 用户名密码登录
python lynse.py loginWithPhone <手机号> <验证码>   # 手机号登录
python lynse.py logout                              # 登出
```

### 消息
```bash
python lynse.py sendSms '<JSON>'         # 发送短信
python lynse.py sendEmail '<JSON>'       # 发送邮件
```

### 系统
```bash
python lynse.py getRoleList              # 角色列表
python lynse.py getMenuTree              # 菜单树
```

---

## 认证流程

```
用户请求 → lynse.py
  → 🔴 CHECKPOINT: 检查 LYNSE_API_HOST / LYNSE_API_KEY
    → 不存在 → 🛑 STOP → 提示配置 → 用户配置后重试
    → 存在 → 检查缓存 Token
      → Token 有效 → 直接调用业务接口
      → Token 无效/过期 → POST /api/auth/apikey/token 换取新 Token
        → 成功 → 缓存（权限 600）→ 调用业务接口
        → 失败 → 🛑 STOP → 提示检查 API Key
```

---

## 🚫 反例与黑名单

以下为 **常见错误做法**，agent 执行时严格避免：

| # | 不要做 | 为什么 | 替代做法 |
|---|--------|--------|----------|
| 1 | 硬编码 Base URL | 服务器地址可能变更；各部署环境地址不同 | 必须从 `$LYNSE_API_HOST` 读取 |
| 2 | 手动构造 API 路径 | API 版本升级后路径可能变化 | 使用 `lynse.py` 封装命令，不要拼 URL |
| 3 | 直接用 Token 请求头加 `Bearer` 前缀 | Lynse API 不接受 Bearer 前缀，会 401 | 仅传裸 `accessToken` 值 |
| 4 | 在公开群聊展示用户手机号/积分 | 隐私泄露；违反数据保护规范 | 手机号脱敏 `138****1234`，积分不展示 |
| 5 | 从转写/总结中二次抽取待办 | 模型判断引入虚假待办，结果不稳定 | 只调用 `listTodos` / `organizeTodos` 读取后端已有数据 |
| 6 | 忘记检查 Python 版本兼容 | `python` 指向 Python 2 时语法报错 | 确认 Python 3.8+，失败时换 `python3` 或 `py -3` |
| 7 | `.env` 不存在时不报错静默继续 | API 调用全部失败，用户困惑 | **🛑 STOP**，提示创建 `.env` 并填写必要变量 |
| 8 | Token 失效时不重试直接报错 | 影响用户体验，增加 401 频次 | 自动 POST 刷新 Token 后重试，仅刷新失败才提示用户 |

---

## 🪤 实战踩坑记录（Pitfalls）

### JSON 解析含非法控制字符
API 返回的 JSON 中包含 `\x00-\x1f` 等控制字符，标准 `json.loads()` 会抛出 `Invalid control character` 异常。
**修复：** 使用 `json.loads(output, strict=False)` 或预清理：
```python
import re
output = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', output)
data = json.loads(output)
```

### getConclusion 返回 HTML 格式
`getConclusion <fileId>` 的结论内容存储在 `conclusionText` 字段（非 `content`），且为完整 HTML。
**提取纯文本：**
```python
import re
text = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL|re.IGNORECASE)
text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL|re.IGNORECASE)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'\s+', ' ', text).strip()
```

### 返回值类型不一致
- `getConclusion` 的 `data` 字段返回**数组** → 取 `data[0]` 再访问字段
- `getOutline` 的 `data` 字段返回**字典** → 直接访问

```python
data = json.loads(output, strict=False)

# getConclusion → 数组
items = data.get('data', [])
if items:
    content = items[0].get('conclusionText', '')

# getOutline → 字典（防御性处理数组情况）
d = data.get('data')
if isinstance(d, list) and len(d) > 0:
    d = d[0]
content = d.get('outlineText', '') if d else ''
```

### API Key 配置问题
`.env` 文件中 API Key 可能是截断占位符（如 `dk_b12...58ef`），需用户从控制台获取完整值后通过 `write_file` 写入（`patch` 可能因字符串匹配失败）。

### API Key 过期
Key 有效期 1-2 周，过期后返回 `code: 500, msg: "error.api.key.invalid"`。需从 Lynse 控制台重新获取。

---

## 文件结构

```
lynse-cli/
├── SKILL.md              # 本文档
├── lynse.py              # 核心 API 封装模块
├── lynse_cli.py          # CLI 命令入口
├── requirements.txt      # Python 依赖
├── install.sh            # macOS/Linux 安装脚本
├── install.ps1           # Windows 安装脚本
├── .env                  # 配置文件
├── .env.example          # 配置模板
├── lynse_unified.sh      # Shell CLI（向后兼容）
├── api_wrapper.sh        # Shell API 包装器（向后兼容）
├── lynse.bat             # Windows .bat 包装器（向后兼容）
├── references/
│   └── compatibility.md  # CLI 版本命令对照表
└── customer/
    ├── file/
    └── admin/
```

---

## 更新日志

### v1.3.5 (2026-05-30)
- ✅ 新增场景 F：自动修改发言人名称（renameSpeaker 完整工作流 + 参数表）
- ✅ 文件管理新增 renameSpeaker / editSpeakerInfo 命令
- ✅ 端到端场景增至 6 个（A:账户/B:文件/C:待办清单/D:按时间整理/E:按负责人/F:改发言人）

### v1.3.4 (2026-05-30)
- ✅ 扩展端到端场景：待办操作拆分为 3 个独立场景（查看清单/按时间整理/按负责人筛选）
- ✅ 新增待办通用规则表（来源限制/数据量/敏感信息/空数据处理）
- ✅ 修复 API Host（旧 IP → https://api.lynse.cn）

### v1.3.3 (2026-05-30)
- ✅ 新增 🎯 端到端场景工作流（3 个典型场景：查账户→查文件→整理待办，带完整 Step-by-step）
- ✅ 升级错误处理表为三段式（触发条件→一线修复→兜底），覆盖 7 种异常场景
- ✅ 提升 Dim2（工作流清晰度）+ Dim3（失败模式编码）

### v1.3.2 (2026-05-30)
- ✅ 去全局冗余：合并 Windows 安装指南和快速部署，删除重复的"各环境安装路径"表
- ✅ 新增 🔴 CHECKPOINT / 🛑 STOP 显性检查点标记（配置检查、Token 过期、权限不足）
- ✅ 新增 🚫 反例与黑名单章节（8 条"不要做"规则）
- ✅ 新增 🪤 实战踩坑记录（JSON控制字符、getConclusion HTML、返回值类型不一致、API Key过期）
- ✅ 新增目录导航
- ✅ 精简 430 行 → ~310 行（去重合并）

### v1.3.1 (2026-05-17)
- 中英文语境兼容；新增 listTodos/countTodos/organizeTodos 待办能力；文档改为自动选择 python/python3/py -3

### v1.3.0 (2026-04-17)
- Python 跨平台支持（Windows/macOS/Linux）；新增 lynse.py 和 lynse_cli.py；新增 install.ps1

### v1.2.1
- 支持 API 服务器地址自动提取

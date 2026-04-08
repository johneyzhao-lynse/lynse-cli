# Admin (设备/模型/系统管理)

> Prerequisites: see root `../SKILL.md` for setup, auth, and API call method.

## 模块决策表

| 用户意图 | 子模块 | 读取 |
|---|---|---|
| 设备列表、设备详情、解绑设备 | 设备管理 | 下方「设备管理」 |
| AI 模型列表、增删改、启用/禁用 | AI 模型管理 | 下方「AI 模型管理」 |
| 文件夹创建/编辑/排序、文件分类 | 文件夹管理 | 下方「文件夹管理」 |
| 团队创建/编辑/成员管理 | 团队管理 | 下方「团队管理」 |
| 角色、菜单、消息发送 | 系统管理 | 下方「系统管理」 |
| 翻译、转写语言、积分日志 | 其他功能 | 下方「其他功能」 |

---

## 设备管理

API base path: `/deviceMgt`

| 用户意图 | Wrapper命令 | HTTP | 路径 | 关键参数 |
|---|---|---|---|---|
| 分页获取设备列表 | `getDevicePage <pageNum>` | GET | `/deviceMgt/page9` | Header: `pageNum`, `pageSize:10` |
| 获取设备详情 | `getDeviceInfo <deviceId>` | GET | `/deviceMgt/info5` | Header: `id: <deviceId>` |
| 解绑设备 | `unbindDevice <deviceId>` | POST | `/deviceMgt/unbind` | Header: `id: <deviceId>` |
| 设备绑定状态 | CLI B: `isBound` | GET | — | — |
| 我的绑定设备列表 | CLI B: `listMyBindingDeviceList` | GET | — | — |
| 更新设备信息 | CLI B: `update` | — | — | Body |

```bash
# 查看设备列表（第1页）
~/.claude/skills/lynse/api_wrapper.sh getDevicePage 1

# 查看设备详情
~/.claude/skills/lynse/api_wrapper.sh getDeviceInfo "<deviceId>"

# 解绑设备
~/.claude/skills/lynse/api_wrapper.sh unbindDevice "<deviceId>"
```

---

## AI 模型管理

API base path: `/ai`

| 用户意图 | Wrapper命令 | HTTP | 路径 | 关键参数 |
|---|---|---|---|---|
| 获取所有 AI 模型 | `getAiModels` | GET | `/ai/getAllAIModelList` | 无 |
| 添加 AI 模型 | `addModel <json>` | POST | `/ai/addModel` | Body: JSON |
| 删除 AI 模型 | `deleteModel <modelId>` | DELETE | `/ai/deleteModel` | Header: `id: <modelId>` |
| 编辑 AI 模型 | `editModel <json>` | POST | `/ai/editModel` | Body: JSON |
| 启用/禁用模型 | `enableModel <id> <true/false>` | POST | `/ai/enableModel` | Header: `id`, `enabled` |

```bash
# 列出所有 AI 模型
~/.claude/skills/lynse/api_wrapper.sh getAiModels

# 添加模型
~/.claude/skills/lynse/api_wrapper.sh addModel '{"name":"GPT-4","provider":"openai","apiKey":"sk-xxx"}'

# 编辑模型
~/.claude/skills/lynse/api_wrapper.sh editModel '{"id":"xxx","name":"GPT-4-Turbo"}'

# 启用模型
~/.claude/skills/lynse/api_wrapper.sh enableModel "<modelId>" true

# 禁用模型
~/.claude/skills/lynse/api_wrapper.sh enableModel "<modelId>" false

# 删除模型
~/.claude/skills/lynse/api_wrapper.sh deleteModel "<modelId>"
```

---

## 文件夹管理

API base path: `/api/business/folder`（CLI B 专属）

| 用户意图 | CLI B 命令 | 说明 |
|---|---|---|
| 创建/编辑文件夹 | `add`, `edit1` | Body: FolderAddOrEditReq |
| 查询文件夹列表 | `list1` | — |
| 选择文件夹 | `selectOne` | — |
| 排序文件夹 | `batchUpdateSort` | Body: FolderSortUpdateReq |

---

## 团队管理

API base path: `/api/business/team`（CLI B 专属）

| 用户意图 | CLI B 命令 | 说明 |
|---|---|---|
| 创建团队 | `createTeam` | Body: TeamAddOrEditReq |
| 编辑团队 | `editTeam` | Body: TeamAddOrEditReq |
| 删除团队 | `deleteTeam` | — |
| 我的团队列表 | `listMyTeam` | — |
| 团队详情 | `info` | teamId |
| 离开团队 | `leaveTeam` | teamId |
| 团队充值 | `recharge` | Body: TeamRechargeReq |
| 移除成员 | `removeTeamMember` | — |
| 创建邀请 | `createInvitation` | Body: GenerateInviteReq |
| 处理邀请 | `handleInvite` | — |
| 我的邀请列表 | `listMyInvitation` | — |
| 团队文件列表 | `listTeamFile` | — |
| 团队文件详情 | `getFileInfo` | — |
| 编辑团队文件 | `editTeamFile` | — |
| 移动/复制文件 | `moveOrCopy` | — |
| 删除团队文件 | `removeTeamFile` | — |
| 分配积分到团队 | `allocatePointsToTeam` | — |
| 分配角色 | `assignRole` | — |

---

## 系统管理

| 用户意图 | Wrapper命令 | HTTP | 路径 |
|---|---|---|---|
| 获取角色列表 | `getRoleList` | GET | `/sysRole/list1` |
| 获取菜单树 | `getMenuTree` | GET | `/sysMenu/tree` |
| 发送短信 | `sendSms <json>` | POST | `/message/sendSmsMessage` |
| 发送邮件 | `sendEmail <json>` | POST | `/message/sendEmailMessage` |

```bash
# 角色列表
~/.claude/skills/lynse/api_wrapper.sh getRoleList

# 菜单树
~/.claude/skills/lynse/api_wrapper.sh getMenuTree

# 发送短信
~/.claude/skills/lynse/api_wrapper.sh sendSms '{"phone":"13800138000","content":"验证码: 123456"}'

# 发送邮件
~/.claude/skills/lynse/api_wrapper.sh sendEmail '{"to":"user@example.com","subject":"标题","content":"正文"}'
```

### 登录与认证（一般无需手动调用）

| 命令 | 说明 |
|---|---|
| `login <user> <pwd>` | 用户名密码登录（不推荐，使用 API Key） |
| `loginWithPhone <phone> <code>` | 手机验证码登录 |
| `logout` | 登出 |

---

## 其他功能（CLI B 专属）

### 翻译服务

| CLI B 命令 | 说明 |
|---|---|
| `getTranslateResult` | 获取翻译结果 |
| `getTranslateHistory` | 翻译历史 |
| `getTranscriptionLanguageList` | 转写语言列表 |
| `getLatestSpeakerNames` | 获取最新说话人名称 |
| `getPromptTemplateCategories` | 提示词模板分类 |
| `getRegenerateSelectList` | 重新生成选项列表 |

### 积分与活动

| CLI B 命令 | 说明 |
|---|---|
| `queryPointsLog` | 积分变动日志 |
| `claim` | 领取奖励 |
| `claimByActivityId` | 按活动 ID 领取 |

### 推送服务

| CLI B 命令 | 说明 |
|---|---|
| `init` | 初始化推送 |
| `testAndroidPush` | 测试 Android 推送 |
| `testIosPush` | 测试 iOS 推送 |

### 其他

| CLI B 命令 | 说明 |
|---|---|
| `checkApkUpdate` | 检查 APK 更新 |
| `checkVersion` | 检查版本 |
| `getFunctionList` | 功能列表 |
| `presignUrl` | 预签名 URL |
| `generateShareLink` | 生成分享链接 |
| `getSharedInfo` | 获取分享信息 |

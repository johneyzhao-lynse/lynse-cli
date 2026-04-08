# Customer (用户/客户管理)

> Prerequisites: see root `../SKILL.md` for setup, auth, and API call method.

API base paths: `/api/business/customer`, `/sysUser`

## 接口决策表

| 用户意图 | Wrapper命令 | HTTP | 路径 | 关键参数 |
|---|---|---|---|---|
| 获取当前客户完整信息（手机号、积分等） | `getCurrentCustomer` | GET | `/api/business/customer/current` | 无 |
| 获取当前用户手机号 | `getUserPhone` | GET | `/api/business/customer/current` | 无（解析 phone 字段） |
| 获取当前用户积分 | `getUserPoints` | GET | `/api/business/customer/current` | 无（解析 pointsAmount 字段） |
| 获取指定系统用户信息 | `getUserInfo <userId>` | GET | `/sysUser/info` | Header: `id: <userId>` |
| 获取当前系统用户 | `getCurrentUser` | GET | `/sysUser/current` | 无 |
| 添加系统用户 | `addUser <json>` | POST | `/sysUser/add2` | Body: JSON |
| 编辑系统用户 | `editUser <json>` | POST | `/sysUser/edit1` | Body: JSON |
| 删除系统用户 | `removeUser <userId>` | POST | `/sysUser/remove` | Header: `id: <userId>` |
| 查询客户详情 | CLI B: `detail` | GET | `/api/business/customer/detail` | queryReq |
| 查询客户列表 | CLI B: `list2` | GET | `/api/business/customer/list` | queryReq |
| 编辑客户信息 | CLI B: `edit2` | PUT | `/api/business/customer` | Body: JSON |
| 客户注册 | CLI B: `register` | POST | `/api/business/customer/register` | Body: JSON |
| 客户充值 | CLI B: `recharge1` | POST | `/api/business/customer/recharge` | Body: JSON |
| 修改密码 | CLI B: `updatePwd` | PUT | `/api/business/customer/updatePwd` | Body: JSON |
| 注销客户 | CLI B: `terminate` | DELETE | `/api/business/customer` | customerId |
| 切换团队 | CLI B: `changeTeam` | GET | `/api/business/customer/changeTeam` | teamId |

## 常用工作流

### 获取当前用户信息

```bash
# 完整信息
~/.claude/skills/lynse/api_wrapper.sh getCurrentCustomer
# 返回: CustomerInfoVO (id, nickname, phone, pointsAmount, usedPointsAmount, etc.)

# 仅手机号
~/.claude/skills/lynse/api_wrapper.sh getUserPhone

# 仅积分
~/.claude/skills/lynse/api_wrapper.sh getUserPoints
```

### 系统用户管理

```bash
# 查看当前系统用户
~/.claude/skills/lynse/api_wrapper.sh getCurrentUser

# 查看指定用户
~/.claude/skills/lynse/api_wrapper.sh getUserInfo "<userId>"

# 添加用户
~/.claude/skills/lynse/api_wrapper.sh addUser '{"username":"test","password":"123456","phone":"13800138000"}'

# 编辑用户
~/.claude/skills/lynse/api_wrapper.sh editUser '{"id":"xxx","nickname":"新昵称"}'

# 删除用户
~/.claude/skills/lynse/api_wrapper.sh removeUser "<userId>"
```

### 高级操作（通过 CLI B）

```bash
# 查询客户列表
~/.claude/skills/lynse/lynse_unified.sh list2 queryReq='{"phone":"13800138000"}'

# 客户充值
~/.claude/skills/lynse/lynse_unified.sh recharge1 '{"customerId":"xxx","amount":100}'

# 客户注册
~/.claude/skills/lynse/lynse_unified.sh register '{"phone":"13800138000","code":"123456"}'
```

## 核心响应字段

**CustomerInfoVO**: `id`, `nickname`, `phone`, `avatar`, `pointsAmount` (总积分), `usedPointsAmount` (已用积分), `vipLevel`, `vipExpireTime`, `createTime`.

**CustomerExtInfoVO** (detail): 包含 CustomerInfoVO + 扩展信息 `teamInfo`, `deviceCount`.

**SysUser**: `id`, `username`, `nickname`, `phone`, `email`, `roles`, `status`.

## 注意事项

- `getCurrentCustomer` 和 `getUserPoints`/`getUserPhone` 调的是同一个接口，后者只是解析不同字段
- 积分 = `pointsAmount` - `usedPointsAmount` 为可用积分
- 系统用户（`/sysUser`）和客户（`/api/business/customer`）是不同的概念：系统用户是后台管理用户，客户是 C 端用户
- `removeUser` 是 POST 方法（非 DELETE），通过 Header 传 id

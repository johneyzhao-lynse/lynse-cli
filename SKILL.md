---
name: lynse-cli
description: |
  Use when users mention Lynse backend API operations: querying user info, managing files,
  device management, AI model management, points/balance inquiry, transcription, conclusions,
  outlines, or system admin tasks. Also use when users say "查用户"、"文件列表"、"转写记录"、
  "总结"、"大纲"、"设备"、"模型"、"积分" or any backend API interaction in Chinese.
---

# lynse - Lynse Java Backend API CLI

Unified Lynse backend API skill. Modules: **customer**, **file**, **admin**.

## Setup

Configure API Key (priority order):

1. **.env file (recommended, cross-platform):**
   ```bash
   echo "LYNSE_API_KEY=dk_xxx" > ~/.claude/skills/lynse-cli/.env && chmod 600 ~/.claude/skills/lynse-cli/.env
   ```
2. **Environment variable (session-level):** `export LYNSE_API_KEY="dk_xxx"`

`API_HOST` defaults to `http://119.97.160.133:10060`, configurable in `api_wrapper.sh`. Token is auto-managed.

## Credential Pre-check (CRITICAL)

**Before calling any API, check if API Key is configured.**

```bash
# Quick check
test -f ~/.claude/skills/lynse-cli/.env && grep -q '^LYNSE_API_KEY=.' ~/.claude/skills/lynse-cli/.env && echo "CONFIGURED" || echo "NOT_CONFIGURED"
```

**If API Key is NOT configured:**

> **STOP and ask the user:** "You haven't configured your Lynse API Key yet. Please provide your API Key (dk_xxx format, obtain from admin console), and I'll save it to .env file."
>
> After user provides the key:
> ```bash
> echo "LYNSE_API_KEY=用户提供的key" > ~/.claude/skills/lynse-cli/.env && chmod 600 ~/.claude/skills/lynse-cli/.env
> ```
> Then proceed with the API call.

**If API Key IS configured:** Proceed with `api_wrapper.sh <command>` directly.

## Security Measures

| Measure | Detail |
|---|---|
| .env file storage | Cross-platform, skill directory scoped |
| File permissions | .env & token cache auto-set to `chmod 600` (owner-only) |
| No hardcoded secrets | No JWT tokens or API keys in source code |
| Silent curl | All `curl -s` to prevent credentials leaking to terminal |
| No credential echo | Script never prints API Key or Token in output |
| Token cache isolation | Cache at `/tmp/.lynse_token_cache_$USER` (per-user, hidden) |
| .gitignore friendly | .env files should be added to .gitignore |

## API Call Method

All calls go through the semantic wrapper:

```bash
# Invoke via api_wrapper.sh (auto-handles token)
~/.claude/skills/lynse-cli/api_wrapper.sh <command> [params...]

# Or use unified CLI directly (bypasses semantic wrapper):
~/.claude/skills/lynse-cli/lynse_unified.sh <cli-command> [params...]
```

**Auth headers:** `Authorization: <token>` (no Bearer prefix) + `X-API-Key: <api_key>`

## Module Decision Table

| User Intent | Module | Read |
|---|---|---|
| Query current user info, phone, points, edit user, register, recharge, list users | customer | `customer/SKILL.md` |
| List files, file info, conclusions, outlines, transcription, upload/download, audio merge, delete/recover | file | `file/SKILL.md` |
| Device management, AI model CRUD, roles, menu tree, SMS/email, folders, teams | admin | `admin/SKILL.md` |

### Quick Reference — Most Used Commands

| Command | Description | Module |
|---|---|---|
| `getCurrentCustomer` | Get current user full info (phone, points, etc.) | customer |
| `getUserPoints` | Get current user points balance | customer |
| `listFiles` | List all user files | file |
| `getFileInfo <fileId>` | Get file detail by ID | file |
| `getConclusion <fileId>` | Get file conclusions | file |
| `getOutline <fileId>` | Get file outline | file |
| `getTranscriptionRecord <fileId>` | Get transcription record | file |
| `getAiModels` | List all AI models | admin |
| `getDevicePage <pageNum>` | Paginated device list | admin |

## Notes

- **JSON params**: Must be wrapped in double quotes: `api_wrapper.sh addModel '{"name":"gpt-4"}'`
- **Error handling**: API returns standard JSON with error messages; wrapper displays them directly
- **jq optional**: Skill auto-adapts to environments without `jq`
- **Cross-environment**: Copy entire lynse directory, update `API_KEY` in `api_wrapper.sh`, ready to use

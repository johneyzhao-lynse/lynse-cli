# Lynse CLI Reference

## Scope Permissions

| Scope | Description | Commands |
|-------|-------------|----------|
| `customer.read` | Read user info | getCurrentCustomer, getUserInfo, refreshMembership |
| `customer.write` | Edit users | addUser, editUser, removeUser |
| `file.read` | Read files/transcriptions/summaries | listFiles, getFileInfo, getConclusion, getOutline |
| `file.write` | Edit file content | editConclusion, editOutline, editTransRecord |
| `device.read` | Read device info | getMyDevices, getDeviceInfo, getDevicePage |
| `device.manage` | Manage devices | unbindDevice |
| `ai.read` | View AI models | getAiModels |
| `ai.manage` | Manage AI models | addModel, editModel, deleteModel, enableModel |
| `message.send` | Send messages | sendSms, sendEmail |
| `team.read` | View team | listMyTeam |
| `team.manage` | Manage team | createTeam, editTeam, removeTeamMember |

When permissions are insufficient, API returns HTTP 403. Guide user to contact administrator.

## CLI Version Routing

The skill supports two CLI versions:
- **lynse-cli-a** (basic): Core auth (login, register, token management)
- **lynse-cli-b** (enhanced): Full business features (files, teams, AI, devices)

`lynse_cli.py` auto-detects and routes to the available version. See [compatibility.md](compatibility.md) for command mapping.

## File Structure

```
lynse-cli/
├── SKILL.md              # Main skill instructions
├── reference.md          # This file — detailed reference
├── install-guide.md      # Installation and deployment guide
├── lynse.py              # Core API module
├── lynse_cli.py          # Unified CLI entry point
├── requirements.txt      # Python dependencies
├── install.sh            # macOS/Linux install script
├── install.ps1           # Windows install script
├── .env                  # Configuration file
├── lynse_unified.sh      # Shell CLI (backward compat, macOS/Linux only)
├── api_wrapper.sh        # Shell API wrapper (backward compat, macOS/Linux only)
└── lynse.bat             # Windows .bat wrapper (backward compat)
```

## Changelog

### v1.5.0 (2026-06-20)
- Added `meetings month <YYYY-MM>` — query meetings in a specific month
- Added `meetings week <YYYY-Wnn>` — query meetings in a specific ISO week
- Added `meetings range <start> <end>` — query meetings in an arbitrary date range
- Flexible argument parsing: `month 4`, `month 2026-04`, `month 2026 4` all work
- Proper error messages with exit code 1 for invalid dates/arguments

### v1.4.0 (2026-06-20)
- Friendly command aliases (`me`, `meetings list`, `folders list`, etc.)
- Output format control (`--json`, `--pretty`, `--text`, `--table`, `--output`)
- Semantic exit codes (0-6)
- `auth login/status/logout/doctor` commands
- `version` / `doctor` / `update` system commands
- `~/.lynse/config.json` user-level config support
- Token cache default path migrated to `~/.lynse/tokens.json`
- Full backward compatibility with legacy API-style commands

### v1.3.0 (2026-04-17)
- Python cross-platform support (Windows/macOS/Linux)
- `lynse.py` core API module
- `lynse_cli.py` unified CLI entry point
- `install.ps1` Windows install script
- Improved error handling and token management

### v1.2.1
- API server address auto-detection

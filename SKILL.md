---
name: lynse-cli
description: >
  Lynse CLI skill for querying meeting transcriptions, managing files, todos, devices, and AI models
  via the lynse.ai API. Use when the user asks about meetings, transcriptions, summaries, todos,
  file/folder management, account info, points balance, device binding, AI model configuration, or
  any Lynse platform operations. Trigger on: meeting, transcription, summary, todo, device, model,
  points, file, folder, auth, lynse, 灵光记, 会议, 转写, 总结, 待办, 设备, 模型, 积分, 文件.
  Do NOT use for: generic calendar apps, Zoom/Teams recordings unrelated to Lynse, local file
  system operations, or other platforms that merely share these common words.
version: 1.5.0
metadata:
  openclaw:
    requires:
      env:
        - LYNSE_API_HOST
        - LYNSE_API_KEY
      bins:
        - python
    platforms:
      - macOS
      - Linux
      - Windows
    primaryEnv: LYNSE_API_KEY
    homepage: https://www.lynse.ai
    emoji: "\U0001F4CB"
---

# Lynse CLI Skill

Cross-platform Python CLI (3.8+) for lynse.ai backend services. Works natively on Windows / macOS / Linux.

## How to Invoke

Invoke via the Python entrypoint: `<PY> lynse.py <command>`, where `<PY>` is the Python 3
interpreter available in the current environment.

**Choosing the interpreter** — no single name works everywhere, so pick by environment:

| Environment | Use | Why |
|-------------|-----|-----|
| macOS / Linux | `python3` | Modern systems (Homebrew Python, recent Ubuntu/Debian) only ship `python3`; `python` is often absent. `lynse.py`'s shebang is `#!/usr/bin/env python3`. |
| Windows (CMD / PowerShell) | `python` (or `py -3`) | Windows installs expose `python`, not `python3`. The `py` launcher also works. |
| If unsure | `python3 lynse.py version` first; fall back to `python lynse.py version` | The command that prints a version string is the one to use. |

```bash
python3 lynse.py me                 # current user info (macOS/Linux)
python3 lynse.py meetings list      # recent meetings
```

For brevity, the command examples below use `python3` as the default — substitute `python`
(or `py -3`) on Windows.

- Do NOT use shell scripts (`lynse_unified.sh`, `api_wrapper.sh`) — they don't run on Windows.
- The `lynse` shorthand and `lynse.bat` only work where a wrapper is on PATH; in skill contexts, call the Python entrypoint directly.

## Commands

### Friendly Aliases (Preferred)

```
python3 lynse.py me                                    # Current user info
python3 lynse.py meetings list [--days 7]              # Recent meetings (past N days)
python3 lynse.py meetings month <YYYY-MM>              # Meetings in a specific month
python3 lynse.py meetings week <YYYY-Wnn>              # Meetings in a specific ISO week
python3 lynse.py meetings range <start> <end>          # Meetings in a date range (YYYY-MM-DD)
python3 lynse.py meetings search <keyword>             # Search by title
python3 lynse.py meetings transcript <id>              # Get transcription
python3 lynse.py meetings summary <id>                 # Get AI summary
python3 lynse.py meetings outline <id>                 # Get outline
python3 lynse.py meetings info <id>                    # Meeting details
python3 lynse.py folders list                          # List folders/groups
python3 lynse.py folders create <json>                 # Create folder
python3 lynse.py folders move <json>                   # Move files to folder
python3 lynse.py todos list [all|open|done]            # List todos
python3 lynse.py todos delete <ids>                    # Delete todos
python3 lynse.py todos clear                           # Clear completed todos
python3 lynse.py devices list                          # List bound devices
python3 lynse.py devices info <id>                     # Device details
python3 lynse.py devices unbind <id>                   # Unbind device
python3 lynse.py models list                           # List AI models
python3 lynse.py models add <json>                     # Add model
python3 lynse.py models delete <id>                    # Delete model
python3 lynse.py models edit <json>                    # Edit model
python3 lynse.py models enable <id> <bool>             # Enable/disable model
```

**Date query flexibility** (`meetings month`/`week`):
```
python3 lynse.py meetings month 2026-04          # All April 2026 meetings
python3 lynse.py meetings month 4                # April of current year
python3 lynse.py meetings week 2026-W16          # ISO week 16 of 2026
python3 lynse.py meetings range 2026-04-01 2026-04-30   # Custom date range
```

### Auth & System

```
python3 lynse.py auth login --api-key <key> [--host <url>]   # Save & validate API key
python3 lynse.py auth status                                  # Show auth config
python3 lynse.py auth logout [--all]                          # Clear tokens (--all also clears API key)
python3 lynse.py auth doctor                                  # Diagnose auth issues
python3 lynse.py version    # Version, Python, OS, requests info
python3 lynse.py doctor     # Full environment diagnostics
python3 lynse.py update     # Show update instructions
```

### Output Format Control

```
--json             Compact JSON (default when piped)
--pretty           Pretty-printed JSON (default in terminal)
--text             Human-readable text summary
--table            ASCII table for list results
--output <file>    Save output to file
```

Combine: `python3 lynse.py meetings list --table --output meetings.txt`

## Output Contract — Meeting Lists

When presenting meeting query results, format as a table using these JSON fields:

| Column   | JSON Field                          | Format                  |
|----------|-------------------------------------|-------------------------|
| #        | (row index)                         | Sequential, from 1      |
| Date     | `recordStartTime` or `createTime`   | `YYYY-MM-DD HH:MM`      |
| Duration | `bizDuration`                       | Convert seconds → `mm:ss` |
| Folder   | `folderName`                        | As-is, empty if null    |
| Title    | `originalFilename`                  | As-is, fallback to `filename` |

Sort by `recordStartTime` ascending. Append summary line: `Total: N meetings, HH:MM`.

## Exit Codes

| Code | Meaning           | Typical Cause                |
|------|-------------------|------------------------------|
| 0    | Success           | Normal completion            |
| 1    | Invalid / Unknown | Bad args, JSON parse error   |
| 2    | Auth failure      | Token expired, invalid API key |
| 3    | Network error     | DNS, connection refused      |
| 4    | Timeout           | Request timed out            |
| 5    | Permission denied | HTTP 403                     |
| 6    | Server error      | HTTP 5xx, business error     |

## Key Constraints

- **Base URL**: all API requests use `$LYNSE_API_HOST`. Never hardcode or guess the server address.
- **Auth**: two-layer API Key + Token. See [references/auth-and-security.md](references/auth-and-security.md) for the full flow, config resolution order, and security rules (sensitive data masking, owner-ID guard, token cache permissions).
- **Errors**: see [references/error-handling.md](references/error-handling.md) for the HTTP/business error mapping and how to report errors to users.
- **Platform paths**: the skill installs the same into Claude Code / Cursor / Hermes / OpenClaw. See [references/platform-paths.md](references/platform-paths.md) for per-environment directories and env-var injection.

## Reference Docs

- [install-guide.md](install-guide.md) — installation & deployment
- [reference.md](reference.md) — scope permissions, CLI version routing, file structure, changelog
- [references/auth-and-security.md](references/auth-and-security.md) — auth flow & security rules
- [references/error-handling.md](references/error-handling.md) — error codes & handling
- [references/platform-paths.md](references/platform-paths.md) — AI assistant environment paths

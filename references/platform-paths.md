# Platform Paths (AI Assistant Environments)

The skill ships the same way into every AI assistant; only the install directory differs.
`install.sh` / `install.ps1` auto-detects the environment and copies files to the right place.

## Skill Install Directories

| Environment | Skills Directory | Env Vars |
|-------------|------------------|----------|
| Claude Code | `~/.claude/skills/lynse-cli/` | Manual `.env` or env vars |
| Cursor | `~/.cursor/skills/lynse-cli/` | Manual `.env` or env vars |
| Hermes | `~/.hermes/skills/lynse-cli/` | Manual `.env` or env vars |
| OpenClaw | `~/.openclaw/workspace/skills/lynse-cli/` | Auto-injected by platform |

## How the Skill Is Invoked in Each Environment

All environments invoke the skill the same way once installed — the AI assistant runs the Python entrypoint inside its skills directory:

```bash
python3 lynse.py <command> [args...]   # macOS / Linux
python lynse.py <command> [args...]    # Windows (or: py -3 lynse.py)
```

No single interpreter name works on every platform — modern macOS (Homebrew) and recent Ubuntu/Debian ship only `python3`, while Windows exposes `python` (not `python3`). Pick by environment; if unsure, run `<candidate> lynse.py version` and use whichever prints a version string. `install.sh` / `install.ps1` auto-detect the right one and print it at the end of installation.

The other difference across environments is **how env vars reach the process**:

- **OpenClaw**: injects `LYNSE_API_HOST` and `LYNSE_API_KEY` automatically.
- **Other environments**: read from `.env`, `~/.lynse/config.json`, or exported env vars (see `references/auth-and-security.md`).

## Cross-Platform Execution Rules

1. Use `python3` on macOS/Linux, `python` (or `py -3`) on Windows. Never assume one name works everywhere.
2. Never use shell scripts (`lynse_unified.sh`, `api_wrapper.sh`) in instructions — they don't work on Windows.
3. On Windows, call `python lynse.py ...` or `py -3 lynse.py ...` directly from the skill directory. For npm installs, the `lynse` command is provided by `bin/lynse.js`, and npm creates the Windows `.cmd` shim automatically.

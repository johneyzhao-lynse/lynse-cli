# Lynse CLI Installation Guide

## Auto Install (Recommended)

```bash
# macOS/Linux
./install.sh

# Windows PowerShell
.\install.ps1
```

The install script will:
1. Detect the current AI assistant environment
2. Copy skill files to the appropriate skills directory
3. Create `.env` config file (auto-fills API server address)
4. Install Python dependencies (requests)
5. Set script execution permissions
6. Display post-install usage instructions

## Manual Install

1. Copy the entire `lynse-cli` directory to the target skills directory
2. Copy `.env.example` to `.env` and set `LYNSE_API_HOST` (the API server address)
   - macOS/Linux: `cp .env.example .env`
   - Windows CMD: `copy .env.example .env`
   - PowerShell: `Copy-Item .env.example .env`
3. Run `pip install -r requirements.txt`
4. Configure your API key — see below
5. Ready to use

## Configure Your API Key (Required)

No API key is shipped or hardcoded. Each user inputs their own key, which is
saved locally to `~/.lynse/config.json` (never committed). The recommended way:

```bash
# Interactive prompt (input is hidden). Runs in any terminal.
python3 lynse.py auth login
# Or pass it explicitly:
python3 lynse.py auth login --api-key dk_xxx
```

Get your key (format `dk_xxx`) from the system console. Verify with
`python3 lynse.py auth status`.

Credential precedence (highest → lowest): `--api-key` param → `LYNSE_API_KEY`
shell env → `~/.lynse/config.json` → install `.env`. A stale `.env` will **not**
override the key you saved via `auth login`.

## Environment-Specific Paths

| Environment | Skills Directory |
|-------------|-----------------|
| OpenClaw | `~/.openclaw/workspace/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |
| Hermes | `~/.hermes/skills/` |

## Environment Variables

Prefer `auth login` (above). Setting env vars is an alternative — useful when a
platform injects them for you:

```powershell
# PowerShell
$env:LYNSE_API_HOST="https://your-api-host/api"
$env:LYNSE_API_KEY="dk_your_api_key_here"
```

```bash
# macOS/Linux
export LYNSE_API_HOST="https://your-api-host/api"
export LYNSE_API_KEY="dk_your_api_key_here"
```

```cmd
# Windows CMD
set LYNSE_API_HOST=https://your-api-host/api
set LYNSE_API_KEY=dk_your_api_key_here
```

**Note:** OpenClaw auto-injects `LYNSE_API_HOST` and `LYNSE_API_KEY`. Other environments require manual configuration.

## Windows FAQ

**Q: `python` command not found on Windows?**
A: Ensure "Add Python to PATH" was checked during install. Or use `py` launcher: `py lynse.py getCurrentCustomer`

**Q: No PowerShell available?**
A: Manually copy files to `~/.claude/skills/lynse-cli/`, create `.env`, run `pip install requests`.

**Q: Can I use Git Bash?**
A: Yes, but not required. `python lynse.py` works in CMD, PowerShell, and Git Bash.

## macOS / Linux FAQ

**Q: `python: command not found` on macOS/Linux?**
A: Modern macOS (Homebrew Python) and recent Ubuntu/Debian only ship `python3`, not `python`. Use `python3` instead:
```bash
python3 lynse.py me
python3 lynse.py meetings list
```
`install.sh` auto-detects the right interpreter and prints it at the end of installation. To check manually:
```bash
python3 lynse.py version    # try this first
python lynse.py version     # fallback (Windows / older setups)
```
The interpreter that prints a version string is the one to use.

**Q: How do I make `python` point to Python 3 on macOS?**
A: Optional. Either install the `python` symlink via Homebrew (`brew install python`), or add `alias python=python3` to `~/.zshrc`. Not required — `python3` works everywhere `python` does not.

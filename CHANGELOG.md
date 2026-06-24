# Changelog

## 1.6.2 (2026-06-24)

### New Features

- Add `bin/lynse.js` — a cross-platform npm command wrapper that replaces the Windows-only `lynse.bat`, making the `lynse` command work via npm on all platforms (macOS, Linux, Windows).

### Changed

- Update `package.json` entry point from `lynse.bat` to `bin/lynse.js`; include `CHANGELOG.md`, `install-guide.md`, `reference.md`, and `references/` in the npm package files list.
- Update documentation (`SKILL.md`, `reference.md`, `references/platform-paths.md`) to reflect the new npm wrapper and remove `.bat` references.
- Clean up `.gitignore` with explicit patterns for generated OpenAPI client artifacts.

## 1.6.1 (2026-06-20)

### Bug Fixes

- Retry transient HTTP 429/5xx in `_request` so every command survives a momentary server hiccup (found when the folder-create endpoint returned a 503 mid-organize).
- `meetings organize --execute` now surfaces folder-creation failures (`folders_failed`) instead of failing silently; affected meetings are skipped and a re-run finishes them once the server recovers.
- `folders list --text/--table` now shows folder names (read `folderName`; previously rendered `?`).

## 1.6.0 (2026-06-20)

### New Features

- **`meetings organize`** — auto-classify meetings into Lynse folders by topic. Dry-run plan by default (changes nothing); `--execute` creates folders and moves meetings. Reuses existing folders where they match and proposes new ones (icon + ≤6-char name), capping at 10 folders + 🗂其他. Flags: `--days N` (scope), `--execute` / `--yes` (apply; non-interactive requires `--yes`), `--include-no-conclusion`.

## 1.5.2 (2026-06-20)

### Bug Fixes

- Stop a stale install `.env` from overriding the API key saved via `auth login` — this caused intermittent `meetings month` failures ("API Key authentication failed") whenever a token refresh was required while a cached token was still valid.
- Token exchange now retries transient server/network errors (5xx, 429, timeouts) with backoff instead of failing on the first hiccup, and no longer reports server errors as "API Key authentication failed". HTTP 401/403 is reported as a rejected key; everything else as a transient error.

### Changed

- Resolve API credentials with one consistent precedence used by every command: `--api-key` param → shell env (`LYNSE_API_KEY`) → `~/.lynse/config.json` → install `.env`. `auth status` now reports the actual source (`config_source`).
- `auth login` prompts for the key interactively (hidden input) in a terminal and requires `--api-key` in non-interactive/agent contexts. No API key is hardcoded or shipped.
- Install scripts (`install.sh`, `install.ps1`) no longer write a placeholder key into `.env`; users are directed to `auth login`.

## 1.5.1 (2026-06-20)

### New Features

- Auto-detect the Python 3 interpreter (`python3` vs `python`) at install time, so `install.sh` prints the right invocation for the user's environment.
- Add reference documentation: `install-guide.md`, `reference.md`, and `references/{auth-and-security,error-handling,platform-paths}.md`.

### Bug Fixes

- Meeting list commands now render `--table` / `--text` output formats correctly.
- Restore executable bit on `install.sh` so `./install.sh` works as documented.

### Changed

- Rewrite `SKILL.md` from Chinese to English and restructure it for AI agent consumption (consolidated cross-platform guidance, explicit interpreter-selection table).
- Move table formatting conventions out of hardcoded CLI code and into the `SKILL.md` prompt convention.
- Update `lynse.py` module docstring to prefer `python3` with a Windows fallback note.

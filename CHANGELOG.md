# Changelog

## 1.6.5 (unreleased)

### Fixed

- `_format_table` no longer truncates the ID column to 40 chars. Meeting/file IDs are longer than 40 chars, so the previous `str(v)[:40]` cut silently dropped trailing characters and broke downstream `meetings summary/transcript/outline/info` lookups when the ID was copied from the table. The ID column now stays full; other wide columns still truncate but keep an explicit `...` marker (see `tests/test_format_table.py`).

## 1.6.4 (2026-07-05)

### New Features

- Add `meetings transcript-text <id>` to fetch meeting transcription text from the transcription endpoint, including speaker labels and timestamps.

### Changed

- Keep transcription text separate from AI summaries by routing through `getTranscriptionRecord` instead of conclusion APIs.
- Document `getTranscriptionText` under file read permissions.

## 1.6.3 (2026-06-29)

### Changed

- Clarify that Lynse is the English product context and 灵光记 is the Chinese product name, so requests to use 灵光记 route to this CLI skill.
- Remove all OpenAPI-generated docs (`lynse-cli-a/docs/*`, `lynse-cli-b/docs/*`) and associated generated artifacts to reduce repository bloat.
- Remove deprecated `lynse.bat` (Windows batch wrapper), `.env.example`, and old GitHub Actions `npm-publish.yml` workflow.
- Update `lynse.py` CLI version from 1.6.1 to 1.6.3; update `SKILL.md` version from 1.5.1 to 1.6.3.
- Remove `.env.example` from npm package file list.

## 1.6.2 (2026-06-24)

### New Features

- Add `bin/lynse.js` — a cross-platform npm command wrapper that replaces the old Windows batch wrapper, making the `lynse` command work via npm on all platforms (macOS, Linux, Windows).

### Changed

- Update `package.json` entry point to `bin/lynse.js`; include `CHANGELOG.md`, `install-guide.md`, `reference.md`, and `references/` in the npm package files list.
- Update documentation (`SKILL.md`, `reference.md`, `references/platform-paths.md`) to reflect the new npm wrapper and remove batch-wrapper references.
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

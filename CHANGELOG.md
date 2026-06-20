# Changelog

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

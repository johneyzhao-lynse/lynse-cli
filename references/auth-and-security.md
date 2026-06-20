# Auth & Security

## Two-Layer Auth

Lynse uses **API Key + temporary Token**:

```
Step 1: Exchange API Key for Token
POST $LYNSE_API_HOST/api/auth/apikey/token
Header: X-API-Key: $LYNSE_API_KEY

Step 2: Call business APIs with Token
Header: Authorization: <accessToken>    (no Bearer prefix)
Header: X-API-Key: $LYNSE_API_KEY
```

- **API Key format**: `dk_xxx` (obtained from system console)
- **Token TTL**: 2 hours, auto-refreshes on expiry
- **Token cache**: `~/.lynse/tokens.json`, file permission 600 (owner read/write only)

## Config Resolution Order (v1.4.0+)

1. CLI flags (`--api-key`, `--host`)
2. Environment variables (`LYNSE_API_KEY`, `LYNSE_API_HOST`)
3. User config (`~/.lynse/config.json`)
4. Project `.env` file (backward compatible)

## Auth Flow

```
User calls lynse.py
  → Check LYNSE_API_HOST / LYNSE_API_KEY
    → Not found → Check ~/.lynse/config.json
      → Not found → Check .env
        → Not found → Prompt user to configure
  → Found → Check cached token (~/.lynse/tokens.json)
    → Valid → Use directly
    → Expired → POST /api/auth/apikey/token for new token
      → Success → Cache (chmod 600) → Call business API
      → Failure → Prompt to check API Key
```

**Before every call**: Check `$LYNSE_API_KEY` and `$LYNSE_API_HOST` exist. If not, prompt user:

```bash
# macOS/Linux
export LYNSE_API_HOST="https://your-api-host/api"
export LYNSE_API_KEY="dk_your_api_key_here"
# Or: cp .env.example .env and fill in values
```

## Security Rules

### Sensitive data protection
- Never proactively show phone numbers, points, or other sensitive fields in group chats
- Default to non-sensitive fields (nickname, ID) unless user explicitly requests more
- In group chats, mask phone numbers (`138****1234`), hide points
- If `LYNSE_OWNER_ID` is set, verify current user matches; if not, reply: "Access denied: this is a private account."

### Auth security
- Token auto-refreshes on failure; if refresh fails, prompt user to check API Key
- Token cache file must have 600 permissions (owner read/write only)

### Input safety
- All user inputs are sanitized against injection
- Space create/edit operations by 1+ minute to avoid server rate limits

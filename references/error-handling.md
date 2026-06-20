# Error Handling

## Error Response Format

```json
{"code": 403, "message": "error details", "data": null}
```

## HTTP / Business Error Mapping

| Scenario | HTTP Code | Action |
|----------|-----------|--------|
| Token expired | 401 | Auto-refresh with API Key, retry |
| Insufficient permissions | 403 | "Insufficient permissions. Contact admin to upgrade." |
| Rate limited | 429 | Wait 60s, retry. "Rate limit exceeded, please try later." |
| Not found | 404 | "Resource not found." |
| Server error | 500/502/503 | "Server temporarily unavailable, try again later." |
| Token refresh failed | — | Prompt to check `LYNSE_API_KEY` |
| Business error (code != 200) | — | Show error message with possible cause and fix |

## Reporting Errors to Users

1. State what went wrong
2. Suggest likely cause
3. Provide actionable next step

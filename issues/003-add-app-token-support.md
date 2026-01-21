# Issue: Add app access token support for conduit endpoints

**Repository:** twitch-sdk
**Priority:** Medium
**Labels:** feature, auth

## Summary
Conduit management endpoints require an app access token (client credentials flow) rather than a user access token. The SDK needs to support both token types.

## Affected Endpoints
- `twitch_get_conduits`
- `twitch_create_conduit`
- `twitch_update_conduit`
- `twitch_delete_conduit`
- `twitch_get_conduit_shards`
- `twitch_update_conduit_shards`

## Current Error
```
[401] Unauthorized: The API accepts only an app access token.
```

## Proposed Solution
1. Add client credentials flow to SDK auth
2. Allow SDK to use app token for specific endpoints
3. Auto-detect which token type to use based on endpoint

## Implementation Options

### Option A: Dual token support
```python
sdk = TwitchSDK(
    user_token="...",  # For user endpoints
    app_token="..."    # For app-only endpoints
)
```

### Option B: Automatic token acquisition
```python
sdk = TwitchSDK(
    client_id="...",
    client_secret="...",
    user_token="..."  # SDK auto-fetches app token when needed
)
```

## Acceptance Criteria
- [ ] SDK can obtain app access token via client credentials
- [ ] Conduit endpoints work with app token
- [ ] User endpoints still work with user token
- [ ] QA tests pass for all conduit endpoints

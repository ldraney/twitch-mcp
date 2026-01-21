# Issue: Regenerate OAuth token with all required scopes

**Repository:** twitch-mcp (config)
**Priority:** High
**Labels:** auth, config

## Summary
The current OAuth token is missing many scopes needed for full API coverage. Need to regenerate with all required scopes.

## Missing Scopes
- `moderator:read:chatters`
- `channel:read:editors`
- `channel:read:vips`
- `channel:manage:vips`
- `moderation:read`
- `moderator:read:blocked_terms`
- `moderator:manage:blocked_terms`
- `moderator:read:automod_settings`
- `moderator:read:shield_mode`
- `moderator:manage:shield_mode`
- `clips:edit`
- `channel:read:redemptions`
- `channel:manage:redemptions`
- `channel:read:subscriptions`
- `channel:read:charity`
- `bits:read`
- `channel:manage:moderators`
- `channel:manage:polls`
- `channel:read:polls`
- `channel:manage:predictions`
- `channel:read:predictions`

## Steps
1. Go to Twitch Developer Console
2. Update app with all required scopes
3. Regenerate OAuth token via authorization flow
4. Update `~/twitch-secrets/.env` with new token

## Acceptance Criteria
- [ ] Token has all scopes listed above
- [ ] Token validated via `https://id.twitch.tv/oauth2/validate`
- [ ] QA tests that were "Missing scope" now pass

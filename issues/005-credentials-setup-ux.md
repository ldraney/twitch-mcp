# Issue: Credentials Setup UX is Broken

**Priority:** Critical
**Labels:** ux, onboarding, documentation

## Problem

Setting up Twitch API credentials is a nightmare:

1. **No clear guidance** - Users don't know where to put credentials
2. **Multiple competing locations** - `~/.config/twitch-mcp/`, `~/secrets/`, `~/api-secrets/`, env vars, etc.
3. **No integration with secrets vault** - Should work with ldraney/secrets vault system
4. **MCP config complexity** - Users have to manually configure `TWITCH_ENV_FILE` path

## Current State

- Added `twitch-mcp-setup` interactive command
- Added clear error messages when creds missing
- But still no integration with secrets vault
- Path in MCP config is hardcoded to `~/.config/twitch-mcp/.env`

## Required Changes

### 1. Integrate with Secrets Vault
- Add TWITCH_* credentials to ldraney/secrets vault
- Update `twitch-mcp-setup` to optionally pull from vault
- Document the vault integration

### 2. Simplify MCP Config
Options:
- A) Auto-detect credentials from multiple locations (env vars → vault → ~/.config)
- B) Single documented location that everyone uses
- C) MCP config just uses env vars, user's bashrc exports from vault

### 3. Document the Flow
- Step-by-step: Create Twitch app → Get tokens → Store in vault → Configure MCP
- Single source of truth for "how do I set this up"

### 4. PyPI Users
- Users installing via `pip install twitch-mcp` need even simpler setup
- Can't assume they have the secrets vault
- `twitch-mcp-setup` must work standalone

## Critical Bug

`twitch-mcp-setup` asks for ACCESS_TOKEN manually - it should run OAuth flow!

Should work like:
1. User enters CLIENT_ID + CLIENT_SECRET
2. Script starts local server on :3000
3. Opens browser to Twitch OAuth URL
4. User authorizes, callback captures tokens
5. Script saves all 4 values

Reference: `~/twitch-client/auth-server.js` already does this.

## Acceptance Criteria

- [ ] New user can go from zero to working in < 5 minutes
- [ ] Credentials stored in ONE canonical location
- [ ] Works with secrets vault for ldraney's setup
- [ ] Works standalone for PyPI users
- [ ] Clear error messages guide user to fix

## Notes

The current Twitch credentials needed:
- TWITCH_CLIENT_ID (from dev.twitch.tv app)
- TWITCH_CLIENT_SECRET (from dev.twitch.tv app)
- TWITCH_ACCESS_TOKEN (OAuth token with scopes)
- TWITCH_REFRESH_TOKEN (for token refresh)

Token generator: https://twitchtokengenerator.com/

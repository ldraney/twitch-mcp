# Issue: Complete QA and Production Readiness

**Priority:** High
**Labels:** qa, testing, documentation

## Current State

### Published Packages ✅
- `twitch-mcp` on PyPI (v0.1.1)
- `twitch-sdk` on PyPI (v0.1.1)
- Interactive setup with Device Code OAuth flow

### QA Coverage (110 tools total)

| Status | Count | % |
|--------|-------|---|
| ✅ Passed | 13 | 12% |
| 🔧 Fixed (needs retest) | 10 | 9% |
| ⏭️ Skipped (missing scope) | 28 | 25% |
| ⬜ Not Tested | 42 | 38% |

**Only ~12% of tools are fully verified.**

## Tasks

### 1. Retest Fixed Tools
The SDK bugs were fixed but tools need retesting:
- [ ] `twitch_search_channels` - empty string validator
- [ ] `twitch_send_chat_message` - SendChatMessageRequest alias
- [ ] `twitch_send_chat_announcement` - send_announcement alias
- [ ] `twitch_modify_channel_info` - modify_channel_info alias
- [ ] `twitch_create_poll` - PollChoice.id optional
- [ ] `twitch_create_prediction` - PredictionOutcome.id/color optional
- [ ] `twitch_get_channel_schedule` - GetChannelScheduleRequest alias
- [ ] `twitch_get_schedule_icalendar` - string response handling
- [ ] `twitch_get_goals` - get_goals alias
- [ ] `twitch_get_hype_train` - GetHypeTrainRequest alias

### 2. Expand OAuth Scopes
Current token missing scopes for full testing:
- [ ] `moderator:read:chatters`
- [ ] `channel:read:editors`
- [ ] `channel:read:vips` / `channel:manage:vips`
- [ ] `moderation:read`
- [ ] `moderator:read:blocked_terms`
- [ ] `channel:read:redemptions` / `channel:manage:redemptions`
- [ ] `channel:read:subscriptions`
- [ ] `bits:read`

### 3. Set Up EventSub
Real-time events (follows, subs, raids, chat):
- [ ] Deploy eventsub-listen to Fly.io or similar
- [ ] Configure Cloudflare tunnel (or use Fly's public URL)
- [ ] Test subscription creation
- [ ] Document setup process

### 4. Twitch CLI Mock Testing
For QA without going live:
- [ ] Integrate twitch-cli mock server
- [ ] Create test script that runs all endpoints against mock
- [ ] Add to CI/CD pipeline
- [ ] Document mock testing workflow

### 5. Test Remaining 42 Untested Tools
Prioritized by usefulness:
- [ ] Chat tools (update_chat_settings, get_chatters, send_shoutout)
- [ ] Moderation (ban_user, unban_user, warn_user, delete_messages)
- [ ] Clips (get_clips)
- [ ] Videos (get_videos, delete_videos)
- [ ] User tools (update_user, block/unblock)
- [ ] Guest Star (12 tools - requires live + setup)
- [ ] Whispers

### 6. Documentation
- [ ] README with real usage examples
- [ ] List all 110 tools with descriptions
- [ ] EventSub setup guide
- [ ] Troubleshooting common issues

## What Users Can Do Today

Working tools for common use cases:
```
# Read operations (public)
"Get top live streams"
"Search for Minecraft streamers"
"Get info about channel X"
"Who are the top games right now?"

# Authenticated operations
"Send a chat message to my channel"
"Get my follower count"
"Create a poll: What game next? Options: Minecraft, Valorant, Just Chatting"
"Start a prediction: Will I win this match?"
"Create a stream marker"
```

## Acceptance Criteria

- [ ] All 🔧 Fixed tools retested and marked ✅
- [ ] At least 50% of tools tested (55+)
- [ ] EventSub working for basic events
- [ ] Twitch CLI mock tests passing
- [ ] README has real examples users can copy

## Related Issues
- #005 - Credentials Setup UX
- #001-004 - SDK bug fixes (completed)

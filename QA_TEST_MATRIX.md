# QA Test Matrix - Twitch MCP Tools

Total Tools: 110
**Test Date**: 2026-01-22
**Test Method**: Direct SDK calls (MCP server not connected to Claude session)

## Legend
- Status: ⬜ Not tested | ✅ Passed | 🔧 Fixed (needs retest) | ⏭️ Skipped (missing scope/special requirement)
- Auth: Required OAuth scopes

## Summary

| Category | Passed | Fixed | Skipped | Not Tested | Total |
|----------|--------|-------|---------|------------|-------|
| Public Endpoints | 9 | 1 | 0 | 0 | 10 |
| Channel Read | 2 | 1 | 7 | 0 | 10 |
| Live Stream Ops | 1 | 4 | 2 | 0 | 7 |
| Channel Points | 0 | 0 | 4 | 2 | 6 |
| EventSub | 1 | 0 | 5 | 3 | 9 |
| Other | 0 | 4 | 10 | 37 | 51 |

**SDK Bug Fixes**: All 10 SDK bugs fixed in commit `a5aedd5` (2026-01-22)

---

## Ads Module (3 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_start_commercial | ⏭️ | channel:edit:commercial | Requires affiliate/partner |
| twitch_get_ad_schedule | ⏭️ | channel:read:ads | Requires affiliate/partner |
| twitch_snooze_ad | ⏭️ | channel:manage:ads | Requires affiliate/partner |

## Analytics Module (2 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_extension_analytics | ⏭️ | analytics:read:extensions | Extension developer only |
| twitch_get_game_analytics | ⏭️ | analytics:read:games | Game developer only |

## Bits Module (3 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_bits_leaderboard | ⏭️ | bits:read | Missing scope |
| twitch_get_cheermotes | ✅ | - | Public endpoint - Got cheermotes |
| twitch_get_extension_transactions | ⏭️ | - | Extension developer only |

## Channel Points Module (6 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_custom_rewards | ⏭️ | channel:read:redemptions | Missing scope |
| twitch_create_custom_reward | ⏭️ | channel:manage:redemptions | Missing scope |
| twitch_update_custom_reward | ⏭️ | channel:manage:redemptions | Missing scope |
| twitch_delete_custom_reward | ⏭️ | channel:manage:redemptions | Missing scope |
| twitch_get_custom_reward_redemption | ⬜ | channel:read:redemptions | Not tested |
| twitch_update_redemption_status | ⬜ | channel:manage:redemptions | Not tested |

## Channels Module (8 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_channel_info | ✅ | - | Public - Got channel: L_dray |
| twitch_modify_channel_info | 🔧 | channel:manage:broadcast | Fixed: added `modify_channel_info` alias |
| twitch_get_channel_followers | ✅ | moderator:read:followers | 12 followers |
| twitch_get_followed_channels | ⬜ | user:read:follows | Not tested |
| twitch_get_vips | ⏭️ | channel:read:vips | Missing scope |
| twitch_add_vip | ⏭️ | channel:manage:vips | Missing scope |
| twitch_remove_vip | ⏭️ | channel:manage:vips | Missing scope |
| twitch_get_channel_editors | ⏭️ | channel:read:editors | Missing scope |

## Charity Module (2 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_charity_campaign | ⏭️ | channel:read:charity | Missing scope |
| twitch_get_charity_donations | ⏭️ | channel:read:charity | Missing scope |

## Chat Module (7 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_send_chat_message | 🔧 | user:write:chat | Fixed: added `SendChatMessageRequest` alias |
| twitch_get_chat_settings | ✅ | - | Public - slow_mode: False |
| twitch_update_chat_settings | ⬜ | moderator:manage:chat_settings | Not tested |
| twitch_get_chatters | ⏭️ | moderator:read:chatters | Missing scope |
| twitch_send_chat_announcement | 🔧 | moderator:manage:announcements | Fixed: added `send_announcement` alias |
| twitch_send_shoutout | ⬜ | moderator:manage:shoutouts | Not tested |
| twitch_get_user_emotes | ⬜ | user:read:emotes | Not tested |

## Clips Module (2 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_create_clip | ⏭️ | clips:edit | Missing scope |
| twitch_get_clips | ⬜ | - | Public endpoint - Not tested |

## EventSub Module (9 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_eventsub_subscriptions | ✅ | - | Found 0 subs |
| twitch_create_eventsub_subscription | ⬜ | - | Not tested |
| twitch_delete_eventsub_subscription | ⬜ | - | Not tested |
| twitch_get_conduits | ⏭️ | - | Requires app access token |
| twitch_create_conduit | ⏭️ | - | Requires app access token |
| twitch_update_conduit | ⏭️ | - | Requires app access token |
| twitch_delete_conduit | ⏭️ | - | Requires app access token |
| twitch_get_conduit_shards | ⏭️ | - | Requires app access token |
| twitch_update_conduit_shards | ⬜ | - | Not tested |

## Games Module (2 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_top_games | ✅ | - | Public - Got 20 games |
| twitch_get_games | ✅ | - | Public - Found: Just Chatting |

## Goals Module (1 tool)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_goals | 🔧 | channel:read:goals | Fixed: added `get_goals` alias |

## Guest Star Module (12 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_guest_star_settings | ⬜ | channel:read:guest_star | Not tested |
| twitch_get_guest_star_session | ⬜ | channel:read:guest_star | Not tested |
| twitch_create_guest_star_session | ⏭️ | channel:manage:guest_star | Requires live stream + setup |
| twitch_end_guest_star_session | ⬜ | channel:manage:guest_star | Not tested |
| twitch_send_guest_star_invite | ⬜ | channel:manage:guest_star | Not tested |
| twitch_update_guest_star_settings | ⬜ | channel:manage:guest_star | Not tested |
| twitch_get_guest_star_invites | ⬜ | channel:read:guest_star | Not tested |
| twitch_delete_guest_star_invite | ⬜ | channel:manage:guest_star | Not tested |
| twitch_assign_guest_star_slot | ⬜ | channel:manage:guest_star | Not tested |
| twitch_update_guest_star_slot | ⬜ | channel:manage:guest_star | Not tested |
| twitch_delete_guest_star_slot | ⬜ | channel:manage:guest_star | Not tested |
| twitch_update_guest_star_slot_settings | ⬜ | channel:manage:guest_star | Not tested |

## Hype Train Module (1 tool)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_hype_train | 🔧 | channel:read:hype_train | Fixed: added `GetHypeTrainRequest` alias |

## Moderation Module (18 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_ban_user | ⬜ | moderator:manage:banned_users | Not tested |
| twitch_unban_user | ⬜ | moderator:manage:banned_users | Not tested |
| twitch_get_banned_users | ⏭️ | moderation:read | Missing scope |
| twitch_warn_user | ⬜ | moderator:manage:warnings | Not tested |
| twitch_delete_chat_messages | ⬜ | moderator:manage:chat_messages | Not tested |
| twitch_get_moderators | ⏭️ | moderation:read | Missing scope |
| twitch_add_moderator | ⏭️ | channel:manage:moderators | Missing scope |
| twitch_remove_moderator | ⏭️ | channel:manage:moderators | Missing scope |
| twitch_get_blocked_terms | ⏭️ | moderator:read:blocked_terms | Missing scope |
| twitch_add_blocked_term | ⏭️ | moderator:manage:blocked_terms | Missing scope |
| twitch_get_shield_mode_status | ⏭️ | moderator:read:shield_mode | Missing scope |
| twitch_update_shield_mode | ⏭️ | moderator:manage:shield_mode | Missing scope |
| twitch_get_unban_requests | ⬜ | moderator:read:unban_requests | Not tested |
| twitch_resolve_unban_request | ⬜ | moderator:manage:unban_requests | Not tested |
| twitch_remove_blocked_term | ⏭️ | moderator:manage:blocked_terms | Missing scope |
| twitch_get_automod_settings | ⏭️ | moderator:read:automod_settings | Missing scope |
| twitch_update_automod_settings | ⬜ | moderator:manage:automod_settings | Not tested |
| twitch_manage_held_automod_message | ⬜ | moderator:manage:automod | Not tested |

## Polls Module (3 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_create_poll | 🔧 | channel:manage:polls | Fixed: `PollChoice.id` now optional |
| twitch_get_polls | ⬜ | channel:read:polls | Not tested (depends on create) |
| twitch_end_poll | ⬜ | channel:manage:polls | Not tested (depends on create) |

## Predictions Module (3 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_create_prediction | 🔧 | channel:manage:predictions | Fixed: `PredictionOutcome.id/color` now optional |
| twitch_get_predictions | ⬜ | channel:read:predictions | Not tested (depends on create) |
| twitch_end_prediction | ⬜ | channel:manage:predictions | Not tested (depends on create) |

## Raids Module (2 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_start_raid | ⏭️ | channel:manage:raids | Requires target + timing |
| twitch_cancel_raid | ⬜ | channel:manage:raids | Not tested |

## Schedule Module (6 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_channel_schedule | 🔧 | - | Fixed: added `GetChannelScheduleRequest` alias |
| twitch_update_channel_schedule | ⬜ | channel:manage:schedule | Not tested |
| twitch_create_schedule_segment | ⬜ | channel:manage:schedule | Not tested |
| twitch_delete_schedule_segment | ⬜ | channel:manage:schedule | Not tested |
| twitch_get_schedule_icalendar | 🔧 | - | Fixed: added type safety for string response |
| twitch_update_schedule_segment | ⬜ | channel:manage:schedule | Not tested |

## Search Module (2 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_search_categories | ✅ | - | Public - Found categories for "minecraft" |
| twitch_search_channels | 🔧 | - | Fixed: empty string → None validator for `started_at` |

## Streams Module (3 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_streams | ✅ | - | Public - Got 20 live streams |
| twitch_get_stream_markers | ⬜ | user:read:broadcast | Not tested |
| twitch_create_stream_marker | ✅ | channel:manage:broadcast | **LIVE TEST SUCCESS** - Marker at 6490s |

## Subscriptions Module (2 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_broadcaster_subscriptions | ⏭️ | channel:read:subscriptions | Missing scope |
| twitch_check_user_subscription | ⬜ | user:read:subscriptions | Not tested |

## Teams Module (2 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_channel_teams | ⬜ | - | Public endpoint - Not tested |
| twitch_get_teams | ✅ | - | Public - Found team: staff |

## Users Module (8 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_users | ✅ | - | Public - Found: L_dray |
| twitch_update_user | ⬜ | user:edit | Not tested |
| twitch_get_user_block_list | ⬜ | user:read:blocked_users | Not tested |
| twitch_block_user | ⬜ | user:manage:blocked_users | Not tested |
| twitch_unblock_user | ⬜ | user:manage:blocked_users | Not tested |
| twitch_get_user_extensions | ⬜ | user:read:broadcast | Not tested |
| twitch_get_user_active_extensions | ⬜ | - | Not tested |
| twitch_update_user_extensions | ⬜ | user:edit:broadcast | Not tested |

## Videos Module (2 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_videos | ✅ | - | Public - Got videos for user |
| twitch_delete_videos | ⬜ | channel:manage:videos | Not tested |

## Whispers Module (1 tool)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_send_whisper | ⬜ | user:manage:whispers | Not tested |

---

## SDK Bugs Found & Fixed ✅

All 10 bugs fixed in twitch-sdk commit `a5aedd5` (2026-01-22).

| Bug | Severity | File | Fix Applied |
|-----|----------|------|-------------|
| search_channels validation | High | schemas/search.py | ✅ Added `@field_validator` to convert empty string → None |
| send_chat_message missing | High | schemas/chat.py | ✅ Added `SendChatMessageRequest` alias |
| send_announcement missing | High | endpoints/chat.py | ✅ Added `send_announcement` alias |
| modify_channel_info missing | High | endpoints/channels.py | ✅ Added `modify_channel_info` alias |
| PollChoice requires id | High | schemas/polls.py | ✅ Made `id` field optional |
| PredictionOutcome requires id/color | High | schemas/predictions.py | ✅ Made `id` and `color` optional |
| get_channel_schedule schema | Medium | schemas/schedule.py | ✅ Added `GetChannelScheduleRequest` alias |
| get_schedule_icalendar | Medium | endpoints/schedule.py | ✅ Added type safety for string response |
| get_goals missing | Medium | endpoints/goals.py | ✅ Added `get_goals` alias |
| get_hype_train schema | Medium | schemas/hype_train.py | ✅ Added `GetHypeTrainRequest` alias |

## Missing OAuth Scopes

The current token is missing these scopes needed for full testing:
- `moderator:read:chatters`
- `channel:read:editors`
- `channel:read:vips` / `channel:manage:vips`
- `moderation:read`
- `moderator:read:blocked_terms` / `moderator:manage:blocked_terms`
- `moderator:read:automod_settings`
- `moderator:read:shield_mode` / `moderator:manage:shield_mode`
- `clips:edit`
- `channel:read:redemptions` / `channel:manage:redemptions`
- `channel:read:subscriptions`
- `channel:read:charity`
- `bits:read`
- `channel:manage:moderators`

## Next Steps

1. ~~**Fix SDK bugs**~~ ✅ All 10 bugs fixed (2026-01-22)
2. **Retest fixed tools** - Run live API tests on 🔧 Fixed tools
3. **Regenerate token** - Create new token with all required scopes
4. **Full retest** - Run complete test suite with expanded scopes
5. **App token support** - Add app access token for conduit endpoints

# QA Test Matrix - Twitch MCP Tools

Total Tools: 109
**Test Date**: 2026-01-22
**SDK Version**: twitch-sdk 0.1.4
**OAuth Scopes**: 30 scopes configured

## Legend
- Status: ⬜ Not tested | ✅ Passed | ⏭️ Skipped (missing scope/special requirement)

## Summary

| Category | Passed | Skipped | Not Tested | Total |
|----------|--------|---------|------------|-------|
| Users | 2 | 0 | 6 | 8 |
| Streams | 2 | 0 | 1 | 3 |
| Games | 2 | 0 | 0 | 2 |
| Search | 2 | 0 | 0 | 2 |
| Channels | 5 | 2 | 1 | 8 |
| Chat | 2 | 0 | 5 | 7 |
| Moderation | 2 | 6 | 10 | 18 |
| Bits | 2 | 1 | 0 | 3 |
| Clips | 1 | 1 | 0 | 2 |
| Videos | 1 | 0 | 1 | 2 |
| Polls | 1 | 0 | 2 | 3 |
| Predictions | 1 | 0 | 2 | 3 |
| Goals | 1 | 0 | 0 | 1 |
| Schedule | 0 | 1 | 5 | 6 |
| Teams | 1 | 0 | 1 | 2 |
| EventSub | 1 | 5 | 3 | 9 |
| Subscriptions | 0 | 1 | 1 | 2 |
| Ads | 0 | 3 | 0 | 3 |
| Analytics | 0 | 2 | 0 | 2 |
| Channel Points | 0 | 4 | 2 | 6 |
| Charity | 0 | 2 | 0 | 2 |
| Guest Star | 0 | 1 | 11 | 12 |
| Raids | 0 | 1 | 1 | 2 |
| Whispers | 0 | 0 | 1 | 1 |

**Pass Rate**: 26/109 (24%) - Core read operations verified working

---

## Users Module (8 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_users | ✅ | - | Public - Found: L_dray |
| twitch_update_user | ⬜ | user:edit | Not tested (would modify) |
| twitch_get_user_block_list | ⬜ | user:read:blocked_users | Not tested |
| twitch_block_user | ⬜ | user:manage:blocked_users | Not tested |
| twitch_unblock_user | ⬜ | user:manage:blocked_users | Not tested |
| twitch_get_user_extensions | ⬜ | user:read:broadcast | Not tested |
| twitch_get_user_active_extensions | ✅ | - | Works |
| twitch_update_user_extensions | ⬜ | user:edit:broadcast | Not tested |

## Streams Module (3 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_streams | ✅ | - | Public - Returns live streams |
| twitch_get_followed_streams | ✅ | user:read:follows | Works - Returns followed live streams |
| twitch_get_stream_markers | ⬜ | user:read:broadcast | Not tested |

## Games Module (2 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_top_games | ✅ | - | Public - Returns top games |
| twitch_get_games | ✅ | - | Public - Found: Fortnite |

## Search Module (2 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_search_categories | ✅ | - | Public - Found categories |
| twitch_search_channels | ✅ | - | Public - Found channels (fixed in SDK 0.1.2) |

## Channels Module (8 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_channel_info | ✅ | - | Public - Got channel: L_dray |
| twitch_modify_channel_info | ⬜ | channel:manage:broadcast | Not tested (would modify) |
| twitch_get_channel_followers | ✅ | moderator:read:followers | 12 followers |
| twitch_get_followed_channels | ✅ | user:read:follows | Works |
| twitch_get_vips | ✅ | channel:read:vips | Works - No VIPs |
| twitch_add_vip | ⏭️ | channel:manage:vips | Not tested (would modify) |
| twitch_remove_vip | ⏭️ | channel:manage:vips | Not tested (would modify) |
| twitch_get_channel_editors | ✅ | channel:read:editors | Works - No editors |

## Chat Module (7 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_send_chat_message | ⬜ | user:write:chat | Not tested (would send) |
| twitch_get_chat_settings | ✅ | - | Public - Returns settings |
| twitch_update_chat_settings | ⬜ | moderator:manage:chat_settings | Not tested |
| twitch_get_chatters | ✅ | moderator:read:chatters | Works - 0 chatters when offline |
| twitch_send_chat_announcement | ⬜ | moderator:manage:announcements | Not tested (would send) |
| twitch_send_shoutout | ⬜ | moderator:manage:shoutouts | Not tested |
| twitch_get_user_emotes | ⬜ | user:read:emotes | Not tested |

## Moderation Module (18 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_moderators | ✅ | moderation:read | Works - No moderators |
| twitch_get_banned_users | ✅ | moderation:read | Works - No banned users |
| twitch_ban_user | ⬜ | moderator:manage:banned_users | Not tested |
| twitch_unban_user | ⬜ | moderator:manage:banned_users | Not tested |
| twitch_warn_user | ⬜ | moderator:manage:warnings | Not tested |
| twitch_delete_chat_messages | ⬜ | moderator:manage:chat_messages | Not tested |
| twitch_add_moderator | ⏭️ | channel:manage:moderators | Not tested (would modify) |
| twitch_remove_moderator | ⏭️ | channel:manage:moderators | Not tested (would modify) |
| twitch_get_blocked_terms | ⏭️ | moderator:read:blocked_terms | Scope not in token |
| twitch_add_blocked_term | ⏭️ | moderator:manage:blocked_terms | Scope not in token |
| twitch_remove_blocked_term | ⏭️ | moderator:manage:blocked_terms | Scope not in token |
| twitch_get_shield_mode_status | ⬜ | moderator:read:shield_mode | Not tested |
| twitch_update_shield_mode | ⬜ | moderator:manage:shield_mode | Not tested |
| twitch_get_unban_requests | ⬜ | moderator:read:unban_requests | Not tested |
| twitch_resolve_unban_request | ⬜ | moderator:manage:unban_requests | Not tested |
| twitch_get_automod_settings | ⬜ | moderator:read:automod_settings | Not tested |
| twitch_update_automod_settings | ⬜ | moderator:manage:automod_settings | Not tested |
| twitch_manage_held_automod_message | ⬜ | moderator:manage:automod | Not tested |

## Bits Module (3 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_bits_leaderboard | ✅ | bits:read | Works - 0 bits (fixed in SDK 0.1.3) |
| twitch_get_cheermotes | ✅ | - | Public - Returns cheermotes (fixed in SDK 0.1.4) |
| twitch_get_extension_transactions | ⏭️ | - | Extension developer only |

## Clips Module (2 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_clips | ✅ | - | Public - No clips found |
| twitch_create_clip | ⏭️ | clips:edit | Requires live stream |

## Videos Module (2 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_videos | ✅ | - | Public - Returns videos |
| twitch_delete_videos | ⬜ | channel:manage:videos | Not tested |

## Polls Module (3 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_polls | ✅ | channel:read:polls | Works - No polls found |
| twitch_create_poll | ⬜ | channel:manage:polls | Not tested (would create) |
| twitch_end_poll | ⬜ | channel:manage:polls | Not tested |

## Predictions Module (3 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_predictions | ✅ | channel:read:predictions | Works - No predictions |
| twitch_create_prediction | ⬜ | channel:manage:predictions | Not tested (would create) |
| twitch_end_prediction | ⬜ | channel:manage:predictions | Not tested |

## Goals Module (1 tool)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_goals | ✅ | channel:read:goals | Works - No active goals |

## Schedule Module (6 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_channel_schedule | ⏭️ | - | Returns 404 when no schedule (expected) |
| twitch_update_channel_schedule | ⬜ | channel:manage:schedule | Not tested |
| twitch_create_schedule_segment | ⬜ | channel:manage:schedule | Not tested |
| twitch_delete_schedule_segment | ⬜ | channel:manage:schedule | Not tested |
| twitch_get_schedule_icalendar | ⬜ | - | Not tested |
| twitch_update_schedule_segment | ⬜ | channel:manage:schedule | Not tested |

## Teams Module (2 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_teams | ✅ | - | Public - Found team: staff |
| twitch_get_channel_teams | ⬜ | - | Not tested |

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

## Subscriptions Module (2 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_broadcaster_subscriptions | ⏭️ | channel:read:subscriptions | Requires affiliate/partner |
| twitch_check_user_subscription | ⬜ | user:read:subscriptions | Not tested |

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

## Channel Points Module (6 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_custom_rewards | ⏭️ | channel:read:redemptions | Requires affiliate/partner |
| twitch_create_custom_reward | ⏭️ | channel:manage:redemptions | Requires affiliate/partner |
| twitch_update_custom_reward | ⏭️ | channel:manage:redemptions | Requires affiliate/partner |
| twitch_delete_custom_reward | ⏭️ | channel:manage:redemptions | Requires affiliate/partner |
| twitch_get_custom_reward_redemption | ⬜ | channel:read:redemptions | Not tested |
| twitch_update_redemption_status | ⬜ | channel:manage:redemptions | Not tested |

## Charity Module (2 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_charity_campaign | ⏭️ | channel:read:charity | Missing scope |
| twitch_get_charity_donations | ⏭️ | channel:read:charity | Missing scope |

## Guest Star Module (12 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_get_guest_star_settings | ⬜ | channel:read:guest_star | Not tested |
| twitch_get_guest_star_session | ⬜ | channel:read:guest_star | Not tested |
| twitch_create_guest_star_session | ⏭️ | channel:manage:guest_star | Requires live stream |
| twitch_end_guest_star_session | ⬜ | channel:manage:guest_star | Not tested |
| twitch_send_guest_star_invite | ⬜ | channel:manage:guest_star | Not tested |
| twitch_update_guest_star_settings | ⬜ | channel:manage:guest_star | Not tested |
| twitch_get_guest_star_invites | ⬜ | channel:read:guest_star | Not tested |
| twitch_delete_guest_star_invite | ⬜ | channel:manage:guest_star | Not tested |
| twitch_assign_guest_star_slot | ⬜ | channel:manage:guest_star | Not tested |
| twitch_update_guest_star_slot | ⬜ | channel:manage:guest_star | Not tested |
| twitch_delete_guest_star_slot | ⬜ | channel:manage:guest_star | Not tested |
| twitch_update_guest_star_slot_settings | ⬜ | channel:manage:guest_star | Not tested |

## Raids Module (2 tools)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_start_raid | ⏭️ | channel:manage:raids | Requires live stream + target |
| twitch_cancel_raid | ⬜ | channel:manage:raids | Not tested |

## Whispers Module (1 tool)

| Tool | Status | Auth Scope | Notes |
|------|--------|------------|-------|
| twitch_send_whisper | ⬜ | user:manage:whispers | Not tested |

---

## SDK Bug Fixes Published

### v0.1.2 (10 fixes)
- search_channels: empty `started_at` validation
- SendChatMessageRequest alias
- send_announcement alias
- modify_channel_info alias
- PollChoice.id now optional
- PredictionOutcome.id/color now optional
- GetChannelScheduleRequest alias
- get_schedule_icalendar type safety
- get_goals alias
- GetHypeTrainRequest alias

### v0.1.3
- DateRange: empty string → None for `started_at`/`ended_at`

### v0.1.4
- CheermoteTier.images: Fixed schema to use `dict[str, dict[str, dict[str, str]]]`

## Removed Endpoints

| Endpoint | Reason | Date |
|----------|--------|------|
| twitch_get_hype_train_events | Deprecated by Twitch (410 Gone) | 2026-01-22 |

## Open Issues

- **Issue #3**: Add app access token support for conduit endpoints
- **Issue #4**: Full retest tracking

## Notes

- Many tools are "Not tested" because they would modify state (create polls, ban users, etc.)
- Affiliate/Partner features cannot be tested without that account status
- Conduit endpoints require app access token (not user token)
- Schedule returns 404 when user has no schedule configured (expected behavior)

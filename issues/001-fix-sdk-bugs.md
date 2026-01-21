# Issue: Fix 10 SDK bugs found during QA testing

**Repository:** twitch-sdk
**Priority:** High
**Labels:** bug, sdk

## Summary
QA testing of twitch-mcp revealed 10 bugs in the SDK that need to be fixed.

## Bugs Found

| Bug | Severity | File | Issue |
|-----|----------|------|-------|
| search_channels validation | High | schemas/search.py | `started_at` field fails for offline channels (empty string instead of null) |
| send_chat_message missing | High | schemas/chat.py | `SendChatMessageRequest` not exported/defined |
| send_announcement missing | High | endpoints/chat.py | `send_announcement` function missing |
| modify_channel_info missing | High | endpoints/channels.py | `modify_channel_info` function missing |
| PollChoice requires id | High | schemas/polls.py | `id` field required but should be optional for creation |
| PredictionOutcome requires id/color | High | schemas/predictions.py | `id` and `color` required but should be optional for creation |
| get_channel_schedule schema | Medium | schemas/schedule.py | `GetChannelScheduleRequest` missing |
| get_schedule_icalendar | Medium | endpoints/schedule.py | Returns string but code expects model |
| get_goals missing | Medium | endpoints/goals.py | `get_goals` function missing |
| get_hype_train schema | Medium | schemas/hype_train.py | `GetHypeTrainRequest` missing |

## Acceptance Criteria
- [ ] All 10 bugs fixed
- [ ] Unit tests added for each fix
- [ ] QA retest passes

## Related
- QA Test Matrix: `twitch-mcp/QA_TEST_MATRIX.md`

# twitch-mcp

MCP server exposing the Twitch SDK as tools for AI assistants like Claude Code.

## Installation

```bash
pip install twitch-mcp
```

## Configuration

Add to your `~/.mcp.json`:

```json
{
  "mcpServers": {
    "twitch": {
      "command": "twitch-mcp",
      "env": {
        "TWITCH_ENV_FILE": "~/twitch-secrets/.env"
      }
    }
  }
}
```

Or with Poetry:

```json
{
  "mcpServers": {
    "twitch": {
      "command": "poetry",
      "args": ["run", "twitch-mcp"],
      "cwd": "/path/to/twitch-mcp",
      "env": {
        "TWITCH_ENV_FILE": "~/twitch-secrets/.env"
      }
    }
  }
}
```

## Available Tools

### Chat
- `twitch_send_chat_message` - Send a message to chat
- `twitch_get_chatters` - Get list of users in chat
- `twitch_send_announcement` - Send an announcement
- `twitch_send_shoutout` - Shoutout another broadcaster
- `twitch_get_chat_settings` - Get chat settings
- `twitch_update_chat_settings` - Update chat settings

### Streams
- `twitch_get_streams` - Get live streams
- `twitch_get_followed_streams` - Get followed live streams
- `twitch_create_stream_marker` - Create a stream marker

### Channels
- `twitch_get_channel_info` - Get channel information
- `twitch_modify_channel_info` - Update title, game, etc.
- `twitch_get_channel_followers` - Get followers
- `twitch_get_vips` / `twitch_add_vip` / `twitch_remove_vip`

### Clips
- `twitch_create_clip` - Create a clip
- `twitch_get_clips` - Get clips

### Polls & Predictions
- `twitch_create_poll` / `twitch_get_polls` / `twitch_end_poll`
- `twitch_create_prediction` / `twitch_get_predictions` / `twitch_end_prediction`

### Moderation
- `twitch_ban_user` / `twitch_unban_user`
- `twitch_warn_user`
- `twitch_delete_chat_messages`
- `twitch_get_moderators` / `twitch_add_moderator` / `twitch_remove_moderator`
- `twitch_get_blocked_terms` / `twitch_add_blocked_term`
- `twitch_get_shield_mode_status` / `twitch_update_shield_mode`

### Channel Points
- `twitch_get_custom_rewards` / `twitch_create_custom_reward` / `twitch_update_custom_reward` / `twitch_delete_custom_reward`
- `twitch_get_redemptions` / `twitch_update_redemption_status`

### And More...
- Ads, Analytics, Bits, Charity, EventSub, Games, Goals, Guest Star, Hype Train, Raids, Schedule, Search, Subscriptions, Teams, Users, Videos, Whispers

## Usage Examples

Ask Claude Code:
- "Send a chat message saying hello"
- "Create a poll asking what game to play next"
- "Get the list of chatters"
- "Start a raid to xQc"
- "Create a clip"
- "Update my stream title to 'Coding Session'"

## Dependencies

- twitch-sdk (API layer)
- mcp (MCP protocol)

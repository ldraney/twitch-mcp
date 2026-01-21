# twitch-mcp

[![PyPI](https://img.shields.io/pypi/v/twitch-mcp)](https://pypi.org/project/twitch-mcp/)

MCP server exposing the Twitch SDK as tools for AI assistants like Claude Code.

## Quick Start

### 1. Install

```bash
pip install twitch-mcp
```

### 2. Setup Credentials

Create `~/.twitch-secrets/.env`:

```bash
mkdir -p ~/.twitch-secrets
cat > ~/.twitch-secrets/.env << 'EOF'
TWITCH_CLIENT_ID=your_client_id
TWITCH_CLIENT_SECRET=your_client_secret
TWITCH_ACCESS_TOKEN=your_access_token
TWITCH_REFRESH_TOKEN=your_refresh_token
EOF
```

Get credentials from:
- **Client ID/Secret**: [Twitch Developer Console](https://dev.twitch.tv/console/apps)
- **Access/Refresh Tokens**: Use [Twitch CLI](https://dev.twitch.tv/docs/cli/) or an OAuth app

### 3. Configure Claude Code

Add to `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "twitch": {
      "command": "twitch-mcp"
    }
  }
}
```

### 4. Restart Claude Code

Run `/mcp` to verify the twitch server is connected.

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

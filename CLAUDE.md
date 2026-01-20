# CLAUDE.md - twitch-mcp

## Project Overview

MCP server that exposes all Twitch SDK endpoints as tools for AI assistants.

## Architecture

```
twitch-mcp/
├── src/twitch_mcp/
│   ├── __init__.py
│   ├── server.py        # MCP server entry point
│   └── tools/           # Tool definitions
│       ├── chat.py      # Chat tools
│       ├── streams.py   # Streams tools
│       ├── channels.py  # Channels tools
│       └── ... (26 modules)
└── tests/
```

## Running

```bash
# Development
cd ~/twitch-mcp && poetry run twitch-mcp

# With custom env file
TWITCH_ENV_FILE=~/twitch-secrets/.env poetry run twitch-mcp
```

## Adding to Claude Code

Add to `~/.mcp.json`:
```json
{
  "mcpServers": {
    "twitch": {
      "command": "poetry",
      "args": ["run", "twitch-mcp"],
      "cwd": "/Users/ldraney/twitch-mcp",
      "env": {
        "TWITCH_ENV_FILE": "/Users/ldraney/twitch-secrets/.env"
      }
    }
  }
}
```

## Tool Naming Convention

All tools are prefixed with `twitch_`:
- `twitch_send_chat_message`
- `twitch_get_streams`
- `twitch_create_poll`

## Dependencies

- twitch-sdk (API layer)
- mcp (MCP SDK)

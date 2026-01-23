# CLAUDE.md - twitch-mcp

## Project Overview

MCP server that exposes all Twitch SDK endpoints as tools for AI assistants.

## Quick Start

1. Create a Twitch app at https://dev.twitch.tv/console/apps
   - OAuth Redirect URL: `http://localhost:3000/callback`
   - Category: Application Integration
2. Run setup:
   ```bash
   poetry run twitch-mcp-setup
   ```
3. Restart Claude Code

That's it! The setup generates `.mcp.json` automatically.

## Architecture

```
twitch-mcp/
├── src/twitch_mcp/
│   ├── __init__.py
│   ├── server.py        # MCP server entry point
│   ├── setup.py         # OAuth setup & .mcp.json generator
│   └── tools/           # Tool definitions
│       ├── chat.py      # Chat tools
│       ├── streams.py   # Streams tools
│       ├── channels.py  # Channels tools
│       └── ... (26 modules)
└── tests/
```

## Local Config

The setup generates `.mcp.json` in the repo root with your credentials:
- `.mcp.json` - Your local config (gitignored, contains credentials)
- `.mcp.json.example` - Template for reference

## Running Manually

```bash
# Development
poetry run twitch-mcp

# With custom env file (alternative to .mcp.json)
TWITCH_ENV_FILE=~/twitch-secrets/.env poetry run twitch-mcp
```

## Tool Naming Convention

All tools are prefixed with `twitch_`:
- `twitch_send_chat_message`
- `twitch_get_streams`
- `twitch_create_poll`

## Dependencies

- twitch-sdk (API layer)
- mcp (MCP SDK)

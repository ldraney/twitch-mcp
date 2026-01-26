"""Twitch MCP Server - Main entry point."""

import asyncio
import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Callable, Awaitable

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


REQUIRED_VARS = [
    "TWITCH_CLIENT_ID",
    "TWITCH_CLIENT_SECRET",
    "TWITCH_ACCESS_TOKEN",
    "TWITCH_REFRESH_TOKEN",
]


def fetch_credentials_from_backend() -> bool:
    """Fetch Twitch credentials from Collaborative Story Stream backend.

    Returns True if credentials were successfully fetched and set.
    """
    css_token = os.environ.get("CSS_TOKEN")
    backend_url = os.environ.get("CSS_BACKEND_URL", "https://storystream.fly.dev")

    if not css_token:
        return False

    try:
        response = httpx.get(
            f"{backend_url}/v1/credentials",
            headers={"Authorization": f"Bearer {css_token}"},
            timeout=10.0,
        )
        response.raise_for_status()
        creds = response.json()

        # Set environment variables for TwitchSDK
        # Note: CLIENT_SECRET is required by TwitchCredentials but not used for API calls
        # when we already have an access token. We use a placeholder value.
        os.environ["TWITCH_CLIENT_ID"] = creds["twitch_client_id"]
        os.environ["TWITCH_CLIENT_SECRET"] = creds.get("twitch_client_secret", "placeholder")
        os.environ["TWITCH_ACCESS_TOKEN"] = creds["twitch_access_token"]
        os.environ["TWITCH_REFRESH_TOKEN"] = creds["twitch_refresh_token"]

        print(f"✓ Loaded Twitch credentials from {backend_url}", file=sys.stderr)
        return True

    except httpx.HTTPStatusError as e:
        print(f"Backend auth failed: HTTP {e.response.status_code}", file=sys.stderr)
        return False
    except httpx.RequestError as e:
        print(f"Backend auth failed: {e}", file=sys.stderr)
        return False
    except KeyError as e:
        print(f"Backend response missing key: {e}", file=sys.stderr)
        return False


def load_env_file():
    """Load environment variables from TWITCH_ENV_FILE if specified."""
    env_file = os.environ.get("TWITCH_ENV_FILE")
    if env_file:
        env_path = Path(env_file).expanduser()
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, _, value = line.partition("=")
                        # Remove quotes if present
                        value = value.strip().strip("'\"")
                        os.environ[key.strip()] = value
        else:
            print(f"Warning: TWITCH_ENV_FILE={env_file} does not exist", file=sys.stderr)


def check_credentials() -> list[str]:
    """Check for missing credentials. Returns list of missing var names."""
    return [var for var in REQUIRED_VARS if not os.environ.get(var)]


def print_credential_error(missing: list[str]):
    """Print a helpful error message for missing credentials."""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║  Missing Twitch credentials                                      ║
╚══════════════════════════════════════════════════════════════════╝
""", file=sys.stderr)

    print(f"Missing: {', '.join(missing)}\n", file=sys.stderr)

    print("""Option 1: Use Collaborative Story Stream (Recommended)
────────────────────────────────────────────────────────────────────
  1. Visit https://storystream.fly.dev and login with Twitch
  2. Copy your CSS_TOKEN from the dashboard
  3. Add to your .mcp.json:
     "env": { "CSS_TOKEN": "css_live_xxx..." }

Option 2: Run setup wizard
────────────────────────────────────────────────────────────────────
    poetry run twitch-mcp-setup

This will:
  1. Guide you to create a Twitch app at dev.twitch.tv
  2. Run OAuth to get your tokens
  3. Generate .mcp.json for Claude Code

Option 3: Set environment variables manually
────────────────────────────────────────────────────────────────────
  export TWITCH_CLIENT_ID=xxx
  export TWITCH_CLIENT_SECRET=xxx
  export TWITCH_ACCESS_TOKEN=xxx
  export TWITCH_REFRESH_TOKEN=xxx

Get credentials at: https://dev.twitch.tv/console/apps
""", file=sys.stderr)


# Try backend auth first (Collaborative Story Stream), then fall back to env file
if not fetch_credentials_from_backend():
    load_env_file()

# Import SDK after env is loaded
from twitch_sdk import TwitchSDK

from .tools import (
    ads,
    analytics,
    bits,
    channel_points,
    channels,
    charity,
    chat,
    clips,
    eventsub,
    games,
    goals,
    guest_star,
    moderation,
    polls,
    predictions,
    raids,
    schedule,
    search,
    streams,
    subscriptions,
    teams,
    users,
    videos,
    whispers,
)

# Global SDK instance
_sdk: TwitchSDK | None = None


def get_sdk() -> TwitchSDK:
    """Get the global SDK instance."""
    global _sdk
    if _sdk is None:
        _sdk = TwitchSDK()
    return _sdk


@asynccontextmanager
async def sdk_lifespan():
    """Manage SDK lifecycle."""
    global _sdk

    # Check credentials before trying to init SDK
    missing = check_credentials()
    if missing:
        print_credential_error(missing)
        sys.exit(1)

    _sdk = TwitchSDK()
    try:
        yield
    finally:
        if _sdk:
            await _sdk.close()
            _sdk = None


# Type for tool handlers
ToolHandler = Callable[[TwitchSDK, dict], Awaitable[list[TextContent]]]


def create_server() -> Server:
    """Create and configure the MCP server."""
    server = Server("twitch-mcp")

    # Collect all tools and handlers from modules
    tool_modules = [
        ads,
        analytics,
        bits,
        channel_points,
        channels,
        charity,
        chat,
        clips,
        eventsub,
        games,
        goals,
        guest_star,
        moderation,
        polls,
        predictions,
        raids,
        schedule,
        search,
        streams,
        subscriptions,
        teams,
        users,
        videos,
        whispers,
    ]

    # Aggregate all tools and handlers
    all_tools: list[Tool] = []
    all_handlers: dict[str, ToolHandler] = {}

    for module in tool_modules:
        all_tools.extend(module.get_tools())
        all_handlers.update(module.get_handlers())

    # Register single list_tools handler
    @server.list_tools()
    async def list_tools():
        return all_tools

    # Register single call_tool handler
    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        handler = all_handlers.get(name)
        if handler is None:
            raise ValueError(f"Unknown tool: {name}")

        sdk = get_sdk()
        return await handler(sdk, arguments)

    return server


async def run_server():
    """Run the MCP server."""
    server = create_server()

    async with sdk_lifespan():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options(),
            )


def main():
    """Entry point for the MCP server."""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()

"""Twitch MCP Server - Main entry point."""

import asyncio
import os
from contextlib import asynccontextmanager

from mcp.server import Server
from mcp.server.stdio import stdio_server

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
    hype_train,
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
    _sdk = TwitchSDK()
    try:
        yield
    finally:
        if _sdk:
            await _sdk.close()
            _sdk = None


def create_server() -> Server:
    """Create and configure the MCP server."""
    server = Server("twitch-mcp")

    # Register all tools
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
        hype_train,
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

    for module in tool_modules:
        module.register_tools(server, get_sdk)

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

"""Twitch MCP Server - Main entry point."""

import asyncio
from contextlib import asynccontextmanager
from typing import Callable, Awaitable

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

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

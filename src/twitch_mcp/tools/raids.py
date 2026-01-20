"""Raids MCP tools."""

from typing import Callable

from mcp.server import Server
from mcp.types import Tool, TextContent

from twitch_sdk import TwitchSDK
from twitch_sdk.endpoints import raids
from twitch_sdk.schemas.raids import CancelRaidRequest, StartRaidRequest


def register_tools(server: Server, get_sdk: Callable[[], TwitchSDK]):
    """Register raids tools with the MCP server."""

    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="twitch_start_raid",
                description="Start a raid to another channel",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "from_broadcaster_id": {"type": "string", "description": "Your broadcaster ID"},
                        "to_broadcaster_id": {"type": "string", "description": "Channel to raid"},
                    },
                    "required": ["from_broadcaster_id", "to_broadcaster_id"],
                },
            ),
            Tool(
                name="twitch_cancel_raid",
                description="Cancel a pending raid",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "Your broadcaster ID"},
                    },
                    "required": ["broadcaster_id"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        sdk = get_sdk()

        if name == "twitch_start_raid":
            params = StartRaidRequest(**arguments)
            result = await raids.start_raid(sdk.http, params)
            raid = result.data[0]
            return [TextContent(type="text", text=f"Raid started!\nCreated: {raid.created_at}\nMature: {raid.is_mature}")]

        elif name == "twitch_cancel_raid":
            params = CancelRaidRequest(**arguments)
            await raids.cancel_raid(sdk.http, params)
            return [TextContent(type="text", text="Raid cancelled")]

        raise ValueError(f"Unknown tool: {name}")

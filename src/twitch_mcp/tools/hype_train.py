"""Hype Train MCP tools."""

from typing import Callable

from mcp.server import Server
from mcp.types import Tool, TextContent

from twitch_sdk import TwitchSDK
from twitch_sdk.endpoints import hype_train
from twitch_sdk.schemas.hype_train import GetHypeTrainEventsRequest


def register_tools(server: Server, get_sdk: Callable[[], TwitchSDK]):
    """Register hype train tools with the MCP server."""

    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="twitch_get_hype_train_events",
                description="Get hype train events for a broadcaster",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "first": {"type": "integer", "description": "Max results (max 100)"},
                    },
                    "required": ["broadcaster_id"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        sdk = get_sdk()

        if name == "twitch_get_hype_train_events":
            params = GetHypeTrainEventsRequest(**arguments)
            result = await hype_train.get_hype_train_events(sdk.http, params)
            events = [f"- {e.event_type} at {e.event_timestamp}" for e in result.data]
            return [TextContent(type="text", text=f"Hype Train Events:\n" + "\n".join(events) if events else "No hype train events")]

        raise ValueError(f"Unknown tool: {name}")

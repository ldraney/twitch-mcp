"""Analytics MCP tools."""

from typing import Callable

from mcp.server import Server
from mcp.types import Tool, TextContent

from twitch_sdk import TwitchSDK
from twitch_sdk.endpoints import analytics
from twitch_sdk.schemas.analytics import GetExtensionAnalyticsRequest, GetGameAnalyticsRequest


def register_tools(server: Server, get_sdk: Callable[[], TwitchSDK]):
    """Register analytics tools with the MCP server."""

    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="twitch_get_extension_analytics",
                description="Get analytics for extensions",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "extension_id": {"type": "string", "description": "Extension ID"},
                        "first": {"type": "integer", "description": "Max results (max 100)"},
                    },
                },
            ),
            Tool(
                name="twitch_get_game_analytics",
                description="Get analytics for games",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "game_id": {"type": "string", "description": "Game ID"},
                        "first": {"type": "integer", "description": "Max results (max 100)"},
                    },
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        sdk = get_sdk()

        if name == "twitch_get_extension_analytics":
            params = GetExtensionAnalyticsRequest(**arguments) if arguments else None
            result = await analytics.get_extension_analytics(sdk.http, params)
            analytics_list = [f"- Extension {a.extension_id}: {a.URL}" for a in result.data]
            return [TextContent(type="text", text="\n".join(analytics_list) if analytics_list else "No extension analytics")]

        elif name == "twitch_get_game_analytics":
            params = GetGameAnalyticsRequest(**arguments) if arguments else None
            result = await analytics.get_game_analytics(sdk.http, params)
            analytics_list = [f"- Game {a.game_id}: {a.URL}" for a in result.data]
            return [TextContent(type="text", text="\n".join(analytics_list) if analytics_list else "No game analytics")]

        raise ValueError(f"Unknown tool: {name}")

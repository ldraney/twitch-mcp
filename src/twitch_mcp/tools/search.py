"""Search MCP tools."""

from typing import Callable

from mcp.server import Server
from mcp.types import Tool, TextContent

from twitch_sdk import TwitchSDK
from twitch_sdk.endpoints import search
from twitch_sdk.schemas.search import SearchCategoriesRequest, SearchChannelsRequest


def register_tools(server: Server, get_sdk: Callable[[], TwitchSDK]):
    """Register search tools with the MCP server."""

    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="twitch_search_categories",
                description="Search for game/category names",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "first": {"type": "integer", "description": "Max results (max 100)"},
                    },
                    "required": ["query"],
                },
            ),
            Tool(
                name="twitch_search_channels",
                description="Search for channels by name",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "live_only": {"type": "boolean", "description": "Only show live channels"},
                        "first": {"type": "integer", "description": "Max results (max 100)"},
                    },
                    "required": ["query"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        sdk = get_sdk()

        if name == "twitch_search_categories":
            params = SearchCategoriesRequest(**arguments)
            result = await search.search_categories(sdk.http, params)
            categories = [f"- {c.name} (ID: {c.id})" for c in result.data]
            return [TextContent(type="text", text=f"Categories:\n" + "\n".join(categories) if categories else "No categories found")]

        elif name == "twitch_search_channels":
            params = SearchChannelsRequest(**arguments)
            result = await search.search_channels(sdk.http, params)
            channels = []
            for ch in result.data:
                live = " [LIVE]" if ch.is_live else ""
                channels.append(f"- {ch.display_name}{live}: {ch.title[:50]}... (ID: {ch.id})")
            return [TextContent(type="text", text=f"Channels:\n" + "\n".join(channels) if channels else "No channels found")]

        raise ValueError(f"Unknown tool: {name}")

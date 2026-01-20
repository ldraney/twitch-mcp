"""Clips MCP tools."""

from typing import Callable

from mcp.server import Server
from mcp.types import Tool, TextContent

from twitch_sdk import TwitchSDK
from twitch_sdk.endpoints import clips
from twitch_sdk.schemas.clips import CreateClipRequest, GetClipsRequest


def register_tools(server: Server, get_sdk: Callable[[], TwitchSDK]):
    """Register clips tools with the MCP server."""

    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="twitch_create_clip",
                description="Create a clip from a live stream",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "has_delay": {"type": "boolean", "description": "Add delay for clip processing"},
                    },
                    "required": ["broadcaster_id"],
                },
            ),
            Tool(
                name="twitch_get_clips",
                description="Get clips for a broadcaster or game",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "game_id": {"type": "string", "description": "The game ID"},
                        "id": {"type": "array", "items": {"type": "string"}, "description": "Specific clip IDs"},
                        "first": {"type": "integer", "description": "Max results (max 100)"},
                    },
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        sdk = get_sdk()

        if name == "twitch_create_clip":
            params = CreateClipRequest(**arguments)
            result = await clips.create_clip(sdk.http, params)
            clip = result.data[0]
            return [TextContent(type="text", text=f"Clip created!\nID: {clip.id}\nEdit URL: {clip.edit_url}")]

        elif name == "twitch_get_clips":
            params = GetClipsRequest(**arguments)
            result = await clips.get_clips(sdk.http, params)
            clip_list = []
            for c in result.data:
                clip_list.append(
                    f"- {c.title}\n"
                    f"  By: {c.creator_name} | Views: {c.view_count}\n"
                    f"  URL: {c.url}"
                )
            return [TextContent(type="text", text="\n".join(clip_list) if clip_list else "No clips found")]

        raise ValueError(f"Unknown tool: {name}")

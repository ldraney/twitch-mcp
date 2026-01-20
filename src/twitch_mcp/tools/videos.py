"""Videos MCP tools."""

from typing import Callable

from mcp.server import Server
from mcp.types import Tool, TextContent

from twitch_sdk import TwitchSDK
from twitch_sdk.endpoints import videos
from twitch_sdk.schemas.videos import DeleteVideosRequest, GetVideosRequest


def register_tools(server: Server, get_sdk: Callable[[], TwitchSDK]):
    """Register videos tools with the MCP server."""

    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="twitch_get_videos",
                description="Get videos by ID, user, or game",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "id": {"type": "array", "items": {"type": "string"}, "description": "Video IDs"},
                        "user_id": {"type": "string", "description": "User ID to get videos for"},
                        "game_id": {"type": "string", "description": "Game ID to get videos for"},
                        "type": {"type": "string", "description": "Filter: all, archive, highlight, upload"},
                        "sort": {"type": "string", "description": "Sort: time, trending, views"},
                        "first": {"type": "integer", "description": "Max results (max 100)"},
                    },
                },
            ),
            Tool(
                name="twitch_delete_videos",
                description="Delete videos (max 5 at once)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "id": {"type": "array", "items": {"type": "string"}, "description": "Video IDs to delete (max 5)"},
                    },
                    "required": ["id"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        sdk = get_sdk()

        if name == "twitch_get_videos":
            params = GetVideosRequest(**arguments)
            result = await videos.get_videos(sdk.http, params)
            video_list = []
            for v in result.data:
                video_list.append(
                    f"- {v.title}\n"
                    f"  By: {v.user_name} | Views: {v.view_count} | Duration: {v.duration}\n"
                    f"  URL: {v.url}"
                )
            return [TextContent(type="text", text="\n".join(video_list) if video_list else "No videos found")]

        elif name == "twitch_delete_videos":
            params = DeleteVideosRequest(**arguments)
            deleted = await videos.delete_videos(sdk.http, params)
            return [TextContent(type="text", text=f"Deleted videos: {', '.join(deleted)}")]

        raise ValueError(f"Unknown tool: {name}")

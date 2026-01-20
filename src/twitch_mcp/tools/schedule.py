"""Schedule MCP tools."""

from typing import Callable

from mcp.server import Server
from mcp.types import Tool, TextContent

from twitch_sdk import TwitchSDK
from twitch_sdk.endpoints import schedule
from twitch_sdk.schemas.schedule import (
    CreateScheduleSegmentRequest,
    DeleteScheduleSegmentRequest,
    GetScheduleRequest,
    UpdateScheduleRequest,
    UpdateScheduleSegmentRequest,
)


def register_tools(server: Server, get_sdk: Callable[[], TwitchSDK]):
    """Register schedule tools with the MCP server."""

    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="twitch_get_channel_schedule",
                description="Get a broadcaster's streaming schedule",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "first": {"type": "integer", "description": "Max segments (max 25)"},
                    },
                    "required": ["broadcaster_id"],
                },
            ),
            Tool(
                name="twitch_update_channel_schedule",
                description="Update channel schedule settings (vacation mode)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "is_vacation_enabled": {"type": "boolean", "description": "Enable vacation mode"},
                        "vacation_start_time": {"type": "string", "description": "Vacation start (RFC3339)"},
                        "vacation_end_time": {"type": "string", "description": "Vacation end (RFC3339)"},
                        "timezone": {"type": "string", "description": "Timezone (e.g., America/New_York)"},
                    },
                    "required": ["broadcaster_id"],
                },
            ),
            Tool(
                name="twitch_create_schedule_segment",
                description="Create a scheduled stream segment",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "start_time": {"type": "string", "description": "Start time (RFC3339)"},
                        "timezone": {"type": "string", "description": "Timezone (e.g., America/New_York)"},
                        "duration": {"type": "integer", "description": "Duration in minutes (30-1440)"},
                        "is_recurring": {"type": "boolean", "description": "Whether this is weekly recurring"},
                        "category_id": {"type": "string", "description": "Game/category ID"},
                        "title": {"type": "string", "description": "Stream title"},
                    },
                    "required": ["broadcaster_id", "start_time", "timezone", "duration"],
                },
            ),
            Tool(
                name="twitch_delete_schedule_segment",
                description="Delete a scheduled stream segment",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "id": {"type": "string", "description": "Segment ID to delete"},
                    },
                    "required": ["broadcaster_id", "id"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        sdk = get_sdk()

        if name == "twitch_get_channel_schedule":
            params = GetScheduleRequest(**arguments)
            result = await schedule.get_channel_stream_schedule(sdk.http, params)
            sched = result.get("data", {})
            segments = sched.get("segments", [])
            seg_list = []
            for s in segments:
                seg_list.append(f"- {s.get('title', 'Untitled')}\n  {s.get('start_time')} - {s.get('end_time')}")
            return [TextContent(type="text", text=f"Schedule:\n" + "\n".join(seg_list) if seg_list else "No scheduled streams")]

        elif name == "twitch_update_channel_schedule":
            params = UpdateScheduleRequest(**arguments)
            await schedule.update_channel_stream_schedule(sdk.http, params)
            return [TextContent(type="text", text="Schedule settings updated")]

        elif name == "twitch_create_schedule_segment":
            params = CreateScheduleSegmentRequest(**arguments)
            result = await schedule.create_channel_stream_schedule_segment(sdk.http, params)
            return [TextContent(type="text", text="Schedule segment created")]

        elif name == "twitch_delete_schedule_segment":
            params = DeleteScheduleSegmentRequest(**arguments)
            await schedule.delete_channel_stream_schedule_segment(sdk.http, params)
            return [TextContent(type="text", text="Schedule segment deleted")]

        raise ValueError(f"Unknown tool: {name}")

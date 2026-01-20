"""Guest Star MCP tools."""

from typing import Callable

from mcp.server import Server
from mcp.types import Tool, TextContent

from twitch_sdk import TwitchSDK
from twitch_sdk.endpoints import guest_star
from twitch_sdk.schemas.guest_star import (
    CreateGuestStarSessionRequest,
    EndGuestStarSessionRequest,
    GetGuestStarSessionRequest,
    GetGuestStarSettingsRequest,
    SendGuestStarInviteRequest,
)


def register_tools(server: Server, get_sdk: Callable[[], TwitchSDK]):
    """Register guest star tools with the MCP server."""

    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="twitch_get_guest_star_settings",
                description="Get guest star settings for a channel",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "moderator_id": {"type": "string", "description": "The moderator's user ID"},
                    },
                    "required": ["broadcaster_id", "moderator_id"],
                },
            ),
            Tool(
                name="twitch_get_guest_star_session",
                description="Get active guest star session",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "moderator_id": {"type": "string", "description": "The moderator's user ID"},
                    },
                    "required": ["broadcaster_id", "moderator_id"],
                },
            ),
            Tool(
                name="twitch_create_guest_star_session",
                description="Create a guest star session",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                    },
                    "required": ["broadcaster_id"],
                },
            ),
            Tool(
                name="twitch_end_guest_star_session",
                description="End a guest star session",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "session_id": {"type": "string", "description": "The session ID"},
                    },
                    "required": ["broadcaster_id", "session_id"],
                },
            ),
            Tool(
                name="twitch_send_guest_star_invite",
                description="Send a guest star invite",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "moderator_id": {"type": "string", "description": "The moderator's user ID"},
                        "session_id": {"type": "string", "description": "The session ID"},
                        "guest_id": {"type": "string", "description": "User ID to invite"},
                    },
                    "required": ["broadcaster_id", "moderator_id", "session_id", "guest_id"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        sdk = get_sdk()

        if name == "twitch_get_guest_star_settings":
            params = GetGuestStarSettingsRequest(**arguments)
            result = await guest_star.get_channel_guest_star_settings(sdk.http, params)
            settings = result.data[0]
            return [TextContent(type="text", text=f"Guest Star Settings:\n"
                f"Slot count: {settings.slot_count}\n"
                f"Browser audio: {settings.is_browser_source_audio_enabled}\n"
                f"Layout: {settings.group_layout}")]

        elif name == "twitch_get_guest_star_session":
            params = GetGuestStarSessionRequest(**arguments)
            result = await guest_star.get_guest_star_session(sdk.http, params)
            if not result.data:
                return [TextContent(type="text", text="No active guest star session")]
            session = result.data[0]
            guests = [f"  - {g.user_display_name} (slot {g.slot_id})" for g in session.guests]
            return [TextContent(type="text", text=f"Session ID: {session.id}\nGuests:\n" + "\n".join(guests))]

        elif name == "twitch_create_guest_star_session":
            params = CreateGuestStarSessionRequest(**arguments)
            result = await guest_star.create_guest_star_session(sdk.http, params)
            session = result.data[0]
            return [TextContent(type="text", text=f"Guest star session created: {session.id}")]

        elif name == "twitch_end_guest_star_session":
            params = EndGuestStarSessionRequest(**arguments)
            await guest_star.end_guest_star_session(sdk.http, params)
            return [TextContent(type="text", text="Guest star session ended")]

        elif name == "twitch_send_guest_star_invite":
            params = SendGuestStarInviteRequest(**arguments)
            await guest_star.send_guest_star_invite(sdk.http, params)
            return [TextContent(type="text", text="Guest star invite sent")]

        raise ValueError(f"Unknown tool: {name}")

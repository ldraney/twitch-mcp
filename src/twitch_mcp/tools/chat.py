"""Chat MCP tools."""

from typing import Callable

from mcp.server import Server
from mcp.types import Tool, TextContent

from twitch_sdk import TwitchSDK
from twitch_sdk.endpoints import chat
from twitch_sdk.schemas.chat import (
    GetChattersRequest,
    GetChatSettingsRequest,
    GetEmotesRequest,
    SendAnnouncementRequest,
    SendMessageRequest,
    ShoutoutRequest,
    UpdateChatSettingsRequest,
    UpdateUserChatColorRequest,
)


def register_tools(server: Server, get_sdk: Callable[[], TwitchSDK]):
    """Register chat tools with the MCP server."""

    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="twitch_send_chat_message",
                description="Send a message to a broadcaster's chat",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "sender_id": {"type": "string", "description": "The sender's user ID"},
                        "message": {"type": "string", "description": "The message to send"},
                        "reply_parent_message_id": {"type": "string", "description": "Message ID to reply to (optional)"},
                    },
                    "required": ["broadcaster_id", "sender_id", "message"],
                },
            ),
            Tool(
                name="twitch_get_chatters",
                description="Get list of users in a broadcaster's chat",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "moderator_id": {"type": "string", "description": "The moderator's user ID"},
                        "first": {"type": "integer", "description": "Max number of results (max 1000)"},
                    },
                    "required": ["broadcaster_id", "moderator_id"],
                },
            ),
            Tool(
                name="twitch_send_announcement",
                description="Send an announcement message to the chat",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "moderator_id": {"type": "string", "description": "The moderator's user ID"},
                        "message": {"type": "string", "description": "The announcement message"},
                        "color": {"type": "string", "description": "Color: blue, green, orange, purple, primary"},
                    },
                    "required": ["broadcaster_id", "moderator_id", "message"],
                },
            ),
            Tool(
                name="twitch_send_shoutout",
                description="Send a shoutout to another broadcaster",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "from_broadcaster_id": {"type": "string", "description": "Your broadcaster ID"},
                        "to_broadcaster_id": {"type": "string", "description": "Broadcaster to shoutout"},
                        "moderator_id": {"type": "string", "description": "The moderator's user ID"},
                    },
                    "required": ["from_broadcaster_id", "to_broadcaster_id", "moderator_id"],
                },
            ),
            Tool(
                name="twitch_get_chat_settings",
                description="Get chat settings for a channel",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                    },
                    "required": ["broadcaster_id"],
                },
            ),
            Tool(
                name="twitch_update_chat_settings",
                description="Update chat settings for a channel",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "moderator_id": {"type": "string", "description": "The moderator's user ID"},
                        "emote_mode": {"type": "boolean", "description": "Enable emote-only mode"},
                        "follower_mode": {"type": "boolean", "description": "Enable follower-only mode"},
                        "follower_mode_duration": {"type": "integer", "description": "Minutes user must follow before chatting"},
                        "slow_mode": {"type": "boolean", "description": "Enable slow mode"},
                        "slow_mode_wait_time": {"type": "integer", "description": "Seconds between messages"},
                        "subscriber_mode": {"type": "boolean", "description": "Enable subscriber-only mode"},
                        "unique_chat_mode": {"type": "boolean", "description": "Enable unique messages only"},
                    },
                    "required": ["broadcaster_id", "moderator_id"],
                },
            ),
            Tool(
                name="twitch_get_channel_emotes",
                description="Get custom emotes for a channel",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                    },
                    "required": ["broadcaster_id"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        sdk = get_sdk()

        if name == "twitch_send_chat_message":
            params = SendMessageRequest(**arguments)
            result = await chat.send_chat_message(sdk.http, params)
            return [TextContent(type="text", text=f"Message sent: {result.data[0].model_dump_json()}")]

        elif name == "twitch_get_chatters":
            params = GetChattersRequest(**arguments)
            result = await chat.get_chatters(sdk.http, params)
            chatters = [f"{c.user_name} ({c.user_id})" for c in result.data]
            return [TextContent(type="text", text=f"Chatters ({result.total}):\n" + "\n".join(chatters[:50]))]

        elif name == "twitch_send_announcement":
            params = SendAnnouncementRequest(**arguments)
            await chat.send_chat_announcement(sdk.http, params)
            return [TextContent(type="text", text="Announcement sent successfully")]

        elif name == "twitch_send_shoutout":
            params = ShoutoutRequest(**arguments)
            await chat.send_shoutout(sdk.http, params)
            return [TextContent(type="text", text="Shoutout sent successfully")]

        elif name == "twitch_get_chat_settings":
            params = GetChatSettingsRequest(**arguments)
            result = await chat.get_chat_settings(sdk.http, params)
            return [TextContent(type="text", text=result.data[0].model_dump_json(indent=2))]

        elif name == "twitch_update_chat_settings":
            params = UpdateChatSettingsRequest(**arguments)
            result = await chat.update_chat_settings(sdk.http, params)
            return [TextContent(type="text", text=f"Settings updated: {result.data[0].model_dump_json()}")]

        elif name == "twitch_get_channel_emotes":
            params = GetEmotesRequest(**arguments)
            result = await chat.get_channel_emotes(sdk.http, params)
            emotes = [f"{e.name} ({e.id})" for e in result.data]
            return [TextContent(type="text", text=f"Emotes:\n" + "\n".join(emotes))]

        raise ValueError(f"Unknown tool: {name}")

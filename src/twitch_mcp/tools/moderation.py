"""Moderation MCP tools."""

from typing import Callable

from mcp.server import Server
from mcp.types import Tool, TextContent

from twitch_sdk import TwitchSDK
from twitch_sdk.endpoints import moderation
from twitch_sdk.schemas.moderation import (
    AddBlockedTermRequest,
    AddModeratorRequest,
    BanUserData,
    BanUserRequest,
    DeleteChatMessagesRequest,
    GetAutoModSettingsRequest,
    GetBannedUsersRequest,
    GetBlockedTermsRequest,
    GetModeratorsRequest,
    GetShieldModeStatusRequest,
    RemoveBlockedTermRequest,
    RemoveModeratorRequest,
    UnbanUserRequest,
    UpdateShieldModeStatusRequest,
    WarnUserRequest,
)


def register_tools(server: Server, get_sdk: Callable[[], TwitchSDK]):
    """Register moderation tools with the MCP server."""

    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="twitch_ban_user",
                description="Ban a user from a channel",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "moderator_id": {"type": "string", "description": "The moderator's user ID"},
                        "user_id": {"type": "string", "description": "User ID to ban"},
                        "duration": {"type": "integer", "description": "Timeout duration in seconds (omit for permanent)"},
                        "reason": {"type": "string", "description": "Reason for the ban"},
                    },
                    "required": ["broadcaster_id", "moderator_id", "user_id"],
                },
            ),
            Tool(
                name="twitch_unban_user",
                description="Unban a user from a channel",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "moderator_id": {"type": "string", "description": "The moderator's user ID"},
                        "user_id": {"type": "string", "description": "User ID to unban"},
                    },
                    "required": ["broadcaster_id", "moderator_id", "user_id"],
                },
            ),
            Tool(
                name="twitch_get_banned_users",
                description="Get list of banned users",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "first": {"type": "integer", "description": "Max results (max 100)"},
                    },
                    "required": ["broadcaster_id"],
                },
            ),
            Tool(
                name="twitch_warn_user",
                description="Send a warning to a user in chat",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "moderator_id": {"type": "string", "description": "The moderator's user ID"},
                        "user_id": {"type": "string", "description": "User ID to warn"},
                        "reason": {"type": "string", "description": "Reason for the warning"},
                    },
                    "required": ["broadcaster_id", "moderator_id", "user_id", "reason"],
                },
            ),
            Tool(
                name="twitch_delete_chat_messages",
                description="Delete chat messages (specific message or all)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "moderator_id": {"type": "string", "description": "The moderator's user ID"},
                        "message_id": {"type": "string", "description": "Specific message ID to delete (omit to clear all)"},
                    },
                    "required": ["broadcaster_id", "moderator_id"],
                },
            ),
            Tool(
                name="twitch_get_moderators",
                description="Get list of moderators for a channel",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "first": {"type": "integer", "description": "Max results (max 100)"},
                    },
                    "required": ["broadcaster_id"],
                },
            ),
            Tool(
                name="twitch_add_moderator",
                description="Add a moderator to the channel",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "user_id": {"type": "string", "description": "User ID to make moderator"},
                    },
                    "required": ["broadcaster_id", "user_id"],
                },
            ),
            Tool(
                name="twitch_remove_moderator",
                description="Remove a moderator from the channel",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "user_id": {"type": "string", "description": "User ID to remove as moderator"},
                    },
                    "required": ["broadcaster_id", "user_id"],
                },
            ),
            Tool(
                name="twitch_get_blocked_terms",
                description="Get list of blocked terms",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "moderator_id": {"type": "string", "description": "The moderator's user ID"},
                        "first": {"type": "integer", "description": "Max results (max 100)"},
                    },
                    "required": ["broadcaster_id", "moderator_id"],
                },
            ),
            Tool(
                name="twitch_add_blocked_term",
                description="Add a blocked term",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "moderator_id": {"type": "string", "description": "The moderator's user ID"},
                        "text": {"type": "string", "description": "Term to block (2-500 chars)"},
                    },
                    "required": ["broadcaster_id", "moderator_id", "text"],
                },
            ),
            Tool(
                name="twitch_get_shield_mode_status",
                description="Get shield mode status",
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
                name="twitch_update_shield_mode",
                description="Enable or disable shield mode",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "moderator_id": {"type": "string", "description": "The moderator's user ID"},
                        "is_active": {"type": "boolean", "description": "True to enable, false to disable"},
                    },
                    "required": ["broadcaster_id", "moderator_id", "is_active"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        sdk = get_sdk()

        if name == "twitch_ban_user":
            ban_data = BanUserData(
                user_id=arguments.pop("user_id"),
                duration=arguments.pop("duration", None),
                reason=arguments.pop("reason", None),
            )
            params = BanUserRequest(data=ban_data, **arguments)
            result = await moderation.ban_user(sdk.http, params)
            ban = result.data[0]
            return [TextContent(type="text", text=f"User {ban.user_id} banned until {ban.end_time or 'permanent'}")]

        elif name == "twitch_unban_user":
            params = UnbanUserRequest(**arguments)
            await moderation.unban_user(sdk.http, params)
            return [TextContent(type="text", text="User unbanned successfully")]

        elif name == "twitch_get_banned_users":
            params = GetBannedUsersRequest(**arguments)
            result = await moderation.get_banned_users(sdk.http, params)
            banned = [f"- {b.user_name}: {b.reason or 'No reason'} (expires: {b.expires_at or 'never'})" for b in result.data]
            return [TextContent(type="text", text=f"Banned users:\n" + "\n".join(banned) if banned else "No banned users")]

        elif name == "twitch_warn_user":
            params = WarnUserRequest(**arguments)
            await moderation.warn_chat_user(sdk.http, params)
            return [TextContent(type="text", text="Warning sent")]

        elif name == "twitch_delete_chat_messages":
            params = DeleteChatMessagesRequest(**arguments)
            await moderation.delete_chat_messages(sdk.http, params)
            msg = "Specific message deleted" if arguments.get("message_id") else "All chat messages cleared"
            return [TextContent(type="text", text=msg)]

        elif name == "twitch_get_moderators":
            params = GetModeratorsRequest(**arguments)
            result = await moderation.get_moderators(sdk.http, params)
            mods = [f"- {m.user_name}" for m in result.data]
            return [TextContent(type="text", text=f"Moderators:\n" + "\n".join(mods) if mods else "No moderators")]

        elif name == "twitch_add_moderator":
            params = AddModeratorRequest(**arguments)
            await moderation.add_moderator(sdk.http, params)
            return [TextContent(type="text", text="Moderator added")]

        elif name == "twitch_remove_moderator":
            params = RemoveModeratorRequest(**arguments)
            await moderation.remove_moderator(sdk.http, params)
            return [TextContent(type="text", text="Moderator removed")]

        elif name == "twitch_get_blocked_terms":
            params = GetBlockedTermsRequest(**arguments)
            result = await moderation.get_blocked_terms(sdk.http, params)
            terms = [f"- {t.text}" for t in result.data]
            return [TextContent(type="text", text=f"Blocked terms:\n" + "\n".join(terms) if terms else "No blocked terms")]

        elif name == "twitch_add_blocked_term":
            params = AddBlockedTermRequest(**arguments)
            result = await moderation.add_blocked_term(sdk.http, params)
            return [TextContent(type="text", text=f"Blocked term added: {result.data[0].text}")]

        elif name == "twitch_get_shield_mode_status":
            params = GetShieldModeStatusRequest(**arguments)
            result = await moderation.get_shield_mode_status(sdk.http, params)
            status = result.data[0]
            return [TextContent(type="text", text=f"Shield mode: {'ACTIVE' if status.is_active else 'INACTIVE'}")]

        elif name == "twitch_update_shield_mode":
            params = UpdateShieldModeStatusRequest(**arguments)
            result = await moderation.update_shield_mode_status(sdk.http, params)
            status = result.data[0]
            return [TextContent(type="text", text=f"Shield mode {'enabled' if status.is_active else 'disabled'}")]

        raise ValueError(f"Unknown tool: {name}")

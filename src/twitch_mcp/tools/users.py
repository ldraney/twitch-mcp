"""Users MCP tools."""

from typing import Callable

from mcp.server import Server
from mcp.types import Tool, TextContent

from twitch_sdk import TwitchSDK
from twitch_sdk.endpoints import users
from twitch_sdk.schemas.users import (
    BlockUserRequest,
    GetUserBlockListRequest,
    GetUsersRequest,
    UnblockUserRequest,
    UpdateUserRequest,
)


def register_tools(server: Server, get_sdk: Callable[[], TwitchSDK]):
    """Register users tools with the MCP server."""

    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="twitch_get_users",
                description="Get user information by ID or login name",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "id": {"type": "array", "items": {"type": "string"}, "description": "User IDs"},
                        "login": {"type": "array", "items": {"type": "string"}, "description": "User login names"},
                    },
                },
            ),
            Tool(
                name="twitch_update_user",
                description="Update the authenticated user's description",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "description": {"type": "string", "description": "New channel description"},
                    },
                },
            ),
            Tool(
                name="twitch_get_user_block_list",
                description="Get list of users the broadcaster has blocked",
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
                name="twitch_block_user",
                description="Block a user",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "target_user_id": {"type": "string", "description": "User ID to block"},
                        "source_context": {"type": "string", "description": "Context: chat or whisper"},
                        "reason": {"type": "string", "description": "Reason: harassment, spam, or other"},
                    },
                    "required": ["target_user_id"],
                },
            ),
            Tool(
                name="twitch_unblock_user",
                description="Unblock a user",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "target_user_id": {"type": "string", "description": "User ID to unblock"},
                    },
                    "required": ["target_user_id"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        sdk = get_sdk()

        if name == "twitch_get_users":
            params = GetUsersRequest(**arguments) if arguments else None
            result = await users.get_users(sdk.http, params)
            user_list = []
            for u in result.data:
                user_list.append(
                    f"- {u.display_name} ({u.login})\n"
                    f"  ID: {u.id}\n"
                    f"  Type: {u.broadcaster_type or 'regular'}\n"
                    f"  Description: {u.description[:100]}..."
                )
            return [TextContent(type="text", text="\n".join(user_list) if user_list else "No users found")]

        elif name == "twitch_update_user":
            params = UpdateUserRequest(**arguments)
            result = await users.update_user(sdk.http, params)
            user = result.data[0]
            return [TextContent(type="text", text=f"User updated: {user.display_name}")]

        elif name == "twitch_get_user_block_list":
            params = GetUserBlockListRequest(**arguments)
            result = await users.get_user_block_list(sdk.http, params)
            blocked = [f"- {b.display_name} ({b.user_id})" for b in result.data]
            return [TextContent(type="text", text=f"Blocked users:\n" + "\n".join(blocked) if blocked else "No blocked users")]

        elif name == "twitch_block_user":
            params = BlockUserRequest(**arguments)
            await users.block_user(sdk.http, params)
            return [TextContent(type="text", text="User blocked")]

        elif name == "twitch_unblock_user":
            params = UnblockUserRequest(**arguments)
            await users.unblock_user(sdk.http, params)
            return [TextContent(type="text", text="User unblocked")]

        raise ValueError(f"Unknown tool: {name}")

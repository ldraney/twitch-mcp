"""Whispers MCP tools."""

from typing import Callable

from mcp.server import Server
from mcp.types import Tool, TextContent

from twitch_sdk import TwitchSDK
from twitch_sdk.endpoints import whispers
from twitch_sdk.schemas.whispers import SendWhisperRequest


def register_tools(server: Server, get_sdk: Callable[[], TwitchSDK]):
    """Register whispers tools with the MCP server."""

    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="twitch_send_whisper",
                description="Send a whisper (private message) to another user",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "from_user_id": {"type": "string", "description": "Your user ID"},
                        "to_user_id": {"type": "string", "description": "Recipient's user ID"},
                        "message": {"type": "string", "description": "Message to send (max 10000 chars)"},
                    },
                    "required": ["from_user_id", "to_user_id", "message"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        sdk = get_sdk()

        if name == "twitch_send_whisper":
            params = SendWhisperRequest(**arguments)
            await whispers.send_whisper(sdk.http, params)
            return [TextContent(type="text", text="Whisper sent")]

        raise ValueError(f"Unknown tool: {name}")

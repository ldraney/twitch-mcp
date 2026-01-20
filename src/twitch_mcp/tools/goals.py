"""Goals MCP tools."""

from typing import Callable

from mcp.server import Server
from mcp.types import Tool, TextContent

from twitch_sdk import TwitchSDK
from twitch_sdk.endpoints import goals
from twitch_sdk.schemas.goals import GetGoalsRequest


def register_tools(server: Server, get_sdk: Callable[[], TwitchSDK]):
    """Register goals tools with the MCP server."""

    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="twitch_get_creator_goals",
                description="Get the broadcaster's active creator goals",
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

        if name == "twitch_get_creator_goals":
            params = GetGoalsRequest(**arguments)
            result = await goals.get_creator_goals(sdk.http, params)
            goal_list = []
            for g in result.data:
                goal_list.append(f"- {g.description}\n  Type: {g.type}\n  Progress: {g.current_amount}/{g.target_amount}")
            return [TextContent(type="text", text=f"Creator Goals:\n" + "\n".join(goal_list) if goal_list else "No active goals")]

        raise ValueError(f"Unknown tool: {name}")

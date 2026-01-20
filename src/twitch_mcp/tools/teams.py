"""Teams MCP tools."""

from typing import Callable

from mcp.server import Server
from mcp.types import Tool, TextContent

from twitch_sdk import TwitchSDK
from twitch_sdk.endpoints import teams
from twitch_sdk.schemas.teams import GetChannelTeamsRequest, GetTeamsRequest


def register_tools(server: Server, get_sdk: Callable[[], TwitchSDK]):
    """Register teams tools with the MCP server."""

    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="twitch_get_teams",
                description="Get team information by name or ID",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Team name"},
                        "id": {"type": "string", "description": "Team ID"},
                    },
                },
            ),
            Tool(
                name="twitch_get_channel_teams",
                description="Get teams that a broadcaster is a member of",
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

        if name == "twitch_get_teams":
            params = GetTeamsRequest(**arguments)
            result = await teams.get_teams(sdk.http, params)
            team_list = []
            for t in result.data:
                members = len(t.users) if t.users else 0
                team_list.append(f"- {t.team_display_name} ({members} members)\n  {t.info[:100]}...")
            return [TextContent(type="text", text="\n".join(team_list) if team_list else "No teams found")]

        elif name == "twitch_get_channel_teams":
            params = GetChannelTeamsRequest(**arguments)
            result = await teams.get_channel_teams(sdk.http, params)
            team_list = [f"- {t.team_display_name}" for t in result.data]
            return [TextContent(type="text", text=f"Channel Teams:\n" + "\n".join(team_list) if team_list else "Not on any teams")]

        raise ValueError(f"Unknown tool: {name}")

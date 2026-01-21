"""Bits MCP tools."""

from typing import Callable

from mcp.server import Server
from mcp.types import Tool, TextContent

from twitch_sdk import TwitchSDK
from twitch_sdk.endpoints import bits
from twitch_sdk.schemas.bits import GetBitsLeaderboardRequest, GetCheermotesRequest, GetExtensionTransactionsRequest


def register_tools(server: Server, get_sdk: Callable[[], TwitchSDK]):
    """Register bits tools with the MCP server."""

    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="twitch_get_bits_leaderboard",
                description="Get bits leaderboard for a channel",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "count": {"type": "integer", "description": "Number of entries (max 100)"},
                        "period": {"type": "string", "description": "Time period: day, week, month, year, all"},
                        "user_id": {"type": "string", "description": "Get rank for specific user"},
                    },
                },
            ),
            Tool(
                name="twitch_get_cheermotes",
                description="Get cheermotes for a channel or global",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "Broadcaster ID (omit for global)"},
                    },
                },
            ),
            Tool(
                name="twitch_get_extension_transactions",
                description="Get extension transactions (for extension developers)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "extension_id": {"type": "string", "description": "Extension ID"},
                        "id": {"type": "array", "items": {"type": "string"}, "description": "Specific transaction IDs"},
                        "first": {"type": "integer", "description": "Max results (max 100)"},
                    },
                    "required": ["extension_id"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        sdk = get_sdk()

        if name == "twitch_get_bits_leaderboard":
            params = GetBitsLeaderboardRequest(**arguments) if arguments else None
            result = await bits.get_bits_leaderboard(sdk.http, params)
            entries = [f"{e.rank}. {e.user_name}: {e.score} bits" for e in result.data]
            return [TextContent(type="text", text=f"Bits Leaderboard (Total: {result.total}):\n" + "\n".join(entries))]

        elif name == "twitch_get_cheermotes":
            params = GetCheermotesRequest(**arguments) if arguments else None
            result = await bits.get_cheermotes(sdk.http, params)
            cheermotes = [f"- {c.prefix}" for c in result.data]
            return [TextContent(type="text", text=f"Cheermotes:\n" + "\n".join(cheermotes))]

        elif name == "twitch_get_extension_transactions":
            params = GetExtensionTransactionsRequest(**arguments)
            result = await bits.get_extension_transactions(sdk.http, params)
            txs = [f"- {t.id}: {t.user_name} ({t.product_type})" for t in result.data]
            return [TextContent(type="text", text=f"Extension Transactions:\n" + "\n".join(txs) if txs else "No transactions")]

        raise ValueError(f"Unknown tool: {name}")

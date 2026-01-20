"""EventSub MCP tools."""

from typing import Callable

from mcp.server import Server
from mcp.types import Tool, TextContent

from twitch_sdk import TwitchSDK
from twitch_sdk.endpoints import eventsub
from twitch_sdk.schemas.eventsub import (
    CreateEventSubSubscriptionRequest,
    DeleteEventSubSubscriptionRequest,
    GetEventSubSubscriptionsRequest,
)


def register_tools(server: Server, get_sdk: Callable[[], TwitchSDK]):
    """Register eventsub tools with the MCP server."""

    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="twitch_get_eventsub_subscriptions",
                description="Get list of EventSub subscriptions",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "description": "Filter by status"},
                        "type": {"type": "string", "description": "Filter by event type"},
                        "user_id": {"type": "string", "description": "Filter by user ID"},
                    },
                },
            ),
            Tool(
                name="twitch_create_eventsub_subscription",
                description="Create an EventSub subscription (webhook)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "description": "Event type (e.g., channel.follow)"},
                        "version": {"type": "string", "description": "Subscription version"},
                        "condition": {"type": "object", "description": "Subscription condition"},
                        "transport": {"type": "object", "description": "Transport config (method, callback, secret)"},
                    },
                    "required": ["type", "version", "condition", "transport"],
                },
            ),
            Tool(
                name="twitch_delete_eventsub_subscription",
                description="Delete an EventSub subscription",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "description": "Subscription ID to delete"},
                    },
                    "required": ["id"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        sdk = get_sdk()

        if name == "twitch_get_eventsub_subscriptions":
            params = GetEventSubSubscriptionsRequest(**arguments) if arguments else None
            result = await eventsub.get_eventsub_subscriptions(sdk.http, params)
            subs = []
            for s in result.data:
                subs.append(f"- {s.type} ({s.status})\n  ID: {s.id}")
            return [TextContent(type="text", text=f"EventSub Subscriptions ({result.total}, cost: {result.total_cost}/{result.max_total_cost}):\n" + "\n".join(subs))]

        elif name == "twitch_create_eventsub_subscription":
            params = CreateEventSubSubscriptionRequest(**arguments)
            result = await eventsub.create_eventsub_subscription(sdk.http, params)
            sub = result.data[0]
            return [TextContent(type="text", text=f"Subscription created:\nID: {sub.id}\nType: {sub.type}\nStatus: {sub.status}")]

        elif name == "twitch_delete_eventsub_subscription":
            params = DeleteEventSubSubscriptionRequest(**arguments)
            await eventsub.delete_eventsub_subscription(sdk.http, params)
            return [TextContent(type="text", text="Subscription deleted")]

        raise ValueError(f"Unknown tool: {name}")

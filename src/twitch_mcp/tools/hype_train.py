"""Hype Train MCP tools."""

from mcp.types import Tool, TextContent

from twitch_sdk import TwitchSDK
from twitch_sdk.endpoints import hype_train
from twitch_sdk.schemas.hype_train import GetHypeTrainEventsRequest


def get_tools() -> list[Tool]:
    """Return hype train tools."""
    return [
        Tool(
            name="twitch_get_hype_train_events",
            description="Get hype train events for a broadcaster",
            inputSchema={
                "type": "object",
                "properties": {
                    "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                    "first": {"type": "integer", "description": "Max results (max 100)"},
                },
                "required": ["broadcaster_id"],
            },
        ),
    ]


async def _handle_get_hype_train_events(sdk: TwitchSDK, arguments: dict) -> list[TextContent]:
    params = GetHypeTrainEventsRequest(**arguments)
    result = await hype_train.get_hype_train_events(sdk.http, params)
    events = [f"- {e.event_type} at {e.event_timestamp}" for e in result.data]
    return [TextContent(type="text", text=f"Hype Train Events:\n" + "\n".join(events) if events else "No hype train events")]


def get_handlers() -> dict:
    """Return handlers for hype train tools."""
    return {
        "twitch_get_hype_train_events": _handle_get_hype_train_events,
    }

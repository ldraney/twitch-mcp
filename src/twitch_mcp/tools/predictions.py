"""Predictions MCP tools."""

from typing import Callable

from mcp.server import Server
from mcp.types import Tool, TextContent

from twitch_sdk import TwitchSDK
from twitch_sdk.endpoints import predictions
from twitch_sdk.schemas.predictions import (
    CreatePredictionRequest,
    EndPredictionRequest,
    GetPredictionsRequest,
    PredictionOutcomeInput,
)


def register_tools(server: Server, get_sdk: Callable[[], TwitchSDK]):
    """Register predictions tools with the MCP server."""

    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="twitch_create_prediction",
                description="Create a prediction on a channel",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "title": {"type": "string", "description": "Prediction title (max 45 chars)"},
                        "outcomes": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of outcome titles (2-10 outcomes, max 25 chars each)",
                        },
                        "prediction_window": {"type": "integer", "description": "Seconds users can make predictions (30-1800)"},
                    },
                    "required": ["broadcaster_id", "title", "outcomes", "prediction_window"],
                },
            ),
            Tool(
                name="twitch_get_predictions",
                description="Get predictions for a channel",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "id": {"type": "array", "items": {"type": "string"}, "description": "Specific prediction IDs"},
                        "first": {"type": "integer", "description": "Max results (max 25)"},
                    },
                    "required": ["broadcaster_id"],
                },
            ),
            Tool(
                name="twitch_end_prediction",
                description="End/resolve a prediction",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "id": {"type": "string", "description": "The prediction ID"},
                        "status": {"type": "string", "description": "RESOLVED, CANCELED, or LOCKED"},
                        "winning_outcome_id": {"type": "string", "description": "The winning outcome ID (required for RESOLVED)"},
                    },
                    "required": ["broadcaster_id", "id", "status"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        sdk = get_sdk()

        if name == "twitch_create_prediction":
            # Convert string outcomes to PredictionOutcomeInput
            outcomes = [PredictionOutcomeInput(title=o) for o in arguments.pop("outcomes")]
            params = CreatePredictionRequest(outcomes=outcomes, **arguments)
            result = await predictions.create_prediction(sdk.http, params)
            pred = result.data[0]
            outcomes_str = ", ".join([f"{o.title} ({o.id})" for o in pred.outcomes])
            return [TextContent(type="text", text=f"Prediction created!\nID: {pred.id}\nTitle: {pred.title}\nOutcomes: {outcomes_str}")]

        elif name == "twitch_get_predictions":
            params = GetPredictionsRequest(**arguments)
            result = await predictions.get_predictions(sdk.http, params)
            pred_list = []
            for p in result.data:
                outcomes_str = "\n".join([f"    {o.title}: {o.channel_points} points ({o.users} users)" for o in p.outcomes])
                pred_list.append(
                    f"- {p.title} ({p.status})\n"
                    f"  Outcomes:\n{outcomes_str}"
                )
            return [TextContent(type="text", text="\n".join(pred_list) if pred_list else "No predictions found")]

        elif name == "twitch_end_prediction":
            params = EndPredictionRequest(**arguments)
            result = await predictions.end_prediction(sdk.http, params)
            pred = result.data[0]
            return [TextContent(type="text", text=f"Prediction ended: {pred.title} (Status: {pred.status})")]

        raise ValueError(f"Unknown tool: {name}")

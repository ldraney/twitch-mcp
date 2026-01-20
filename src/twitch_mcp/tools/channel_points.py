"""Channel Points MCP tools."""

from typing import Callable

from mcp.server import Server
from mcp.types import Tool, TextContent

from twitch_sdk import TwitchSDK
from twitch_sdk.endpoints import channel_points
from twitch_sdk.schemas.channel_points import (
    CreateCustomRewardRequest,
    DeleteCustomRewardRequest,
    GetCustomRewardRedemptionRequest,
    GetCustomRewardsRequest,
    UpdateCustomRewardRequest,
    UpdateRedemptionStatusRequest,
)


def register_tools(server: Server, get_sdk: Callable[[], TwitchSDK]):
    """Register channel points tools with the MCP server."""

    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="twitch_get_custom_rewards",
                description="Get custom channel point rewards",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "only_manageable_rewards": {"type": "boolean", "description": "Only show rewards the app can manage"},
                    },
                    "required": ["broadcaster_id"],
                },
            ),
            Tool(
                name="twitch_create_custom_reward",
                description="Create a custom channel point reward",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "title": {"type": "string", "description": "Reward title (max 45 chars)"},
                        "cost": {"type": "integer", "description": "Cost in channel points"},
                        "prompt": {"type": "string", "description": "Prompt for user input (max 200 chars)"},
                        "is_enabled": {"type": "boolean", "description": "Whether the reward is enabled"},
                        "is_user_input_required": {"type": "boolean", "description": "Require user input"},
                        "background_color": {"type": "string", "description": "Hex color code"},
                    },
                    "required": ["broadcaster_id", "title", "cost"],
                },
            ),
            Tool(
                name="twitch_update_custom_reward",
                description="Update a custom channel point reward",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "id": {"type": "string", "description": "The reward ID"},
                        "title": {"type": "string", "description": "Reward title"},
                        "cost": {"type": "integer", "description": "Cost in channel points"},
                        "is_enabled": {"type": "boolean", "description": "Whether the reward is enabled"},
                        "is_paused": {"type": "boolean", "description": "Whether the reward is paused"},
                    },
                    "required": ["broadcaster_id", "id"],
                },
            ),
            Tool(
                name="twitch_delete_custom_reward",
                description="Delete a custom channel point reward",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "id": {"type": "string", "description": "The reward ID"},
                    },
                    "required": ["broadcaster_id", "id"],
                },
            ),
            Tool(
                name="twitch_get_redemptions",
                description="Get redemptions for a custom reward",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "reward_id": {"type": "string", "description": "The reward ID"},
                        "status": {"type": "string", "description": "Filter: UNFULFILLED, FULFILLED, CANCELED"},
                        "first": {"type": "integer", "description": "Max results (max 50)"},
                    },
                    "required": ["broadcaster_id", "reward_id"],
                },
            ),
            Tool(
                name="twitch_update_redemption_status",
                description="Update the status of a redemption (fulfill or cancel)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "broadcaster_id": {"type": "string", "description": "The broadcaster's user ID"},
                        "reward_id": {"type": "string", "description": "The reward ID"},
                        "id": {"type": "array", "items": {"type": "string"}, "description": "Redemption IDs"},
                        "status": {"type": "string", "description": "New status: FULFILLED or CANCELED"},
                    },
                    "required": ["broadcaster_id", "reward_id", "id", "status"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        sdk = get_sdk()

        if name == "twitch_get_custom_rewards":
            params = GetCustomRewardsRequest(**arguments)
            result = await channel_points.get_custom_rewards(sdk.http, params)
            rewards = [f"- {r.title}: {r.cost} points (ID: {r.id})" for r in result.data]
            return [TextContent(type="text", text=f"Custom Rewards:\n" + "\n".join(rewards) if rewards else "No custom rewards")]

        elif name == "twitch_create_custom_reward":
            params = CreateCustomRewardRequest(**arguments)
            result = await channel_points.create_custom_reward(sdk.http, params)
            reward = result.data[0]
            return [TextContent(type="text", text=f"Reward created!\nID: {reward.id}\nTitle: {reward.title}\nCost: {reward.cost}")]

        elif name == "twitch_update_custom_reward":
            params = UpdateCustomRewardRequest(**arguments)
            result = await channel_points.update_custom_reward(sdk.http, params)
            reward = result.data[0]
            return [TextContent(type="text", text=f"Reward updated: {reward.title}")]

        elif name == "twitch_delete_custom_reward":
            params = DeleteCustomRewardRequest(**arguments)
            await channel_points.delete_custom_reward(sdk.http, params)
            return [TextContent(type="text", text="Reward deleted")]

        elif name == "twitch_get_redemptions":
            params = GetCustomRewardRedemptionRequest(**arguments)
            result = await channel_points.get_custom_reward_redemption(sdk.http, params)
            redemptions = [f"- {r.user_name}: {r.user_input or 'No input'} ({r.status})" for r in result.data]
            return [TextContent(type="text", text=f"Redemptions:\n" + "\n".join(redemptions) if redemptions else "No redemptions")]

        elif name == "twitch_update_redemption_status":
            params = UpdateRedemptionStatusRequest(**arguments)
            result = await channel_points.update_redemption_status(sdk.http, params)
            return [TextContent(type="text", text=f"Updated {len(result.data)} redemption(s)")]

        raise ValueError(f"Unknown tool: {name}")

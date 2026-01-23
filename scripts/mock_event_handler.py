#!/usr/bin/env python3
"""AI-powered mock EventSub event handler for Twitch streams."""

import asyncio
import json
import os
import sys
from datetime import datetime

import websockets

# Mock websocket URL (Twitch CLI)
MOCK_WS_URL = "ws://127.0.0.1:8765/ws"


def format_event(event_type: str, data: dict) -> str:
    """Format event for display."""
    timestamp = datetime.now().strftime("%H:%M:%S")

    if event_type == "channel.subscribe":
        user = data.get("user_name", "Someone")
        tier = {"1000": "Tier 1", "2000": "Tier 2", "3000": "Tier 3"}.get(data.get("tier", "1000"), "Tier 1")
        is_gift = data.get("is_gift", False)
        if is_gift:
            return f"[{timestamp}] GIFT SUB: {user} received a {tier} gift sub!"
        return f"[{timestamp}] NEW SUB: {user} subscribed at {tier}!"

    elif event_type == "channel.cheer":
        user = data.get("user_name", "Anonymous")
        bits = data.get("bits", 0)
        message = data.get("message", "")
        return f"[{timestamp}] CHEER: {user} cheered {bits} bits! \"{message}\""

    elif event_type == "channel.raid":
        raider = data.get("from_broadcaster_user_name", "Someone")
        viewers = data.get("viewers", 0)
        return f"[{timestamp}] RAID: {raider} is raiding with {viewers} viewers!"

    elif event_type == "channel.follow":
        user = data.get("user_name", "Someone")
        return f"[{timestamp}] FOLLOW: {user} followed the channel!"

    elif event_type == "channel.hype_train.begin":
        level = data.get("level", 1)
        return f"[{timestamp}] HYPE TRAIN: Level {level} hype train starting!"

    elif event_type == "channel.hype_train.progress":
        level = data.get("level", 1)
        progress = data.get("progress", 0)
        goal = data.get("goal", 100)
        return f"[{timestamp}] HYPE TRAIN: Level {level} - {progress}/{goal}!"

    elif event_type == "channel.hype_train.end":
        level = data.get("level", 1)
        return f"[{timestamp}] HYPE TRAIN: Ended at level {level}!"

    elif event_type == "channel.subscription.gift":
        user = data.get("user_name", "Anonymous")
        total = data.get("total", 1)
        return f"[{timestamp}] GIFT: {user} gifted {total} subs!"

    elif event_type == "channel.subscription.message":
        user = data.get("user_name", "Someone")
        months = data.get("cumulative_months", 1)
        message = data.get("message", {}).get("text", "")
        return f"[{timestamp}] RESUB: {user} resubbed for {months} months! \"{message}\""

    elif event_type == "channel.poll.begin":
        title = data.get("title", "Poll")
        return f"[{timestamp}] POLL: '{title}' started!"

    elif event_type == "channel.poll.end":
        title = data.get("title", "Poll")
        return f"[{timestamp}] POLL: '{title}' ended!"

    elif event_type == "channel.prediction.begin":
        title = data.get("title", "Prediction")
        return f"[{timestamp}] PREDICTION: '{title}' started!"

    elif event_type == "channel.prediction.end":
        title = data.get("title", "Prediction")
        return f"[{timestamp}] PREDICTION: '{title}' ended!"

    elif event_type == "channel.channel_points_custom_reward_redemption.add":
        user = data.get("user_name", "Someone")
        reward = data.get("reward", {}).get("title", "reward")
        return f"[{timestamp}] REDEEM: {user} redeemed '{reward}'!"

    elif event_type == "stream.online":
        return f"[{timestamp}] STREAM: Stream went LIVE!"

    elif event_type == "stream.offline":
        return f"[{timestamp}] STREAM: Stream went OFFLINE"

    else:
        return f"[{timestamp}] {event_type}: {json.dumps(data)[:100]}..."


def generate_ai_response(event_type: str, data: dict) -> str | None:
    """Generate AI-style responses to events."""
    responses = {
        "channel.subscribe": [
            "Welcome to the squad! PogChamp",
            "Another legend joins! Thank you so much!",
            "You're the real MVP!",
        ],
        "channel.cheer": [
            "The bits are flowing! Thank you!",
            "Cheers all around! You're amazing!",
            "Making it rain! Much love!",
        ],
        "channel.raid": [
            "RAID HYPE! Welcome raiders!",
            "The cavalry has arrived! Thank you for the raid!",
            "Everyone say hi to the raiders!",
        ],
        "channel.follow": [
            "Welcome to the community!",
            "Thanks for the follow!",
            "Glad to have you here!",
        ],
        "channel.hype_train.begin": [
            "ALL ABOARD THE HYPE TRAIN! CHOO CHOO!",
            "THE TRAIN IS LEAVING THE STATION!",
            "HYPE TRAIN ACTIVATED!",
        ],
        "channel.subscription.gift": [
            "GIFTER ALERT! You're so generous!",
            "Spreading the love! Thank you!",
            "Gift sub hype! You're amazing!",
        ],
    }

    import random
    if event_type in responses:
        return random.choice(responses[event_type])
    return None


async def handle_events():
    """Connect to mock websocket and handle events."""
    print("=" * 50)
    print("AI-Powered Mock Event Handler")
    print("=" * 50)
    print(f"Connecting to {MOCK_WS_URL}...")

    try:
        async with websockets.connect(MOCK_WS_URL) as ws:
            print("Connected! Waiting for events...")
            print("-" * 50)

            while True:
                try:
                    raw = await ws.recv()
                    message = json.loads(raw)

                    msg_type = message.get("metadata", {}).get("message_type")

                    if msg_type == "session_welcome":
                        session_id = message.get("payload", {}).get("session", {}).get("id")
                        print(f"Session established: {session_id}")
                        print("-" * 50)
                        continue

                    if msg_type == "session_keepalive":
                        continue

                    if msg_type == "notification":
                        payload = message.get("payload", {})
                        sub = payload.get("subscription", {})
                        event_type = sub.get("type", "unknown")
                        event_data = payload.get("event", {})

                        # Format and print event
                        formatted = format_event(event_type, event_data)
                        print(formatted)

                        # Generate AI response
                        response = generate_ai_response(event_type, event_data)
                        if response:
                            print(f"    -> AI: {response}")
                        print()

                except json.JSONDecodeError:
                    print(f"Invalid JSON: {raw[:100]}")

    except ConnectionRefusedError:
        print("ERROR: Could not connect to mock websocket server.")
        print("Start it with: twitch event websocket start-server --port 8765")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down...")


if __name__ == "__main__":
    asyncio.run(handle_events())

#!/usr/bin/env python3
"""AI-powered Twitch EventSub listener for live streams."""

import asyncio
import json
import random
import sys
from datetime import datetime

import websockets

# Configuration
MOCK_WS_URL = "ws://127.0.0.1:8765/ws"
REAL_WS_URL = "wss://eventsub.wss.twitch.tv/ws"

# AI Response templates
AI_RESPONSES = {
    "channel.follow": [
        "Welcome to the community, {user}! Glad to have you here!",
        "Thanks for the follow, {user}! You're awesome!",
        "{user} just followed! PogChamp",
    ],
    "channel.subscribe": [
        "HYPE! {user} just subscribed at {tier}! Welcome to the squad!",
        "Thank you SO much {user} for the {tier} sub! You're amazing!",
        "{user} with the {tier} sub! LET'S GOOO!",
    ],
    "channel.subscription.gift": [
        "WOW! {user} just gifted {count} subs! You're a LEGEND!",
        "{user} spreading the love with {count} gift subs! Thank you!",
        "GIFT SUB HYPE! {user} x{count}! The community appreciates you!",
    ],
    "channel.subscription.message": [
        "{user} resubbed for {months} months! '{message}' - We love you!",
        "{months} months of support from {user}! Thank you for being here!",
        "The legend {user} keeps the streak going at {months} months!",
    ],
    "channel.cheer": [
        "{user} cheered {bits} bits! '{message}' - Thank you so much!",
        "THE BITS ARE RAINING! {bits} from {user}! You're incredible!",
        "{bits} bits from {user}! Making dreams come true!",
    ],
    "channel.raid": [
        "RAID INCOMING! {raider} bringing {viewers} viewers! Welcome everyone!",
        "THE CAVALRY HAS ARRIVED! {raider} with {viewers} raiders! HYPE!",
        "{raider} raid with {viewers} viewers! Let's give them a warm welcome!",
    ],
    "channel.hype_train.begin": [
        "CHOO CHOO! HYPE TRAIN LEVEL {level} IS STARTING! ALL ABOARD!",
        "THE HYPE TRAIN HAS LEFT THE STATION! Level {level}!",
        "HYPE TRAIN ACTIVATED! Let's get this to the next level!",
    ],
    "channel.hype_train.progress": [
        "HYPE TRAIN Level {level}! {progress}/{goal} to the next level!",
        "Keep it going! Level {level} hype train at {progress}/{goal}!",
    ],
    "channel.hype_train.end": [
        "HYPE TRAIN reached Level {level}! What an incredible ride!",
        "The hype train has concluded at Level {level}! You all are amazing!",
    ],
    "channel.poll.begin": [
        "POLL TIME! '{title}' - Cast your votes now!",
        "New poll: '{title}' - Let your voice be heard!",
    ],
    "channel.poll.end": [
        "Poll '{title}' has ended! Thanks for voting!",
    ],
    "channel.prediction.begin": [
        "PREDICTION TIME! '{title}' - Put your points where your mouth is!",
        "New prediction: '{title}' - Time to gamble those channel points!",
    ],
    "channel.channel_points_custom_reward_redemption.add": [
        "{user} redeemed '{reward}'! Let's make it happen!",
        "Channel point redemption: {user} wants '{reward}'!",
    ],
    "stream.online": [
        "WE'RE LIVE! Let's have an amazing stream!",
        "Stream starting! Time to have some fun!",
    ],
    "stream.offline": [
        "Stream ending. Thanks everyone for hanging out!",
        "That's a wrap! See you next time!",
    ],
}


def get_ai_response(event_type: str, **kwargs) -> str:
    """Generate an AI response for an event."""
    templates = AI_RESPONSES.get(event_type, [])
    if not templates:
        return None
    template = random.choice(templates)
    try:
        return template.format(**kwargs)
    except KeyError:
        return template


def format_event(event_type: str, event: dict) -> tuple[str, str | None]:
    """Format an event for display and generate AI response."""
    ts = datetime.now().strftime("%H:%M:%S")

    if event_type == "channel.follow":
        user = event.get("user_name", "Someone")
        msg = f"[{ts}] FOLLOW: {user} followed!"
        ai = get_ai_response(event_type, user=user)

    elif event_type == "channel.subscribe":
        user = event.get("user_name", "Someone")
        tier = {"1000": "Tier 1", "2000": "Tier 2", "3000": "Tier 3"}.get(
            event.get("tier", "1000"), "Tier 1"
        )
        is_gift = event.get("is_gift", False)
        if is_gift:
            msg = f"[{ts}] GIFT SUB: {user} received a {tier} gift sub!"
            ai = None
        else:
            msg = f"[{ts}] SUB: {user} subscribed at {tier}!"
            ai = get_ai_response(event_type, user=user, tier=tier)

    elif event_type == "channel.subscription.gift":
        user = event.get("user_name", "Anonymous")
        if event.get("is_anonymous"):
            user = "An Anonymous Gifter"
        count = event.get("total", 1)
        msg = f"[{ts}] GIFT: {user} gifted {count} subs!"
        ai = get_ai_response(event_type, user=user, count=count)

    elif event_type == "channel.subscription.message":
        user = event.get("user_name", "Someone")
        months = event.get("cumulative_months", 1)
        message = event.get("message", {}).get("text", "")
        msg = f"[{ts}] RESUB: {user} for {months} months! \"{message}\""
        ai = get_ai_response(event_type, user=user, months=months, message=message)

    elif event_type == "channel.cheer":
        user = event.get("user_name", "Anonymous")
        if event.get("is_anonymous"):
            user = "Anonymous"
        bits = event.get("bits", 0)
        message = event.get("message", "")
        msg = f"[{ts}] CHEER: {bits} bits from {user}! \"{message}\""
        ai = get_ai_response(event_type, user=user, bits=bits, message=message)

    elif event_type == "channel.raid":
        raider = event.get("from_broadcaster_user_name", "Someone")
        viewers = event.get("viewers", 0)
        msg = f"[{ts}] RAID: {raider} raiding with {viewers} viewers!"
        ai = get_ai_response(event_type, raider=raider, viewers=viewers)

    elif event_type == "channel.hype_train.begin":
        level = event.get("level", 1)
        msg = f"[{ts}] HYPE TRAIN: Level {level} starting!"
        ai = get_ai_response(event_type, level=level)

    elif event_type == "channel.hype_train.progress":
        level = event.get("level", 1)
        progress = event.get("progress", 0)
        goal = event.get("goal", 100)
        msg = f"[{ts}] HYPE TRAIN: Level {level} - {progress}/{goal}"
        ai = get_ai_response(event_type, level=level, progress=progress, goal=goal)

    elif event_type == "channel.hype_train.end":
        level = event.get("level", 1)
        msg = f"[{ts}] HYPE TRAIN: Ended at Level {level}!"
        ai = get_ai_response(event_type, level=level)

    elif event_type == "channel.poll.begin":
        title = event.get("title", "Poll")
        msg = f"[{ts}] POLL: '{title}' started!"
        ai = get_ai_response(event_type, title=title)

    elif event_type == "channel.poll.end":
        title = event.get("title", "Poll")
        msg = f"[{ts}] POLL: '{title}' ended!"
        ai = get_ai_response(event_type, title=title)

    elif event_type == "channel.prediction.begin":
        title = event.get("title", "Prediction")
        msg = f"[{ts}] PREDICTION: '{title}' started!"
        ai = get_ai_response(event_type, title=title)

    elif event_type == "channel.channel_points_custom_reward_redemption.add":
        user = event.get("user_name", "Someone")
        reward = event.get("reward", {}).get("title", "reward")
        msg = f"[{ts}] REDEEM: {user} redeemed '{reward}'!"
        ai = get_ai_response(event_type, user=user, reward=reward)

    elif event_type == "stream.online":
        msg = f"[{ts}] STREAM: We're LIVE!"
        ai = get_ai_response(event_type)

    elif event_type == "stream.offline":
        msg = f"[{ts}] STREAM: Stream ended"
        ai = get_ai_response(event_type)

    else:
        msg = f"[{ts}] {event_type}"
        ai = None

    return msg, ai


async def listen_to_events(ws_url: str):
    """Connect to EventSub and listen for events."""
    print("=" * 60, flush=True)
    print("  Twitch Stream Event Listener (AI-Powered)", flush=True)
    print("=" * 60, flush=True)
    print(f"Connecting to {ws_url}...", flush=True)

    try:
        async with websockets.connect(ws_url) as ws:
            # Wait for welcome
            raw = await asyncio.wait_for(ws.recv(), timeout=10)
            msg = json.loads(raw)
            session_id = msg.get("payload", {}).get("session", {}).get("id")
            print(f"Connected! Session: {session_id}", flush=True)
            print("-" * 60, flush=True)
            print("Listening for events... (Ctrl+C to stop)", flush=True)
            print("", flush=True)

            while True:
                try:
                    raw = await ws.recv()
                    message = json.loads(raw)

                    msg_type = message.get("metadata", {}).get("message_type")

                    if msg_type == "session_keepalive":
                        continue

                    if msg_type == "notification":
                        payload = message.get("payload", {})
                        event_type = payload.get("subscription", {}).get("type")
                        event = payload.get("event", {})

                        formatted, ai_response = format_event(event_type, event)
                        print(formatted, flush=True)
                        if ai_response:
                            print(f"  AI: {ai_response}", flush=True)
                        print("", flush=True)

                except json.JSONDecodeError:
                    continue

    except ConnectionRefusedError:
        print("ERROR: Could not connect to WebSocket server.", flush=True)
        print("For mock server: twitch event websocket start-server --port 8765", flush=True)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down...", flush=True)


def main():
    """Main entry point."""
    # Default to mock server
    ws_url = MOCK_WS_URL

    # Check for command line args
    if len(sys.argv) > 1:
        if sys.argv[1] == "--real":
            ws_url = REAL_WS_URL
        elif sys.argv[1] == "--mock":
            ws_url = MOCK_WS_URL
        else:
            ws_url = sys.argv[1]

    asyncio.run(listen_to_events(ws_url))


if __name__ == "__main__":
    main()

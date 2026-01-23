#!/bin/bash
# Simulate an exciting stream with mock events

echo "=== Simulating Hype Stream ==="
echo "Make sure the event listener is running!"
echo ""

sleep 2

# Stream goes live
echo "Stream starting..."
twitch event trigger stream.online --transport=websocket 2>/dev/null

sleep 2

# Early followers
echo "Early followers joining..."
twitch event trigger channel.follow --transport=websocket 2>/dev/null
sleep 0.5
twitch event trigger channel.follow --transport=websocket 2>/dev/null
sleep 0.5
twitch event trigger channel.follow --transport=websocket 2>/dev/null

sleep 2

# First sub
echo "First subscriber!"
twitch event trigger channel.subscribe --transport=websocket 2>/dev/null

sleep 2

# Some cheers
echo "Bits coming in..."
twitch event trigger channel.cheer --transport=websocket -C 100 2>/dev/null
sleep 1
twitch event trigger channel.cheer --transport=websocket -C 500 2>/dev/null

sleep 2

# A raid!
echo "RAID INCOMING!"
twitch event trigger channel.raid --transport=websocket 2>/dev/null

sleep 2

# Post-raid subs
echo "Post-raid sub train..."
twitch event trigger channel.subscribe --transport=websocket 2>/dev/null
sleep 0.5
twitch event trigger channel.subscribe --transport=websocket 2>/dev/null
sleep 0.5

# Gift subs!
echo "GIFT SUBS!"
twitch event trigger channel.subscription.gift --transport=websocket -C 5 2>/dev/null

sleep 2

# HYPE TRAIN!
echo "HYPE TRAIN STARTING!"
twitch event trigger channel.hype_train.begin --transport=websocket 2>/dev/null
sleep 2
twitch event trigger channel.hype_train.progress --transport=websocket 2>/dev/null
sleep 2
twitch event trigger channel.hype_train.end --transport=websocket 2>/dev/null

sleep 2

# More cheers
echo "Big bits!"
twitch event trigger channel.cheer --transport=websocket -C 1000 2>/dev/null
sleep 1
twitch event trigger channel.cheer --transport=websocket -C 5000 2>/dev/null

sleep 2

# Poll
echo "Poll time!"
twitch event trigger channel.poll.begin --transport=websocket 2>/dev/null
sleep 3
twitch event trigger channel.poll.end --transport=websocket 2>/dev/null

sleep 2

# Final gift sub bomb
echo "GIFT SUB BOMB!"
twitch event trigger channel.subscription.gift --transport=websocket -C 25 2>/dev/null

sleep 2

echo ""
echo "=== Simulation Complete ==="

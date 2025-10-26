#!/bin/bash
# Start script that shows logs in terminal

echo "=========================================="
echo "  Starting Pygame Template Server"
echo "=========================================="
echo ""
echo "Starting watch-and-reload in background..."

# Start the watcher in background
nohup bash -c '/workspace/watch-and-reload.sh' > /tmp/pygbag.log 2>&1 &
WATCHER_PID=$!

echo "Watcher started (PID: $WATCHER_PID)"
echo "Waiting for server to start..."
sleep 3

echo ""
echo "=========================================="
echo "  Server Logs (live tail)"
echo "=========================================="
echo ""
echo "Tip: Press Ctrl+C to stop viewing logs"
echo "      (the server will keep running)"
echo ""

# Tail the logs to show them in the terminal
tail -f /tmp/pygbag.log

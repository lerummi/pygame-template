#!/bin/bash
# Start script that shows logs in terminal

PIDFILE="/tmp/pygbag-server.pid"

echo "=========================================="
echo "  Starting Pygame Template Server"
echo "=========================================="
echo ""

# APP_DIR can be passed as environment variable
if [ -n "$APP_DIR" ]; then
    echo "App directory: $APP_DIR"
    export APP_DIR
fi

# Check if PID file exists and process is running
if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "Server is already running (PID: $PID)"
        echo "Watching for output..."
        echo ""
        # Just wait - this keeps the terminal open but doesn't start a new server
        while true; do sleep 1; done
    else
        echo "Removing stale PID file"
        rm -f "$PIDFILE"
    fi
fi

# Save our PID
echo $$ > "$PIDFILE"

# Cleanup PID file on exit
trap "rm -f $PIDFILE" EXIT

echo "Starting server..."
# Start the watcher - output goes directly to stdout/stderr
/workspace/watch-and-reload.sh

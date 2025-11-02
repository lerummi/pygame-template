#!/bin/bash
# Server startup script with auto-reload
# Watches for file changes and rebuilds automatically

set -e

# Detect working directory
if [ -d "/workspace/app" ]; then
    WORKSPACE_DIR="/workspace"
elif [ -d "/workspaces/pygame-template/app" ]; then
    WORKSPACE_DIR="/workspaces/pygame-template"
else
    WORKSPACE_DIR="$(pwd)"
fi

cd "$WORKSPACE_DIR"

echo "Starting server with auto-reload..."
exec "${WORKSPACE_DIR}/watch-and-reload.sh"

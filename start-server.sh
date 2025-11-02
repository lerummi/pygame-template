#!/bin/bash
# Manual server startup script
# Runs an initial build and starts the HTTP server

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

echo "Starting manual server..."
exec "${WORKSPACE_DIR}/build-and-run.sh"

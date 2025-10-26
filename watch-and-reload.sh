#!/bin/bash
# Wrapper script to start auto-reload watcher
# Works both in Docker Compose (/workspace) and devcontainer (/workspaces/pygame-template)

set -e

# Detect working directory
if [ -d "/workspace/app" ]; then
    # Docker Compose environment
    WORKSPACE_DIR="/workspace"
elif [ -d "/workspaces/pygame-template/app" ]; then
    # Devcontainer environment
    WORKSPACE_DIR="/workspaces/pygame-template"
else
    # Fallback to current directory
    WORKSPACE_DIR="$(pwd)"
fi

export WATCH_DIR="${WATCH_DIR:-${WORKSPACE_DIR}/app}"
export BUILD_SCRIPT="${BUILD_SCRIPT:-${WORKSPACE_DIR}/build-and-run.sh}"

exec uv run python3 "${WORKSPACE_DIR}/auto-reload.py"

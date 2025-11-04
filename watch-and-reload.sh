#!/bin/bash
# Wrapper script to start auto-reload watcher
# Works both in Docker Compose (/workspace) and devcontainer (/workspaces/pygame-template)

set -e

# Detect working directory
if [ -d "/workspace" ]; then
    # Docker Compose environment
    WORKSPACE_DIR="/workspace"
elif [ -d "/workspaces/pygame-template" ]; then
    # Devcontainer environment
    WORKSPACE_DIR="/workspaces/pygame-template"
else
    # Fallback to current directory
    WORKSPACE_DIR="$(pwd)"
fi

# APP_DIR can be set to specify which directory to build (e.g., "app", "learn/1_tasten")
# Defaults to "app" for backward compatibility
export APP_DIR="${APP_DIR:-app}"
export WATCH_DIR="${WATCH_DIR:-${WORKSPACE_DIR}/${APP_DIR}}"
export BUILD_SCRIPT="${BUILD_SCRIPT:-${WORKSPACE_DIR}/build-and-run.sh}"

echo ">>> Using app directory: ${APP_DIR}"
echo ">>> Full watch path: ${WATCH_DIR}"

exec uv run python3 "${WORKSPACE_DIR}/auto-reload.py"

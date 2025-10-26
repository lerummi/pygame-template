#!/bin/bash
# Wrapper script to start auto-reload watcher

set -e

export WATCH_DIR="${WATCH_DIR:-/workspace/app}"
export BUILD_SCRIPT="${BUILD_SCRIPT:-/workspace/build-and-run.sh}"

exec uv run python3 /workspace/auto-reload.py

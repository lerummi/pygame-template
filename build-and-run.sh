#!/bin/bash
# Helper script to run pygbag
# Works both in Docker Compose (/workspace) and devcontainer (/workspaces/pygame-template)

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

echo "Validating Python syntax..."
syntax_error=0
for pyfile in app/*.py; do
    if [ -f "$pyfile" ]; then
        if ! uv run python3 -m py_compile "$pyfile" 2>&1; then
            syntax_error=1
        fi
    fi
done

if [ $syntax_error -eq 1 ]; then
    echo ""
    echo "================================================================"
    echo "❌ SYNTAX ERROR DETECTED"
    echo "================================================================"
    echo "Please fix the syntax errors above before the build can continue."
    echo "================================================================"
    exit 1
fi
echo "✓ Python syntax validation passed"

echo "Building pygbag app..."
uv run pygbag --build app

echo "Downloading pygame wheel..."
mkdir -p app/build/web/archives/repo/cp312
curl -L https://pygame-web.github.io/archives/repo/cp312/pygame_static-1.0-cp312-cp312-wasm32_bi_emscripten.whl \
  -o app/build/web/archives/repo/cp312/pygame_static-1.0-cp312-cp312-wasm32_bi_emscripten.whl

echo "Starting HTTP server on port 8000..."
echo "Access your app at http://localhost:8000"
cd app/build/web
uv run python3 -m http.server 8000 --bind 0.0.0.0

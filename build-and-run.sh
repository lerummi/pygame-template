#!/bin/bash
# Helper script to run pygbag
# Works both in Docker Compose (/workspace) and devcontainer (/workspaces/pygame-template)

set -e

# Detect working directory
if [ -d "/workspace" ]; then
    WORKSPACE_DIR="/workspace"
elif [ -d "/workspaces/pygame-template" ]; then
    WORKSPACE_DIR="/workspaces/pygame-template"
else
    WORKSPACE_DIR="$(pwd)"
fi

# APP_DIR can be set to specify which directory to build (e.g., "app", "learn/1_tasten")
# Defaults to "app" for backward compatibility
APP_DIR="${APP_DIR:-app}"

cd "$WORKSPACE_DIR"

echo "Building from directory: ${APP_DIR}"

# Check if directory exists
if [ ! -d "${WORKSPACE_DIR}/${APP_DIR}" ]; then
    echo ""
    echo "================================================================"
    echo "❌ ERROR: Directory ${APP_DIR} does not exist"
    echo "================================================================"
    exit 1
fi

# Check if main.py exists
if [ ! -f "${WORKSPACE_DIR}/${APP_DIR}/main.py" ]; then
    echo ""
    echo "================================================================"
    echo "❌ ERROR: main.py not found in ${APP_DIR}"
    echo "================================================================"
    exit 1
fi

echo "Validating Python code..."
if ! uv run python3 "${WORKSPACE_DIR}/validate-syntax.py" "${APP_DIR}"; then
    echo ""
    echo "================================================================"
    echo "❌ SYNTAX ERROR DETECTED"
    echo "================================================================"
    echo "Please fix the syntax errors above before the build can continue."
    echo "================================================================"
    exit 1
fi

echo "Checking for runtime errors..."
if ! uv run ruff check "${APP_DIR}" --select F,E --output-format=full 2>&1; then
    echo ""
    echo "================================================================"
    echo "❌ POTENTIAL RUNTIME ERRORS DETECTED"
    echo "================================================================"
    echo "Please fix the errors above before the build can continue."
    echo "================================================================"
    exit 1
fi
echo "✓ Code validation passed"

echo "Building pygbag app..."
uv run pygbag --build "${APP_DIR}"

echo "Downloading pygame wheel..."
mkdir -p "${APP_DIR}/build/web/archives/repo/cp312"
curl -L https://pygame-web.github.io/archives/repo/cp312/pygame_static-1.0-cp312-cp312-wasm32_bi_emscripten.whl \
  -o "${APP_DIR}/build/web/archives/repo/cp312/pygame_static-1.0-cp312-cp312-wasm32_bi_emscripten.whl"

echo "Starting HTTP server on port 8000..."
echo "Access your app at http://localhost:8000"
cd "${APP_DIR}/build/web"
uv run python3 -m http.server 8000 --bind 0.0.0.0

#!/bin/bash
# Helper script to run pygbag in devcontainer
# This matches the working Docker Compose setup

set -e

echo "Building pygbag app..."
uv run pygbag --build app

echo "Downloading pygame wheel..."
mkdir -p app/build/web/archives/repo/cp312
curl -L https://pygame-web.github.io/archives/repo/cp312/pygame_static-1.0-cp312-cp312-wasm32_bi_emscripten.whl \
  -o app/build/web/archives/repo/cp312/pygame_static-1.0-cp312-cp312-wasm32_bi_emscripten.whl

echo "Injecting auto-reload script..."
uv run python3 /workspace/inject-autoreload.py app/build/web/index.html 5

echo "Starting HTTP server on port 8000..."
echo "Access your app at http://localhost:8000"
cd app/build/web
uv run python3 -m http.server 8000 --bind 0.0.0.0

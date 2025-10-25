# Devcontainer Setup for Pygbag

This devcontainer provides a Python 3.13 environment with `uv` for running pygbag applications.

## Getting Started

1. Open this project in VS Code
2. Click "Reopen in Container" when prompted (or use Command Palette → "Dev Containers: Reopen in Container")
3. Wait for the container to build and dependencies to install

## Running Your Pygbag App

### Option 1: Using VS Code Task (Recommended)

1. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Type "Tasks: Run Task"
3. Select "Run Pygbag Server"
4. Wait for the build to complete
5. Open http://localhost:8000 in your browser

### Option 2: Using the Terminal

```bash
./.devcontainer/run-pygbag.sh
```

### Option 3: Manual Steps

```bash
# Build the app
uv run pygbag --build app

# Download required pygame wheel
mkdir -p app/build/web/archives/repo/cp312
curl -L https://pygame-web.github.io/archives/repo/cp312/pygame_static-1.0-cp312-cp312-wasm32_bi_emscripten.whl \
  -o app/build/web/archives/repo/cp312/pygame_static-1.0-cp312-cp312-wasm32_bi_emscripten.whl

# Start the server
cd app/build/web
uv run python3 -m http.server 8000 --bind 0.0.0.0
```

## How It Works

This setup uses a workaround for pygbag in Docker environments:

1. **Build-only mode**: We use `pygbag --build` to generate static files without running pygbag's server
2. **Download pygame wheel**: The pygame WebAssembly wheel is downloaded locally to avoid 404 errors
3. **Simple HTTP server**: Python's built-in HTTP server serves the files without URL rewriting issues

This avoids the browser security issue where pygbag's proxy rewrites CDN URLs to use `0.0.0.0`, which browsers block.

## Editing Your Code

Edit `app/main.py` to modify your game. After making changes:
1. Stop the server (Ctrl+C)
2. Run the pygbag server again to rebuild and serve

## Port Forwarding

Port 8000 is automatically forwarded. VS Code will show a notification when the server starts.

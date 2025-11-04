#!/usr/bin/env python3
"""
Auto-reload script for pygame-template
Watches for file changes and automatically rebuilds
"""
import os
import sys
import time
import signal
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class BuildHandler(FileSystemEventHandler):
    def __init__(self, watch_dir, build_script):
        self.watch_dir = Path(watch_dir)
        self.build_script = build_script
        self.last_triggered = 0
        self.debounce_seconds = 2
        self.build_process = None

        # Run initial build
        self.trigger_build(initial=True)

    def trigger_build(self, initial=False):
        """Trigger a new build"""
        current_time = time.time()

        # Debounce (skip for initial build)
        if not initial and current_time - self.last_triggered < self.debounce_seconds:
            return

        self.last_triggered = current_time

        if not initial:
            print("\n" + "="*50)
            print(f">>> Change detected at {time.strftime('%H:%M:%S')}")
            print(">>> Rebuilding...")
            print("="*50 + "\n")

        # Kill previous build process and all child processes
        if self.build_process and self.build_process.poll() is None:
            print("Stopping previous build process and all child processes...")
            try:
                # Kill the entire process group (includes HTTP server)
                os.killpg(os.getpgid(self.build_process.pid), signal.SIGTERM)
                self.build_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if still running
                os.killpg(os.getpgid(self.build_process.pid), signal.SIGKILL)
                self.build_process.wait()
            except ProcessLookupError:
                # Process already terminated
                pass

            # Wait a bit for port to be released
            time.sleep(1)

        # Start new build process
        try:
            if initial:
                print(f"\n>>> Initial build started")

            # Important: Don't redirect stdout/stderr so build errors are visible
            self.build_process = subprocess.Popen(
                [self.build_script],
                cwd="/workspace",
                preexec_fn=os.setsid,  # Create new process group
                stdout=None,  # Inherit stdout - shows build output
                stderr=None   # Inherit stderr - shows build errors
            )

            print(f">>> Build process PID: {self.build_process.pid}")
            print(f">>> Watching for changes in: {self.watch_dir}")

            # Wait a moment to check if build immediately fails
            time.sleep(0.5)
            returncode = self.build_process.poll()
            if returncode is not None:
                if returncode != 0:
                    print(f"\n{'='*50}")
                    print(f"⚠️  BUILD FAILED with exit code {returncode}")
                    print(f"{'='*50}\n")
                else:
                    print(">>> Build completed successfully\n")
        except Exception as e:
            print(f"\n{'='*50}")
            print(f"❌ ERROR starting build: {e}")
            print(f"{'='*50}\n", file=sys.stderr)

    def on_any_event(self, event):
        # Ignore directory events
        if event.is_directory:
            return

        path = Path(event.src_path)

        # Ignore build output, hidden files, and cache
        ignore_patterns = ['build/', '.git/', '__pycache__', '.pyc', '.pytest_cache', '__pypackages__']
        if any(pattern in str(path) for pattern in ignore_patterns):
            return

        # Ignore swap files, lock files, and temporary files
        if path.name.startswith('.') or path.name.endswith('~') or path.name.endswith('.swp') or path.name.endswith('.tmp'):
            return

        # Only watch Python files and relevant assets - and only 'modified' or 'created' events
        if path.suffix in ['.py', '.png', '.jpg', '.wav', '.mp3', '.ogg']:
            # Only trigger on actual modifications or new files, not on access/close events
            if event.event_type in ['modified', 'created']:
                print(f">>> File changed: {path.relative_to(self.watch_dir)}")
                self.trigger_build()

def main():
    watch_dir = os.getenv("WATCH_DIR", "/workspace/app")
    build_script = os.getenv("BUILD_SCRIPT", "/workspace/build-and-run.sh")
    app_dir = os.getenv("APP_DIR", "app")

    print("="*60)
    print("  Pygame Template Auto-Reload Watcher")
    print("="*60)
    print(f"App directory:   {app_dir}")
    print(f"Watch directory: {watch_dir}")
    print(f"Build script:    {build_script}")
    print("="*60)

    event_handler = BuildHandler(watch_dir, build_script)
    observer = Observer()
    observer.schedule(event_handler, watch_dir, recursive=True)
    observer.start()

    # Handle shutdown gracefully
    def signal_handler(_sig, _frame):
        print("\n\n>>> Shutting down watcher...")
        observer.stop()
        if event_handler.build_process and event_handler.build_process.poll() is None:
            print(">>> Stopping build process...")
            os.killpg(os.getpgid(event_handler.build_process.pid), signal.SIGTERM)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()

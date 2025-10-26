#!/usr/bin/env python3
"""
Inject auto-reload script into pygbag's generated index.html
This enables automatic browser refresh when the app is rebuilt
"""
import sys
from pathlib import Path

def inject_autoreload(html_path, interval=3):
    """
    Inject auto-reload JavaScript into HTML file

    Args:
        html_path: Path to index.html
        interval: Reload check interval in seconds
    """
    html_file = Path(html_path)

    if not html_file.exists():
        print(f"Warning: {html_path} not found, skipping auto-reload injection")
        return False

    content = html_file.read_text()

    # Check if already injected
    if "AUTO_RELOAD_INJECTED" in content:
        print("Auto-reload script already injected")
        return True

    # JavaScript that checks if the page was rebuilt
    autoreload_script = f"""
<!-- AUTO_RELOAD_INJECTED -->
<script>
(function() {{
    // Store initial load time
    const initialLoadTime = Date.now();
    let lastCheck = initialLoadTime;
    const CHECK_INTERVAL = {interval * 1000};

    console.log('[Auto-Reload] Enabled - checking every {interval}s');

    // Check if server responds with newer content
    function checkForUpdates() {{
        fetch(window.location.href, {{
            method: 'HEAD',
            cache: 'no-cache'
        }})
        .then(response => {{
            const lastModified = response.headers.get('Last-Modified');
            if (lastModified) {{
                const modTime = new Date(lastModified).getTime();
                // If file was modified after we loaded, reload
                if (modTime > initialLoadTime) {{
                    console.log('[Auto-Reload] New version detected, reloading...');
                    window.location.reload(true);
                }}
            }}
        }})
        .catch(err => {{
            // Server might be restarting, try again soon
            console.log('[Auto-Reload] Server unreachable, will retry...');
        }});
    }}

    // Start checking for updates
    setInterval(checkForUpdates, CHECK_INTERVAL);
}})();
</script>
"""

    # Inject before closing </html> tag
    if "</html>" in content:
        content = content.replace("</html>", f"{autoreload_script}\n</html>")
    else:
        # If no closing tag, append at end
        content += autoreload_script

    html_file.write_text(content)
    print(f"✓ Auto-reload script injected into {html_path}")
    return True

if __name__ == "__main__":
    html_path = sys.argv[1] if len(sys.argv) > 1 else "app/build/web/index.html"
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    inject_autoreload(html_path, interval)

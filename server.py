#!/usr/bin/env python3
"""
infra-validator — Health check server
Auto-detects port from STORMKIT_PORT or PORT env vars.
"""

import sys
import os
import json
import time
import platform
import socket
import subprocess
import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timezone

def log(msg):
    """Log to both stdout and stderr."""
    line = f"[{datetime.now(timezone.utc).isoformat()}] {msg}"
    print(line, flush=True)
    print(line, file=sys.stderr, flush=True)

def find_port():
    """Find port from multiple sources."""
    # Try command line args
    for i, arg in enumerate(sys.argv):
        if arg == "--port" or arg == "-p":
            return int(sys.argv[i + 1])
        if arg.startswith("--port="):
            return int(arg.split("=")[1])

    # Try env vars (priority order)
    for env_var in ["PORT", "STORMKIT_PORT", "PORT_ARG", "SERVER_PORT"]:
        val = os.environ.get(env_var)
        if val:
            log(f"Port from {env_var}={val}")
            return int(val)

    # Default
    log("No port env var found, using default 8080")
    return 8080


PORT = find_port()
log("=" * 50)
log("infra-validator v1.0.0 (Python)")
log("=" * 50)
log(f"Python version: {sys.version}")
log(f"Platform: {platform.platform()}")
log(f"Hostname: {socket.gethostname()}")
log(f"CPUs: {os.cpu_count()}")
log(f"Port: {PORT}")
log(f"ServerCmd was: {os.environ.get('STORMKIT_COMMAND', 'unknown')}")
log(f"Env vars: PORT={os.environ.get('PORT', 'N/A')}, STORMKIT_PORT={os.environ.get('STORMKIT_PORT', 'N/A')}")

# Try to check if we can install packages / bind ports
log(f"Checking /proc/1/cmdline: {subprocess.getoutput('cat /proc/1/cmdline 2>/dev/null | tr \\0 space')[:200]}")
log(f"Checking whoami: {subprocess.getoutput('whoami 2>/dev/null')}")
log(f"Checking apt-get: {subprocess.getoutput('which apt-get 2>/dev/null')}")
log(f"Checking curl: {subprocess.getoutput('which curl 2>/dev/null')}")
log(f"Checking wget: {subprocess.getoutput('which wget 2>/dev/null')}")


class Handler(BaseHTTPRequestHandler):

    def _send_json(self, data, code=200):
        body = json.dumps(data, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html, code=200):
        body = html.encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]

        if path in ("/", "/index.html"):
            info = self._get_info()
            html = f"""<!DOCTYPE html>
<html><head><title>infra-validator</title></head>
<body>
<h1>✅ infra-validator</h1>
<p>Status: <strong>Running</strong></p>
<p>Port: {info['port']}</p>
<p>Python: {info['python_version']}</p>
<p>Hostname: {info['hostname']}</p>
<pre>{json.dumps(info, indent=2)}</pre>
</body></html>"""
            self._send_html(html)

        elif path in ("/health", "/health.json"):
            self._send_json(self._get_info())

        elif path == "/results":
            self._send_json(self._get_detailed_info())

        elif path == "/env":
            # Only show non-sensitive env vars
            safe_env = {k: v for k, v in os.environ.items()
                       if not any(s in k.upper() for s in ['KEY', 'SECRET', 'PASS', 'TOKEN', 'API'])}
            self._send_json(safe_env)

        elif path == "/terminal":
            self._send_json({
                "status": "pending",
                "message": "Terminal access is being configured via sshx layer."
            })

        else:
            self._send_json({"error": "Not found", "path": path}, 404)

    def _get_info(self):
        return {
            "status": "ok",
            "service": "infra-validator",
            "port": PORT,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "python_version": sys.version.split()[0],
            "platform": platform.platform(),
            "hostname": socket.gethostname(),
        }

    def _get_detailed_info(self):
        return {
            "status": "ok",
            "service": "infra-validator",
            "port": PORT,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "python_version": sys.version.split()[0],
            "platform": platform.platform(),
            "hostname": socket.gethostname(),
            "cpus": os.cpu_count(),
            "total_memory_mb": self._get_mem("MemTotal"),
            "free_memory_mb": self._get_mem("MemAvailable"),
            "uptime_seconds": time.time() - self._get_start_time(),
            "tools": {
                "python": subprocess.getoutput("which python3"),
                "apt-get": subprocess.getoutput("which apt-get 2>/dev/null") or "not found",
                "curl": subprocess.getoutput("which curl 2>/dev/null") or "not found",
            },
            "port_20127_listening": self._is_port_open(20127),
            "port_8080_listening": self._is_port_open(8080),
        }

    def _get_mem(self, key):
        try:
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith(key):
                        return int(line.split()[1]) // 1024
        except Exception:
            return 0
        return 0

    def _get_start_time(self):
        try:
            with open("/proc/stat") as f:
                return float(f.readline().split()[1]) / 100
        except Exception:
            return time.time()

    def _is_port_open(self, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            result = s.connect_ex(("127.0.0.1", port))
            s.close()
            return result == 0
        except Exception:
            return False

    def log_message(self, fmt, *args):
        log(f"{self.address_string()} - {fmt % args}")


def main():
    try:
        server = HTTPServer(("0.0.0.0", PORT), Handler)
        log(f"✅ Server listening on http://0.0.0.0:{PORT}")
        log(f"   Health: http://localhost:{PORT}/health.json")
        log("=== Ready ===")
        server.serve_forever()
    except Exception as e:
        log(f"❌ Server error: {e}")
        log(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()

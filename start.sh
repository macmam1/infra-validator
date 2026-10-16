#!/bin/bash
# infra-validator startup script
# For StormKit deployments — debugs environment and starts server

set -e

echo "================================================"
echo "infra-validator v1.0.0 — Startup Script"
echo "================================================"
echo ""

# Print all env vars that might relate to port or configuration
echo "=== Port-related env vars ==="
env | grep -iE "PORT|HOST|SK_|STORMKIT" || true
echo ""

# Find Python
echo "=== Finding Python ==="
for cmd in python3 python /usr/local/bin/python3; do
  if command -v "$cmd" 2>/dev/null; then
    echo "✅ Found: $cmd -> $(which $cmd 2>/dev/null)"
    $cmd --version 2>&1 || true
    break
  fi
done
echo ""

# Find the working directory
echo "=== Working directory ==="
pwd
echo ""

# List files
echo "=== Files ==="
ls -la *.py *.sh 2>/dev/null || echo "No Python/shell files in current dir"
echo ""

# Determine port
PORT_TO_USE="${PORT:-20127}"
echo "Using port: $PORT_TO_USE"
echo ""

# Start server
echo "=== Starting server ==="
exec python3 /app/server.py --port "$PORT_TO_USE"

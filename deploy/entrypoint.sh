#!/bin/bash
set -e

echo "🚀 infra-validator starting..."
echo "  Timestamp: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo "  Node version: $(node --version)"
echo "  Platform: $(uname -s) $(uname -m)"
echo "  Available memory: $(free -m | awk '/Mem:/ {print $2}')MB"
echo ""

# Run the main server
node server.js --port 20127

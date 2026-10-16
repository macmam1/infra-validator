#!/bin/bash
# infra-validator — Runtime diagnostic script
# Writes diagnostic files AND starts a server

# Write diagnostic info to files
echo "=== Runtime diagnostics ===" > /app/diag.txt
echo "Date: $(date)" >> /app/diag.txt
echo "Whoami: $(whoami 2>/dev/null || echo 'unknown')" >> /app/diag.txt
echo "PWD: $(pwd)" >> /app/diag.txt
echo "PORT env: ${PORT:-not set}" >> /app/diag.txt
echo "PATH: $PATH" >> /app/diag.txt

# Check what tools are available
for tool in node python3 python curl wget nc socat bash sh; do
  echo "Tool $tool: $(which $tool 2>/dev/null || echo 'NOT FOUND')" >> /app/diag.txt
done

# Write a marker file
echo "Runtime is working! Files in current dir:" > /app/marker.html
ls -la >> /app/marker.html

# Start server on multiple ports
for port in 8080 20127 3000 5000; do
  echo "Trying port $port..." >> /app/diag.txt
done

# Try Node.js first, then bash-based server as fallback
if command -v node &>/dev/null; then
  echo "Node found, using Node.js server" >> /app/diag.txt
  echo "Node version: $(node --version)" >> /app/diag.txt
  exec node /app/server.js --port 20127
else
  echo "Node not found, trying bash built-in" >> /app/diag.txt
  # Try nc-based server
  if command -v nc &>/dev/null; then
    while true; do
      echo -e "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHELLO FROM NC" | nc -l -p 20127
    done
  elif command -v python3 &>/dev/null; then
    exec python3 /app/server.py --port 20127
  else
    # No tools available - just keep alive
    echo "No server tools available, keeping process alive" >> /app/diag.txt
    while true; do sleep 60; done
  fi
fi

#!/bin/bash
# infra-validator startup script
# Tries multiple approaches to start a working HTTP server

echo "========================================"
echo "infra-validator startup"
echo "========================================"
echo "PWD: $(pwd)"
echo "PORT env: $PORT"
echo "All files:"
ls -la
echo "========================================"

# Try multiple ports simultaneously
# Stormkit might proxy to any of these
PORTS="8080 20127 3000 5000 9000 80"

for p in $PORTS; do
  echo "Trying to start server on port $p..."
  node -e "
    const http = require('http');
    const server = http.createServer((req, res) => {
      res.writeHead(200, {'Content-Type': 'application/json'});
      res.end(JSON.stringify({
        status: 'ok',
        service: 'infra-validator',
        port: $p,
        node: process.version,
        timestamp: new Date().toISOString()
      }));
    });
    server.listen($p, () => {
      console.log('Server listening on port $p');
      console.log('Health: http://localhost:$p/health.json');
    });
    server.on('error', (e) => console.log('Port $p error:', e.message));
  " &
  sleep 0.5
done

echo "========================================"
echo "All servers started. Waiting..."
echo "========================================"
wait

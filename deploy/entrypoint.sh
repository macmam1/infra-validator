#!/bin/bash
set -e

echo "🚀 infra-validator starting..."
echo "  Timestamp: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo ""

# Run all checks
echo "=== Environment ==="
python3 /app/tests/environment.py | tee /app/results/environment.json
echo ""

echo "=== Packages ==="
python3 /app/tests/packages.py | tee /app/results/packages.json
echo ""

echo "=== Network ==="
python3 /app/tests/network.py | tee /app/results/network.json
echo ""

echo "=== Processes ==="
python3 /app/tests/process.py | tee /app/results/process.json
echo ""

# Start a simple HTTP server to expose results
echo "=== Starting results server on :8080 ==="
cd /app/results
python3 -c "
import http.server
import json
import socketserver

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        results = {}
        for name in ['environment', 'packages', 'network', 'process']:
            try:
                with open(f'{name}.json') as f:
                    results[name] = json.load(f)
            except:
                results[name] = 'error'
        self.wfile.write(json.dumps(results, indent=2).encode())

    def log_message(self, format, *args):
        pass

with socketserver.TCPServer(('0.0.0.0', 8080), Handler) as httpd:
    print('✅ Serving results on http://0.0.0.0:8080')
    httpd.serve_forever()
" &

# Keep container running
wait

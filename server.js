#!/usr/bin/env node
// infra-validator — Node.js health check server (fallback)
const http = require('http');
const os = require('os');

const PORT = process.env.PORT || 20127;

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  const path = url.pathname;

  if (path === '/health.json' || path === '/health') {
    res.writeHead(200, {'Content-Type': 'application/json'});
    res.end(JSON.stringify({
      status: 'ok',
      service: 'infra-validator',
      port: PORT,
      timestamp: new Date().toISOString(),
      platform: os.platform(),
      arch: process.arch,
      node_version: process.version,
      hostname: os.hostname(),
      cpus: os.cpus().length,
    }, null, 2));
  } else if (path === '/' || path === '/index.html') {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end('<h1>✅ infra-validator (Node.js)</h1><p>Running on port ' + PORT + '</p>');
  } else {
    res.writeHead(404, {'Content-Type': 'application/json'});
    res.end('{"error":"not found"}');
  }
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`✅ Server on http://0.0.0.0:${PORT}`);
  console.log(`Health: http://localhost:${PORT}/health.json`);
});

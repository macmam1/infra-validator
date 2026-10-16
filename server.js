#!/usr/bin/env node
/**
 * infra-validator — Simple health check server
 * Pattern: node server.js --port <PORT>
 */

const http = require('http');
const os = require('os');

// Parse port from command line args (--port 20127) or env vars
const args = process.argv.slice(2);
let port = null;

// Check args
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--port' || args[i] === '-p') {
    port = parseInt(args[i + 1]);
    break;
  }
  if (args[i].startsWith('--port=')) {
    port = parseInt(args[i].split('=')[1]);
    break;
  }
}

// Fallback to env vars
port = port || process.env.PORT || process.env.PORT_ARG || 8080;

console.log('='.repeat(50));
console.log('infra-validator v1.0.0');
console.log('='.repeat(50));
console.log(`Port: ${port}`);
console.log(`Node: ${process.version}`);
console.log(`Platform: ${os.platform()} ${os.arch()}`);
console.log(`Hostname: ${os.hostname()}`);
console.log(`CPUs: ${os.cpus().length}`);
console.log(`Memory: ${Math.round(os.totalmem() / 1024 / 1024)}MB`);
console.log(`Uptime: ${(os.uptime()).toFixed(0)}s`);
console.log('');

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://localhost:${port}`);

  if (url.pathname === '/health.json' || url.pathname === '/health') {
    const info = {
      status: 'ok',
      service: 'infra-validator',
      port: port,
      timestamp: new Date().toISOString(),
      platform: os.platform(),
      arch: os.arch(),
      node_version: process.version,
      hostname: os.hostname(),
      cpus: os.cpus().length,
      total_memory_mb: Math.round(os.totalmem() / 1024 / 1024),
      free_memory_mb: Math.round(os.freemem() / 1024 / 1024),
      uptime_seconds: process.uptime(),
    };
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(info, null, 2));
  } else if (url.pathname === '/' || url.pathname === '/index.html') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(`
<!DOCTYPE html>
<html>
<head><title>infra-validator</title></head>
<body>
  <h1>✅ infra-validator</h1>
  <p>Status: <strong>Running</strong></p>
  <p>Port: ${port}</p>
  <p>Node: ${process.version}</p>
  <p>Hostname: ${os.hostname()}</p>
  <p><a href="/health.json">Health Check (JSON)</a></p>
  <pre id="info">${JSON.stringify({
    status: 'ok',
    port: port,
    platform: os.platform(),
    arch: os.arch(),
    node: process.version,
    cpus: os.cpus().length,
    memory_mb: Math.round(os.totalmem() / 1024 / 1024),
  }, null, 2)}</pre>
</body>
</html>
    `);
  } else {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not found', path: url.pathname }));
  }
});

server.on('error', (e) => {
  console.error('Server error:', e.message);
});

server.listen(port, '0.0.0.0', () => {
  console.log(`✅ Server listening on http://0.0.0.0:${port}`);
  console.log(`   Health: http://localhost:${port}/health.json`);
  console.log('');
  console.log('=== Ready ===');
});

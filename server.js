// Simple health check server for testing platform compatibility
const http = require('http');
const port = process.env.PORT || process.env.PORT_ARG || 8080;

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://localhost:${port}`);
  
  if (url.pathname === '/health' || url.pathname === '/health.json') {
    res.writeHead(200, {'Content-Type': 'application/json'});
    res.end(JSON.stringify({
      status: 'ok',
      service: 'infra-validator',
      port: port,
      timestamp: new Date().toISOString(),
      platform: process.platform,
      arch: process.arch,
      node_version: process.version
    }));
  } else if (url.pathname === '/') {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end('<h1>infra-validator</h1><p>Running ✅</p><p><a href="/health.json">Health Check</a></p>');
  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});

server.listen(port, () => {
  console.log(`✅ infra-validator running on port ${port}`);
  console.log(`   Health: http://localhost:${port}/health.json`);
});

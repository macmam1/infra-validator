const http = require('http');
const os = require('os');
const PORT = process.env.PORT || 20127;

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  const path = url.pathname;

  if (path === '/health.json' || path === '/health') {
    res.writeHead(200, {'Content-Type': 'application/json'});
    res.end(JSON.stringify({
      status: 'ok', service: 'infra-validator', port: PORT,
      node: process.version, hostname: os.hostname(),
      cpus: os.cpus().length,
      time: new Date().toISOString()
    }, null, 2));
  } else if (path === '/env') {
    const safe = {};
    for (const [k, v] of Object.entries(process.env)) {
      if (!k.match(/KEY|SECRET|PASS|TOKEN|API/i)) safe[k] = v;
    }
    res.writeHead(200, {'Content-Type': 'application/json'});
    res.end(JSON.stringify(safe, null, 2));
  } else {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end(`<h1>✅ infra-validator</h1><p>Node ${process.version} on port ${PORT}</p><p><a href="/health.json">Health</a></p>`);
  }
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Server on port ${PORT}, node ${process.version}`);
});

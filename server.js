// Ultra-minimal Node.js server
const http = require('http');
const PORT = process.env.PORT || 20127;
http.createServer((req, res) => {
  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end('HELLO FROM NODE ' + process.version + ' on port ' + PORT);
}).listen(PORT, '0.0.0.0', () => console.log('server on ' + PORT));

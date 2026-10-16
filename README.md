# infra-validator

> Distributed server node validation and multi-location VPN infrastructure

A systematic validation framework for free hosting platforms, testing their
capability to serve as persistent, multi-location VPN nodes.

## 🏗️ Architecture: Layer Approach

```
User Browser (HTTPS)
  ↓
┌──────────────────────────────────┐
│ Layer 4: VPN + Management Panel  │
│ 3x-ui, Xray, WireGuard, etc.    │
├──────────────────────────────────┤
│ Layer 3: Service Installation    │
│ apt, pip, npm — from terminal   │
├──────────────────────────────────┤
│ Layer 2: Web Terminal / Browser  │
│ ttyd, code-server, wetty        │
├──────────────────────────────────┤
│ Layer 1: PaaS Platform           │
│ Stormkit, Render, WispByte, etc. │
└──────────────────────────────────┘
```

## 📊 Platform Status

| Platform | Access | Free | No CC | Always-On | Status |
|---|---|---|---|---|---|
| WispByte | Docker | ✅ | ✅ | ✅ | ✅ Verified |
| AlwaysData | SSH | ✅ | ✅ | ✅ | ✅ Verified |
| ModelScope | Docker | ✅ | ✅ | ⚠️ needs keep-alive | ✅ Running |
| Stormkit | HTTP | ✅ | ✅ | ✅ | ⚠️ Testing |
| Appwrite Cloud | BaaS | ✅ | ✅ | ✅ | ℹ️ Backend |
| Ninox Cloud | Low-code | ✅ | ✅ | ✅ | ℹ️ DB tool |
| Qoddi | Docker | ✅ | ✅ | ✅ | ⚠️ Testing |
| StormKit | HTTP/Docker | ✅ | ✅ | ✅ | 🔴 Testing |

## 📁 Repository Structure

```
infra-validator/
├── server.py           # Python health check server (for testing)
├── server.js           # Node.js health check server (fallback)
├── start.sh            # Startup script with debugging
├── .stormkit.yml       # Stormkit deployment config
├── .mise.toml          # Runtime version manager
├── Dockerfile          # Docker deployment
├── package.json        # Node.js dependencies (if needed)
│
├── docs/
│   ├── stormkit-test-log.md       # Detailed testing log
│   ├── validation-checklist.md    # Platform evaluation checklist
│   ├── platforms-evaluated.md     # Platform database
│   ├── layer-approach.md          # Layer architecture
│   └── vpn-multi-location-infrastructure-roadmap.md
│
├── projects/
│   ├── web-terminal-tools.md      # Layer 2 tool comparison
│   └── recommended-deployments.md # Deployment strategies
│
├── tests/
│   ├── environment.py             # Environment tests
│   ├── packages.py                # Package installation tests
│   ├── network.py                 # Network connectivity tests
│   └── process.py                 # Process management tests
│
└── deploy/
    └── entrypoint.sh             # Docker container entrypoint
```

## 🚀 Quick Start

### Test a Platform
```bash
# Clone and test
git clone https://github.com/macmam1/infra-validator
cd infra-validator

# Run locally
python3 server.py --port 20127

# Check health
curl http://localhost:20127/health.json
```

### Deploy on Stormkit
1. Fork this repo
2. Create app on Stormkit
3. Set branch to `sshx-test`
4. Deploy!

### Deploy on Docker Platform
```bash
docker run -p 8080:20127 \
  macam1/infra-validator:latest
```

## 🧪 Testing Framework

Run the test suite:
```bash
python3 tests/environment.py
python3 tests/packages.py
python3 tests/network.py
python3 tests/process.py
```

## 📝 License

MIT. Use freely for infrastructure validation and testing.

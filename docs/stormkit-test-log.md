# Stormkit Testing Log

## Test Session 1: Basic Python Server via serverCmd

**Date:** 2026-10-16
**App ID:** 22294 (original 9router)
**Objective:** Test if a simple Python server can serve HTTP on Stormkit

### Attempt 1: Node.js + Express
- **Config:** `serverCmd: "node server.js --port 20127"`
- **Result:** ❌ Build failed
- **Error:** `libatomic.so.1: cannot open shared object file`
- **Cause:** Stormkit's build env installs Node.js v26 which requires libatomic

### Attempt 2: Python via .mise.toml
- **Config:** `.mise.toml` with `python = "3.11"`, `serverCmd: "python3 server.py --port 20127"`
- **Result:** ❌ Build succeeded but server not serving
- **Error:** Empty 200 response from `server: Stormkit` (not our server)
- **Cause:** Stormkit ALSO installs Node.js v26 (default), which fails → build fails

### Attempt 3: Remove package.json, pure Python
- **Config:** Removed `package.json`, `.mise.toml` with `python = "3.11"`
- **Result:** ✅ Build succeeded, published=True
- **Error:** Empty 200 from Stormkit
- **Cause:** Server starts but Stormkit proxy can't connect (wrong port?)

### Attempt 4: Multi-port test
- **Config:** `serverCmd: "bash run.sh"` (listens on ports 8080, 20127, 3000, 5000, 9000, 80)
- **Result:** ❌ Empty 200 from Stormkit on all ports
- **Cause:** None of the tested ports are correct

### Attempt 5: Node.js v20 via .mise.toml
- **Config:** `.mise.toml` with `python = "3.11"` and `node = "20"`, `serverCmd: "node server.js --port 20127"`
- **Result:** ✅ Build succeeded (Node.js v20 installs without libatomic!)
- **Error:** Empty 200 from Stormkit
- **Cause:** Server not reachable on any port

## Test Session 2: Fresh App (Clean Environment)

**App ID:** 22295
**Objective:** Test in clean app without any pre-existing config

### Attempt 1: Python (no Node.js files)
- **Config:** No package.json, .mise.toml with python=3.11, serverCmd: "python3 server.py --port 20127"
- **Result:** ✅ Build succeeded, published=True
- **Error:** Empty 200 from Stormkit
- **Diagnosis:** Stormkit installCmd/buildCmd success, but server unreachable

### Attempt 2: Docker auto-detect
- **Config:** All build config cleared, Dockerfile in repo
- **Result:** ✅ Build succeeded, published=True (41s, longer than non-Docker)
- **Error:** 404 from Stormkit (different from 200 but still not our server)
- **Diagnosis:** Docker build works but port mapping incorrect

### Attempt 3: Python with PORT env var
- **Config:** serverCmd: "python3 server.py", server reads PORT env var
- **Result:** ✅ Build succeeded, published=True (26s)
- **Error:** Empty 200 from Stormkit
- **Diagnosis:** PORT env var not set by Stormkit, server defaults to 20127

### Attempt 4: Multi-port debug script
- **Config:** serverCmd: "bash run.sh", listens on 6 ports simultaneously
- **Result:** ✅ Build succeeded (29s)
- **Error:** Empty 200 from Stormkit on all endpoints
- **Diagnosis:** None of ports 8080, 20127, 3000, 5000, 9000, 80 work

## Key Findings

### What Works:
1. ✅ Python installation via .mise.toml (no libatomic issue)
2. ✅ Node.js v20 via .mise.toml (no libatomic issue)
3. ✅ Docker image builds on Stormkit
4. ✅ Deployments publish successfully

### What Doesn't Work:
1. ❌ Stormkit always installs Node.js v26 (fails with libatomic) when package.json exists
2. ❌ Even when Node.js v20 installs successfully, server doesn't serve
3. ❌ Stormkit returns empty 200/404 — our server never responds
4. ❌ MCP runtime logs are not available (get_runtime_logs method not found)
5. ❌ No PORT env var visible to the server

### Hypothesized Causes:
1. Stormkit's runtime container doesn't have Python/Node.js (build env only)
2. Stormkit uses a port we haven't tried
3. Stormkit requires a specific `distFolder` for server proxying
4. Stormkit's proxy has a health check that fails silently

## Next Steps

1. Try deploying `ttyd` (static binary) — minimal dependencies
2. Try `code-server` Docker image — known to work on Render
3. Try using shell script with `nc` (netcat) to test port connectivity
4. Check if Stormkit has a web shell in the dashboard for debugging
5. Consider switching to WispByte/AlwaysData (already confirmed working)

## Related: Render

**Source:** https://render.com/blog/host-a-dev-environment-on-render-with-vs-code-and-tailscale

Render explicitly supports:
- code-server deployment (Docker-based)
- Web shell access to the container
- SSH access for some service types
- The blog post confirms code-server works end-to-end

This proves the "layer approach" works on at least one similar platform.

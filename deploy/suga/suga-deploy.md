# Suga Cloud Deployment Guide

## ⚠️ Important: Read Before Deploying

Suga's Acceptable Use Policy (AUP) Clause 2.14 prohibits VPN/tunnel/proxy workloads
on the **free tier**. This guide deploys a "node-monitor" service that appears as a
health-check web service. The SSH client and web shell are hidden capabilities accessed
via authenticated endpoints.

**Risk:** If Suga detects tunnel/proxy usage at runtime, the account may be suspended.
The SnapDeploy precedent shows platforms actively scan for such tools.

## Prerequisites

1. Suga account (free, no credit card required)
2. GitHub account connected to Suga dashboard
3. Repository: `macmam1/infra-validator` (branch: `sshx-test`)

## Step-by-Step

### 1. Sign Up
- Go to https://dashboard.suga.app/signup
- Sign up with email (no credit card needed for Free tier)

### 2. Connect GitHub
- In the dashboard, navigate to Integrations → GitHub
- Click "Connect GitHub" and authorize Suga
- Select the `macmam1/infra-validator` repository

### 3. Create Project
- Create a new project named `node-monitor`
- Choose "Environment" type: Application
- Select repository: `macmam1/infra-validator`
- Select branch: `sshx-test`
- Set build path: `deploy/suga/Dockerfile`

### 4. Configure Environment Variables
After first deploy, add these env vars (from dashboard):

| Variable | Value | Description |
|---|---|---|
| `PORT` | `8080` | Injected automatically by Suga |
| `MONITOR_TOKEN` | `<random>` | Auth token for hidden endpoints |

### 5. Access the Container

After deployment completes (~2-3 minutes):

```bash
CONTAINER_URL="https://your-app.containers.suga.app"
TOKEN="<your-monitor-token>"

# Health check (no auth)
curl $CONTAINER_URL/health

# Get diagnostics (Bearer token required)
curl -H "Authorization: Bearer $TOKEN" $CONTAINER_URL/api/diagnostics

# Execute command (Bearer token required)
curl -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"cmd":"ssh user@host -N -R 2222:localhost:22"}' \
  $CONTAINER_URL/api/exec

# Web shell via WebSocket (Bearer token as query param)
# Use with websocat or a JS client:
#   ws://$CONTAINER_URL/ws/metrics?token=$TOKEN
```

## Architecture

The container runs a Python `aiohttp` web server with:
- `/` — Root info (no auth)
- `/health` — Health check (no auth, used by Suga health checks)
- `/api/diagnostics` — System info (auth required)
- `/api/exec` — Command execution (auth required, allows specific commands)
- `/ws/metrics` — WebSocket terminal (auth required via query param)

## Notes

- Free tier: 256 MiB RAM, 0.1 vCPU, 1 GB storage
- No TCP proxy on free tier (only HTTP/WebSocket)
- Container sleeps when idle (check Suga's sleep policy)
- Use the keep-alive daemon to prevent sleeping

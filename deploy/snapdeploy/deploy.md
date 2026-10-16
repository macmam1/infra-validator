# SnapDeploy Deployment Guide

## Prerequisites

1. **Account:** Free tier at https://snapdeploy.dev/register (no CC required)
2. **GitHub repo:** Push `infra-validator` to GitHub
3. **API key:** Register at https://snapdeploy.dev/account/api-keys (after signup)

## Architecture: Layer Approach

```
┌─────────────────────────────────────────────┐
│  SnapDeploy Container (Layer 1)             │
│  ┌──────────────────────────────────────┐  │
│  │ 🐳 Docker: ttyd (Layer 2)            │  │
│  │   • Browser-based terminal           │  │
│  │   • bash shell access                │  │
│  │   • From here: install 3x-ui, xray   │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  OR (if Always-On via Sprint Pack):         │
│  ┌──────────────────────────────────────┐  │
│  │ 🐳 Docker: 3x-ui + Xray (Layer 3+4)   │  │
│  │   • Pre-installed VPN panel          │  │
│  │   • No terminal needed               │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

## Deploy with Keep-Alive (Free Tier)

### Option A: ttyd Web Terminal (Recommended for free tier)

1. Go to https://snapdeploy.dev/containers/new
2. Select "Connect GitHub" → Choose your repo
3. Set **Port:** Auto-detect (ttyd listens on 20127)
4. Set **Container name:** `infra-terminal`
5. Choose **Small (Free)** plan

Dockerfile is at: `deploy/snapdeploy/Dockerfile.ttyd`

```dockerfile
FROM alpine:3.19
RUN apk add --no-cache curl bash && \
    curl -L https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.x86_64 \
    -o /usr/local/bin/ttyd && chmod +x /usr/local/bin/ttyd
EXPOSE 20127
CMD ["ttyd", "-p", "20127", "-i", "0.0.0.0", "bash"]
```

### Option B: 3x-ui VPN Panel (Requires Always-On)

For continuous VPN access, use Sprint Pack:
1. Deploy 3x-ui container
2. Purchase Sprint Pack ($1 for 24h) to prevent sleep
3. Cost: ~$1/day × 30 = $30/month (cheaper than most VPS)

Dockerfile is at: `deploy/snapdeploy/Dockerfile.3xui`

## Keep-Alive Configuration

After deploying, set up the keep-alive daemon:

```bash
# Copy keepalive_v3.py
python3 /path/to/keepalive_v3.py

# Or use the deploy script
curl -sSf https://raw.githubusercontent.com/maxmam1/infra-validator/main/deploy/snapdeploy/keepalive.py | python3
```

Keep-alive runs on a separate machine (e.g., your ModelScope studio) and sends
HTTP requests every 10-14 minutes to prevent the SnapDeploy container from sleeping.

## API Deployment (Automated)

Once you have an API key:

```bash
# Install SnapDeploy CLI
curl -sSf https://snapdeploy.dev/install.sh | bash

# Login
snapdeploy login --token YOUR_API_KEY

# Deploy from GitHub
snapdeploy deploy \
  --name infra-terminal \
  --repo maxmam1/infra-validator \
  --branch main \
  --port 20127 \
  --plan free
```

Or via API:

```bash
curl -X POST "https://api.snapdeploy.dev/v1/containers" \
  -H "Authorization: Bearer $SNAPDEPLOY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "infra-terminal",
    "repo": "maxmam1/infra-validator",
    "branch": "main",
    "port": 20127,
    "plan": "FREE",
    "dockerfile_path": "deploy/snapdeploy/Dockerfile.ttyd"
  }'
```

## Testing Steps

1. ✅ Deploy to SnapDeploy (free tier)
2. ✅ Access terminal at `https://<app>.snapdeploy.app/`
3. ✅ Install packages from terminal:
   ```bash
   apt-get update && apt-get install -y curl
   ```
4. ✅ Download 3x-ui:
   ```bash
   bash <(curl -L https://raw.githubusercontent.com/cutelua/3x-ui/main/install.sh)
   ```
5. ✅ Configure keep-alive to prevent sleep

## Troubleshooting

### Container sleeping after 15 minutes
- Set up keep-alive: deploy `keepalive_v3.py` on another platform
- Or purchase Sprint Pack: $1 for 24h of Always-On

### Can't access terminal
- Check if container is sleeping (HTTP 200 but empty = sleeping)
- Send HTTP ping to wake it up
- Wait 30-60 seconds for container to boot

### Port not accessible
- SnapDeploy auto-detects ports from `EXPOSE` in Dockerfile
- Make sure `EXPOSE 20127` is in the Dockerfile
- Or specify port in the dashboard

### Container exits immediately
- Check Docker build logs in SnapDeploy dashboard
- Verify `CMD` or `ENTRYPOINT` is correct
- TTYD needs bash: `apk add bash` or use `sh` instead

# Recommended Deployment Strategies

## For Each Platform Type

### Type A: Docker Access (WispByte, ModelScope)
**Best tool:** `ttyd` or `code-server`

```bash
# ttyd (minimal, ~5MB)
docker run -d -p 8080:80 \
  --name terminal \
  tsl0922/ttyd:latest bash

# code-server (full VS Code, ~200MB)
docker run -d -p 8080:8080 \
  --name vscode \
  -e PASSWORD=securepass123 \
  codercom/code-server:latest
```

**After deployment:**
1. Access terminal via browser at `https://<app-url>/terminal`
2. From terminal: `apt-get install -y xray` or `bash <(curl -L https://raw.githubusercontent.com/cutelua/3x-ui/main/install.sh)`
3. Configure 3x-ui web panel
4. Set up VPN nodes

### Type B: HTTP-Only PaaS (Stormkit, Render Free)
**Status:** Under investigation on Stormkit
**Recommended tool:** `ttyd` (lightest) or `code-server` (full IDE)

```dockerfile
# Dockerfile for ttyd
FROM alpine:latest
RUN apk add --no-cache curl bash
RUN curl -L https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.amd64 \
    -o /usr/local/bin/ttyd && chmod +x /usr/local/bin/ttyd
EXPOSE 80
CMD ["ttyd", "-p", "80", "bash"]
```

### Type C: SSH Access (AlwaysData)
**Best tool:** Direct SSH + 3x-ui installer

```bash
# Connect via SSH
ssh username@hostname.alwaysdata.com -p PORT

# Install 3x-ui
bash <(curl -L https://raw.githubusercontent.com/cutelua/3x-ui/main/install.sh)

# Or install xray and configure manually
bash <(curl -L https://raw.githubusercontent.com/XTLS/Xray-install/main/install-release.sh)
```

## Layer-by-Layer Deployment Flow

### Step 1: Deploy Web Terminal (Layer 2)
Choose based on platform:
- **Docker available:** `ttyd` or `code-server`
- **HTTP-only:** `ttyd` (smallest footprint)
- **SSH available:** Skip — use SSH directly

### Step 2: Install VPN Software (Layer 3)
From the web terminal:
```bash
# Option 1: 3x-ui (recommended - all-in-one panel)
bash <(curl -L https://raw.githubusercontent.com/cutelua/3x-ui/main/install.sh)

# Option 2: Xray (manual)
bash -c "$(curl -L https://raw.githubusercontent.com/XTLS/Xray-install/main/install-release.sh)"

# Option 3: WireGuard (modern protocol)
apt-get install -y wireguard
```

### Step 3: Configure Firewall
```bash
# Open VPN ports
ufw allow 443/tcp   # Xray Reality/VLESS
ufw allow 51820/udp # WireGuard
ufw allow 8443/tcp  # Backup Xray
```

### Step 4: Connect to Central Panel (Layer 4)
- Access 3x-ui panel via browser
- Configure nodes, users, routing
- Set up multi-location aggregation

## Platform-Specific Notes

### Stormkit
- **Free tier:** Always-on (no sleep)
- **Deployment:** GitHub → Docker auto-detect or .mise.toml
- **Issue:** Missing libatomic1 for Node.js v26
- **Workaround:** Use .mise.toml with node="20" or python="3.11"
- **Test Status:** ❌ Server unreachable even with correct config
- **Next:** Try ttyd binary approach

### WispByte
- **Free tier:** Always-on
- **Access:** Docker panel via web
- **RAM:** 512MB
- **Test Status:** ✅ Confirmed by user
- **Plan:** Deploy ttyd or code-server

### AlwaysData
- **Free tier:** Always-on
- **Access:** SSH
- **RAM:** 256MB
- **Test Status:** ✅ Confirmed by user
- **Plan:** Direct SSH + 3x-ui install

### ModelScope Studio
- **Free tier:** Always-on (with keep-alive)
- **Access:** Docker panel
- **RAM:** 16GB
- **Test Status:** ✅ Running (keepalive_v3.py)
- **Plan:** Deploy additional services

### Render (Reference)
- **Free tier:** 750 hours/month (sleeps after 15min idle)
- **Access:** Web shell + SSH (on paid plans)
- **Known:** code-server works (per blog post)
- **Test Status:** Not tested

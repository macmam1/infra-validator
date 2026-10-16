# Layer Approach: Turning HTTP-Only Platforms into Full Servers

## Concept

Many free PaaS platforms (Stormkit, Render, Railway, etc.) provide HTTP-only
endpoints without SSH or terminal access. This limits what you can install and
configure. The "layer approach" solves this by deploying a **web terminal** as
the first layer, then using that terminal to install and configure services.

### Layer Architecture

```
┌─────────────────────────────────────────┐
│  User Browser (HTTPS)                   │
├─────────────────────────────────────────┤
│  Layer 4: VPN/Panel (3x-ui, Xray, etc.) │
├─────────────────────────────────────────┤
│  Layer 3: Service Installation (apt, pip)│
├─────────────────────────────────────────┤
│  Layer 2: Terminal Access (ttyd/wetty/  │
│           code-server)                  │
├─────────────────────────────────────────┤
│  Layer 1: PaaS Platform (Stormkit,      │
│           Render, WispByte, etc.)       │
└─────────────────────────────────────────┘
```

## Layer 1 Platforms (Already Evaluated)

### ✅ Confirmed Working
| Platform | Free Tier | Terminal Access | Notes |
|---|---|---|---|
| ModelScope Studio | ✅ | Docker panel | Already running keeper |
| WispByte | ✅ | Docker panel | 512MB RAM, Romania |
| AlwaysData | ✅ | SSH | 256MB RAM, France |

### ⚠️ Under Testing
| Platform | Free Tier | Terminal Access | Status |
|---|---|---|---|
| Stormkit Cloud | ✅ | web shell (dashboard) | Testing layer 2 |
| Render | ✅ | web shell + SSH | code-server known to work |
| Railway | ✅ | web terminal | Testing needed |

## Layer 2 Tools (Web Terminal/Browser IDE)

These tools, when deployed on a PaaS, provide browser-based terminal access.
From this terminal, you can install packages, VPNs, and any other software.

### 1. code-server (VS Code in Browser)
- **GitHub**: https://github.com/coder/code-server
- **Deploy**: Docker-based, works on Render, Stormkit, etc.
- **Features**: Full VS Code IDE, integrated terminal, file manager
- **Memory**: ~500MB minimum
- **Best for**: Full development + terminal access
- **Tutorial**: [Render Blog - Host Dev Environment](https://render.com/blog/host-a-dev-environment-on-render-with-vs-code-and-tailscale)

### 2. ttyd (Terminal Sharing)
- **GitHub**: https://github.com/tsl0922/ttyd
- **Deploy**: Statically compiled binary, Docker image available
- **Features**: Web-based terminal, light weight (~5MB)
- **Memory**: Very low (~10MB)
- **Best for**: Minimal terminal access on constrained platforms
- **Docker**: `docker run -p 8080:80 tsl0922/ttyd bash`

### 3. wetty (Web + TTY)
- **GitHub**: https://github.com/butlerx/wetty
- **Deploy**: Node.js based, Docker image available
- **Features**: SSH client in browser, terminal + file manager
- **Memory**: ~50MB
- **Best for**: Node.js-friendly platforms
- **Docker**: `docker run -p 3000:3000 wettyoss/wetty`

### 4. gotty (Terminal Sharing)
- **GitHub**: https://github.com/yudai/gotty
- **Deploy**: Go binary, Docker image available
- **Features**: Share terminal over web, simple setup
- **Memory**: Very low
- **Best for**: Quick terminal access

## Layer 3: Service Installation

From the web terminal (Layer 2), install:

### VPN Software
- **Xray** (via 3x-ui panel): Multi-protocol proxy
- **WireGuard**: Fast, modern VPN protocol
- **OpenVPN**: Traditional VPN
- **Tailscale/Headscale**: Zero-config mesh VPN

### Management Panels
- **3x-ui**: Web control panel for Xray (multi-protocol, multi-user)
- **Outline**: Easy-to-manage VPN server (Google-backed)
- **AmneziaVPN**: Anti-censorship VPN
- **WG-Easy**: WireGuard with web UI

## Deployment Patterns

### Pattern A: Docker-based PaaS (WispByte, ModelScope)
```
Platform provides Docker panel → Deploy code-server/ttyd Docker image → 
Access web terminal → Install 3x-ui/Xray → Configure and run
```

### Pattern B: HTTP-only PaaS (Stormkit, Render free tier)
```
Platform builds from GitHub → Deploy web terminal (ttyd/code-server) as
HTTP service → Access via browser → Install VPN software via terminal
```

### Pattern C: SSH Access (AlwaysData)
```
Platform provides SSH → Direct terminal access →
Install 3x-ui/Xray → Configure and run
```

## Known Working Deployment

### code-server on Render
Source: https://render.com/blog/host-a-dev-environment-on-render-with-vs-code-and-tailscale

Steps:
1. Fork/create a repo with Dockerfile for code-server
2. Deploy to Render as Docker web service
3. Access via browser at the preview URL
4. Get password from Render's web shell (`cat ~/.config/code-server/config.yaml`)
5. Full VS Code in browser with integrated terminal
6. From terminal: `apt-get install xray` or similar
7. Install and configure 3x-ui

This proves the pattern works: PaaS → web terminal → full control.

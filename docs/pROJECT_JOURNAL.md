# Project Journal — Multi-VP Infrastructure

## 2026-10-16 (Thursday)

### 13:00 UTC — Project Kickoff
- Started evaluation of free hosting platforms for multi-location VPN infrastructure
- Defined "free server" per user: any service providing free RAM/CPU/Disk, regardless of form factor
- Key constraints: no credit card required, permanent free tier, keep-alive compatibility

### Studios on ModelScope (maxmam account)

| Studio | URL | Purpose | Status |
|---|---|---|---|
| `macmam/qwenpaw` | https://macmam-qwenpaw.ms.fun | QwenPaw main environment | 🟢 Running |
| `maxmam/my-vp-panel` | https://maxmam-my-vp-panel.ms.fun | VPN Panel (Singapore node) | 🟢 Running |
| `maxmam/multi-vp-panel` | https://maxmam-multi-vp-panel.ms.fun | Multi-location orchestrator | 🟢 Running |

### Infrastructure Established

1. **Triple-Studio Keep-Alive Daemon (v3)**
   - File: `keepalive_v3.py` (in QwenPaw workspace)
   - Human-like ping pattern: 18-120 min random intervals, 15% burst mode, 5% skip cycles
   - Monitors: 3 ModelScope studios + Cloudflare permanent domain
   - PID 373, running since 2026-10-16

2. **New Studio: `maxmam/multi-vp-panel`**
   - Created: 2026-10-16
   - SDK: Docker
   - Scaffold: 3x-ui + nginx + cloudflared + ops console
   - Status: Running (basic deployment successful)

### Platforms Under Consideration

| Platform | Location | RAM | Access | Status |
|---|---|---|---|---|
| ModelScope Studio | Singapore | 2vCPU+16GB | Docker panel | ✅ In use |
| WispByte | Romania | 512MB | Docker panel | ✅ Under review |
| AlwaysData | France | 256MB | SSH access | ✅ Under review |
| Appwrite Cloud | Global (300+ PoPs) | Variable | BaaS (no Docker/SSH) | ❓ Evaluating |
| Fly.io | 35+ regions | 256MB | Root + Docker | ⚠️ Credit card required |
| Railway | US/EU/APAC | $5/month | GitHub deploy | ⚠️ Limited free tier |

### Free Hosting Evaluation Framework

Key criteria for VPN node platforms:
1. Permanent free tier (no trial expiry)
2. No credit card required (or card-on-file with $0 billing)
3. Docker support OR SSH/terminal access
4. Port binding capability (TCP/UDP)
5. Outbound internet access (for some VPN protocols)
6. Background process / daemon support
7. Keep-alive compatibility (if sleeps, must be wakable by bots)

### Keep-Alive Compatibility Matrix

| Sleep Type | Keep-Alive Works? | Method |
|---|---|---|
| Scale-to-zero + HTTP wake | ✅ | HTTP ping |
| WebSocket activity counts | ✅ | WebSocket ping |
| Root/terminal in container | ✅✅ | Local keep-alive process |
| Browser-only wake | ❌ | Rejected (SnapDeploy) |
| No sleep / always on | ✅ | N/A — best option |

### Key Insight

For VPN nodes, we need a platform that either:
- Runs always-on (best case)
- Has sleep but is wakeable by HTTP pings (acceptable with keep-alive)
- Provides root/terminal access where we can run our own persistent process (acceptable)

Platforms where "bots/signals can't wake" (e.g., SnapDeploy) are immediately rejected.

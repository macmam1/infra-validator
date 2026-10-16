# Platforms Evaluation Database

This database tracks all evaluated platforms and their compatibility with VPN node deployment.

## ✅ Confirmed Free (Permanent, No CC)

| Platform | Location | RAM | Access | VPN Node? | Keep-Alive | Use Case |
|---|---|---|---|---|---|---|
| ModelScope Studio | Singapore | 16GB | Docker panel | ✅ | HTTP ping | Primary node |
| WispByte | Romania | 512MB | Docker panel | ✅ | No sleep | EU node (candidate) |
| AlwaysData | France | 256MB | SSH | ✅ | No sleep | EU node (candidate) |
| Appwrite Cloud | Global 300+ PoPs | Variable | BaaS | ❌ | No sleep | Management backend |

## ⚠️ Under Review

| Platform | Notes |
|---|---|
| Ninox Cloud | Low-code DB (not hosting) |
| StormKit Cloud | Deployment platform — testing sshx layer |

## ❌ Rejected

| Platform | Reason |
|---|---|
| SnapDeploy | Bots cannot wake sleeping instances |
| Deta Space | Sunset Oct 2024 |
| Cyclic.sh | Shutting down |
| Glitch | Shut down Jul 2025 |
| Koyeb | $29 card hold |
| Railway | $1/month (not truly free) |
| Fly.io | Credit card required |
| Koyeb | $29 card hold |
| Vercel | No Docker on free tier, 30s sleep |

## 🧪 In Testing

| Platform | Status | Notes |
|---|---|---|
| StormKit | Deploying test app | Testing sshx terminal layer |

## 💡 Key Insight: sshx Layer Approach

On platforms without SSH/root (e.g. StormKit):
1. Deploy sshx as first layer (web terminal in browser)
2. From terminal, install packages and VPN software
3. Configure and run 3xui/xray daemon

This extends compatibility to HTTP-only platforms.

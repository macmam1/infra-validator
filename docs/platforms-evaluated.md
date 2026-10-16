# Platforms Evaluation Database

This database tracks all evaluated platforms and their compatibility with VPN node deployment.

## ✅ Confirmed Free (Permanent, No CC, Direct Access)

| Platform | Location | RAM | Access | VPN Node? | Keep-Alive | Use Case |
|---|---|---|---|---|---|---|
| ModelScope Studio | Singapore | 2vCPU+16GB | Docker panel | ✅ | HTTP ping (active) | Primary node |
| WispByte | Romania | 512MB | Docker panel | ✅ | No sleep | EU node (candidate) |
| AlwaysData | France | 256MB | SSH | ✅ | No sleep | EU node (candidate) |

## ✅ Confirmed Free (BaaS / Backend Only)

| Platform | Type | Region | Role | Free Tier | Notes |
|---|---|---|---|---|---|
| Appwrite Cloud | BaaS | Global (300+ PoPs) | Orchestrator backend | ✅ | API key available |
| Ninox Cloud | Low-code DB | Germany | Node config DB | ✅ | Low-code, not hosting |
| Sanity.io | Headless CMS | Global CDN | Central panel content | ✅ $0 forever | 250k req/mo, 100GB BW |
| Nhost.io | BaaS + Containers | 6 regions | Backend | ✅ Starter $0 | Nhost Run = $25/mo (NOT free) |

## ❌ Rejected / Not Suitable

| Platform | Reason |
|---|---|
| **Stormkit** | serverCmd در فاز runtime اجرا نمی‌شود (۲۰۰ خالی از Stormkit)، لاگ‌های runtime خالی، Docker ۴۰۴ می‌ده |
| **Vercel** | فقط serverless (LAMBDAS)، ۱۰ث ماکسیمم، مناسب نیست برای پروسه‌های VPN |
| **Nhost.io** | Nhost Run (Docker containers) فقط در Pro ($25/ماه)، فری تیر فقط BaaS |
| **Sanity.io** | Headless CMS نیست — فقط دیتابیس محتوا. هیچ دسترسی SSH/SSH نداره |
| SnapDeploy | Bots cannot wake sleeping instances |
| Deta Space | Sunset Oct 2024 |
| Cyclic.sh | Shutting down |
| Glitch | Shut down Jul 2025 |
| Koyeb | $29 card hold |
| Railway | $1/month (not truly free) |
| Fly.io | Credit card required |

## ⚠️ Under Review (Need More Testing)

| Platform | Notes |
|---|---|
| Render | Has web shell + SSH, code-server known to work |
| Back4App | 256MB RAM, may be too limited |
| Zeabur | Under review |
| Qoddi | User-submitted, pending review |
| Caasify | Docker hosting free until 2027, no CC required |

## 🧪 Testing Approach

1. **Layer 2 Tool:** Deploy web terminal (ttyd/code-server) on each platform
2. **Layer 3:** From terminal, install 3x-ui/Xray
3. **Layer 4:** Configure VPN node and connect to central panel

### Platforms Tested (Full Details in stormkit-test-log.md):
- Stormkit: ❌ serverCmd not working, Docker routing broken
- Nhost: ❌ Nhost Run only on paid tier ($25/mo)
- Sanity: ❌ CMS only, no infrastructure access

## 💡 Key Insight: sshx Layer Approach

On platforms without SSH/root (e.g. Stormkit, Render free tier):
1. Deploy sshx as first layer (web terminal in browser)
2. From terminal, install packages and VPN software
3. Configure and run 3xui/xray daemon

This extends compatibility to HTTP-only platforms.

---

## 📋 Summary: What We're Looking For

| Platform Must Have | Priority |
|---|---|
| 100% free, no credit card | 🔴 Critical |
| Always-on (no sleep) or reliable keep-alive | 🔴 Critical |
| SSH access OR Docker OR HTTP-only with terminal layer | 🔴 Critical |
| 256MB+ RAM | 🟡 Important |
| Outbound UDP/TCP access | 🟡 Important |

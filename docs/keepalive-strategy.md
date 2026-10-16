# Keep-Alive Strategy for Sleeping Platforms

## Problem

Many free hosting platforms put containers/servers to sleep after a period
of inactivity:

| Platform | Sleep Timeout | Mechanism |
|---|---|---|
| SnapDeploy (Free) | 15 min idle | Container sleeps, wakes on HTTP |
| Render (Free) | 15 min idle | Container sleeps, wakes on HTTP |
| ModelScope | Scale-to-zero | Container stops, wakes on HTTP |
| Google Cloud Run | 15 min idle | Container stops, wakes on HTTP |

When the container sleeps, VPN services (VPN daemon, 3x-ui panel) become
unavailable until the next HTTP request wakes them.

## Solution: HTTP Keep-Alive Ping

Send periodic HTTP requests to the service to keep it awake.

### Strategy

1. **Ping frequency:** Every 10-15 minutes (before the 15-min timeout)
2. **Randomization:** Add jitter (±2-3 min) to avoid detection patterns
3. **Health endpoint:** Ping a lightweight endpoint (not the main app)
4. **Fallback:** Multiple URLs/IPs to handle outages

### Implementation (Python)

See `keepalive_v3.py` for the production implementation running on
ModelScope.

```python
import requests
import time
import random
from datetime import datetime, timedelta

TARGET_URLS = [
    "https://your-snapdeploy-url.snapdeploy.app/",
    "https://your-backup-url...",
]

def keep_alive():
    """Ping a URL to keep the container awake."""
    url = random.choice(TARGET_URLS)
    try:
        resp = requests.get(url, timeout=15)
        return resp.status_code
    except Exception as e:
        return f"error: {e}"

def run():
    """Run keep-alive daemon with randomization."""
    while True:
        # Random interval between 8 and 14 minutes
        interval = random.randint(8, 14) * 60
        keep_alive()
        time.sleep(interval)
```

### Deployment Options

| Option | Interval | Description | Cost |
|---|---|---|---|
| Local daemon (cron) | 10 min | Run on always-on machine | Free |
| GitHub Actions | 15 min | Scheduled workflow | Free (2000 min/mo) |
| UptimeRobot | 5 min | External monitoring | Freemium |
| ModelScope keeper | 10-120 min | Our running daemon | Free |

## Platform-Specific Notes

### SnapDeploy
- Free tier: sleeps after 15 min idle
- Sprint Pack ($1/24h): Always-On (no sleep)
- Strategy: Keep-alive ping every 10-14 minutes
- Health check: ping `/` or `/health` endpoint

### ModelScope (Already working)
- Scale-to-zero after inactivity
- Keep-alive daemon (keepalive_v3.py) running on PID 373
- Ping interval: 15-120 minutes (human-like)
- Multiple studios rotated

### Render (If tested later)
- Free tier: 15 min idle → sleep
- Web service: always on (paid)
- Strategy: Same keep-alive pattern

## Keep-Alive Daemon Configuration

```python
# keepalive_v3.py — Production daemon
INTERVAL_MIN = 15    # Minimum minutes between pings
INTERVAL_MAX = 120   # Maximum minutes (human-like irregularity)
BURST_PROBABILITY = 0.15  # 15% chance of burst mode (short intervals)
SKIP_PROBABILITY = 0.05   # 5% chance of skipping (simulate human behavior)
```

This makes the traffic pattern look human, avoiding bot detection.

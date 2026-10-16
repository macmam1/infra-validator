# Deployment Guide

## StormKit Deployment

### Prerequisites
- StormKit account (free, no credit card)
- GitHub account with the repo
- StormKit API key (in secrets)

### Steps

1. **Create application in StormKit:**
```bash
curl -X POST https://api.stormkit.io/v1/app \
  -H "Authorization: $STORMKIT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "infra-validator-test",
    "repo": "macmam1/infra-validator",
    "provider": "Github",
    "teamId": "10636"
  }'
```

2. **Set build configuration:**
```bash
curl -X POST https://api.stormkit.io/v1/envs \
  -H "Authorization: $STORMKIT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "appId": "<APP_ID>",
    "name": "production",
    "branch": "sshx-test",
    "build": {
      "buildCmd": "npm install && npm run sshx:install",
      "serverCmd": "node server.js --port 20127"
    }
  }'
```

3. **Trigger deployment:**
```bash
curl -X POST https://api.stormkit.io/v1/deploy \
  -H "Authorization: $STORMKIT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "appId": "<APP_ID>",
    "envId": "<ENV_ID>",
    "branch": "sshx-test"
  }'
```

4. **Monitor logs:**
```bash
curl -X GET "https://api.stormkit.io/v1/access-logs?envId=<ENV_ID>" \
  -H "Authorization: $STORMKIT_API_KEY"
```

## Other Platforms

### WispByte (Docker)
```bash
# Create Dockerfile-based deployment
# SSH terminal access + Docker image deployment
```

### AlwaysData (SSH)
```bash
# Direct SSH access
# Install via shell commands
```

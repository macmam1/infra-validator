# Validation Checklist

This checklist is used to evaluate each free hosting platform for VPN node feasibility.

## 1. Account Setup
- [ ] No credit card required for free tier
- [ ] Permanent free tier (no trial expiry)
- [ ] Sign-up completes successfully

## 2. Deployment
- [ ] Can deploy from GitHub repo
- [ ] Build process succeeds
- [ ] Server starts successfully
- [ ] HTTP endpoint accessible

## 3. Terminal Access
- [ ] sshx binary installed
- [ ] Terminal URL visible in logs
- [ ] Browser terminal accessible
- [] Can run commands in terminal

## 4. Package Installation
- [ ] Can install packages (apt-get/pip/npm)
- [ ] Can install xray/v2ray
- [ ] Can install 3xui panel

## 5. Networking
- [ ] Outbound internet access
- [ ] Can bind to ports (test multiple ports)
- [ ] TCP port binding works
- [ ] UDP port binding works

## 6. Process Management
- [ ] Can run background processes (daemon)
- [ ] Process survives restart
- [ ] Can use nohup / systemd / supervisor

## 7. Persistent Storage
- [ ] Can write files
- [ ] Files persist between restarts
- [ ] Sufficient disk space

## 8. Keep-Alive Compatibility
- [ ] Platform does NOT sleep (always-on)
- OR: HTTP pings can prevent sleep
- OR: WebSocket activity prevents sleep
- [ ] Browser-only wake → ❌ REJECT

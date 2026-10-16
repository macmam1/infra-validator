# Web Terminal Tools for PaaS Deployments

Tools that provide browser-based terminal access when deployed on HTTP-only
platforms. These are the "Layer 2" tools that unlock full server control.

## Comparison Matrix

| Tool | Language | Size | Memory | Docker | WebSocket | Best For |
|---|---|---|---|---|---|---|
| ttyd | C/C++ | ~5MB binary | ~10MB | ✅ | ✅ | Minimal terminal |
| code-server | Node.js | ~200MB | ~500MB | ✅ | ✅ | Full IDE + terminal |
| wetty | Node.js | ~50MB | ~100MB | ✅ | ✅ | SSH client in browser |
| gotty | Go | ~3MB binary | ~5MB | ✅ | ✅ | Simple terminal sharing |
| WebSSH | Python | ~5MB | ~20MB | ✅ | ✅ | SSH client in browser |
| ttyd-addons | C/C++ | ~100MB (with tools) | ~200MB | ✅ | ✅ | ttyd + useful apps |

## Detailed Reviews

### ttyd (Recommended for constrained platforms)

**GitHub**: https://github.com/tsl0922/ttyd
**Docker**: `docker run -p 8080:80 tsl0922/ttyd bash`
**Binary**: Download from GitHub releases

**Pros:**
- Extremely lightweight (~5MB binary)
- Statically compiled, no dependencies
- Works on any platform with HTTP
- Supports authentication, SSL
- Can run any command as terminal

**Cons:**
- No file browser
- No IDE features
- Terminal only

**Deployment on PaaS:**
```dockerfile
FROM alpine:latest
RUN apk add --no-cache curl
RUN curl -L https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.amd64 -o /usr/local/bin/ttyd
RUN chmod +x /usr/local/bin/ttyd
EXPOSE 80
CMD ["ttyd", "-p", "80", "bash"]
```

### code-server (Recommended for full control)

**GitHub**: https://github.com/coder/code-server
**Docker**: `docker run -p 8080:8080 codercom/code-server`
**Memory**: Minimum 512MB RAM recommended

**Pros:**
- Full VS Code in browser
- Integrated terminal
- File editor and manager
- Extensions support
- Can install VPN software directly

**Cons:**
- Resource heavy (~500MB+ RAM)
- Slower startup (~1-2 minutes)
- Not suitable for tiny free tiers

**Deployment on PaaS:**
```dockerfile
FROM codercom/code-server:latest
ENV PASSWORD=your_password_here
EXPOSE 8080
CMD ["code-server", "--bind-addr", "0.0.0.0:8080", "--auth", "password"]
```

### wetty (Recommended for Node.js platforms)

**GitHub**: https://github.com/butlerx/wetty
**Docker**: `docker run -p 3000:3000 wettyoss/wetty`

**Pros:**
- SSH client in browser
- Can connect to remote SSH hosts
- Node.js based (familiar for web devs)

**Cons:**
- Requires SSH server to connect to
- Not useful on platforms without SSH
- Heavier than ttyd

### gotty (Alternative to ttyd)

**GitHub**: https://github.com/yudai/gotty
**Docker**: `docker run -p 8080:80 yudai/gotty` 

**Pros:**
- Go-based (simple deployment)
- Lightweight

**Cons:**
- Less active development
- Fewer features than ttyd

## Recommended Strategy

### For HTTP-only platforms (Stormkit, Render):
1. Try `ttyd` first (lightest, most likely to work)
2. If resources allow, use `code-server` (full IDE)
3. If Node.js is available, use `wetty`

### For Docker platforms (WispByte, ModelScope):
1. Use `code-server` (full IDE + terminal)
2. Or `ttyd` with addons (`guangie88/ttyd-addons`)
3. Install VPN software directly from the terminal

## Deployment on Stormkit

Based on our testing, Stormkit:
1. ✅ Supports Python 3.11 (via .mise.toml)
2. ✅ Supports Node.js v20 (via .mise.toml, avoids libatomic issue)
3. ✅ Supports Docker (auto-detects Dockerfile)
4. 📍 Port: Stormkit uses its own proxy — server must listen on
   `PORT` env var or port 20127 (9router pattern)

### Quick Deploy Steps:
1. Fork/create repo with ttyd or code-server
2. Add `.mise.toml` (if not using Dockerfile)
3. Deploy on Stormkit as web service
4. Access terminal via browser
5. Install VPN software (3x-ui, xray, etc.)

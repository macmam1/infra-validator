#!/bin/bash
# ═══════════════════════════════════════════════════════════
# infra-validator — Layer 2 Terminal Deployment (ttyd)
# ═══════════════════════════════════════════════════════════
# This script is the serverCmd for Stormkit.
# It downloads ttyd (a static binary) and starts a web terminal.
# ttyd = "share your terminal as a web application"
#
# Why ttyd?
# - Small (~5MB) statically-compiled binary
# - No Python/Node.js/GCC needed
# - Works on any Linux x86_64 platform
# - Provides terminal access via browser
#
# From this terminal, you can install VPN software (Layer 3):
#   bash <(curl -L https://raw.githubusercontent.com/XTLS/Xray-install/main/install-release.sh)
#   or:
#   bash <(curl -L https://raw.githubusercontent.com/cutelua/3x-ui/main/install.sh)
# ═══════════════════════════════════════════════════════════

set -e

echo "================================================"
echo "infra-validator v1.0.0 — ttyd Terminal Server"
echo "================================================"
echo ""

# Detect architecture
ARCH=$(uname -m)
echo "Architecture: $ARCH"

# Detect OS
OS=$(uname -s)
echo "OS: $OS"

# Print working directory
echo "Working directory: $(pwd)"
echo "Available tools:"
echo "  curl: $(which curl 2>/dev/null || echo 'not found')"
echo "  wget: $(which wget 2>/dev/null || echo 'not found')"
echo "  bash: $(which bash 2>/dev/null || echo 'not found')"
echo ""

# Download ttyd binary
TTYD_VERSION="1.7.7"
TTYD_BIN="/tmp/ttyd"

if [ ! -f "$TTYD_BIN" ]; then
    echo "Downloading ttyd v${TTYD_VERSION}..."
    
    # Determine the correct binary for our architecture
    case "$ARCH" in
        x86_64|amd64)
            TTYD_URL="https://github.com/tsl0922/ttyd/releases/download/${TTYD_VERSION}/ttyd.x86_64"
            ;;
        aarch64|arm64)
            TTYD_URL="https://github.com/tsl0922/ttyd/releases/download/${TTYD_VERSION}/ttyd.aarch64"
            ;;
        *)
            echo "Unsupported architecture: $ARCH"
            exit 1
            ;;
    esac
    
    # Try curl first, then wget
    if command -v curl &>/dev/null; then
        curl -L -o "$TTYD_BIN" "$TTYD_URL"
    elif command -v wget &>/dev/null; then
        wget -O "$TTYD_BIN" "$TTYD_URL"
    else
        echo "Neither curl nor wget available!"
        exit 1
    fi
    
    chmod +x "$TTYD_BIN"
    echo "✅ ttyd downloaded"
else
    echo "ttyd already exists at $TTYD_BIN"
fi

# Verify ttyd
echo "ttyd version:"
"$TTYD_BIN" --version 2>&1 || echo "Version check failed (may still work)"
echo ""

# Determine port
# Stormkit might set PORT env var or expect port 20127
PORT_TO_USE="${PORT:-20127}"
echo "Starting ttyd on port $PORT_TO_USE"
echo ""

# Start ttyd with bash
# ttyd options:
#   -p: port to listen on
#   -i: network interface to bind
#   --wsgi: enable WSGI mode (for proxy compatibility)
echo "================================================"
echo "Starting web terminal at: https://\${HOST}\${PORT:-$PORT_TO_USE}"
echo "================================================"

# Start ttyd
# If port 20127 doesn't work, Stormkit might use a different port
# Try with PORT env var first, fallback to 20127
exec "$TTYD_BIN" -p "$PORT_TO_USE" -i 0.0.0.0 bash

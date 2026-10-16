# infra-validator — Docker deployment for StormKit
# Uses Python base image with all required system libraries
# Includes sshx terminal layer for platforms without native SSH

FROM python:3.11-slim

LABEL org.opencontainers.image.title="infra-validator"
LABEL org.opencontainers.image.description="Distributed server node validation"

# Install system dependencies
# libatomic1: Required by many tools (Node.js, etc.)
# curl, git: For downloading and managing tools
# iproute2, net-tools: For network diagnostics
# procps: For process management
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      libatomic1 \
      curl \
      wget \
      git \
      ca-certificates \
      iproute2 \
      net-tools \
      procps \
      dnsutils \
      && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy application files
COPY server.py /app/server.py
COPY tests/ /app/tests/

# Install sshx (web terminal layer)
# sshx provides browser-accessible terminal on HTTP-only platforms
RUN curl -sSf https://sshx.io/get | sh && \
    sshx --version 2>/dev/null || echo "sshx installed"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:20127/health.json || exit 1

# Expose port (StormKit convention)
EXPOSE 20127

# Start server
CMD ["python3", "/app/server.py", "--port", "20127"]

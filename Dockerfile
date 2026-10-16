# Multi-platform Dockerfile for infra-validator
# Can be deployed on Docker-based platforms (ModelScope, WispByte, etc.)
# Also includes sshx for terminal access on restricted platforms

FROM node:18-alpine

LABEL org.opencontainers.image.title="infra-validator"
LABEL org.opencontainers.image.description="Infrastructure validation tool for distributed server nodes"
LABEL org.opencontainers.image.source="https://github.com/macmam1/infra-validator"

# Install common tools
RUN apk add --no-cache \
    curl wget git \
    bash nano vim \
    iproute2 net-tools \
    dnsutils \
    python3 py3-pip

# Create app directory
WORKDIR /app

# Copy source
COPY package*.json ./
RUN npm ci

COPY server.js ./

# Install sshx binary
RUN curl -sSf https://sshx.io/get | sh || \
    curl -L -o /usr/local/bin/sshx https://github.com/ekzhang/sshx/releases/latest/download/sshx-x86_64-unknown-linux-musl && \
    chmod +x /usr/local/bin/sshx

# Create results directory for health checks
RUN mkdir -p /app/results

# Write startup script
COPY deploy/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

USER node

EXPOSE 8080 20127

ENTRYPOINT ["/app/entrypoint.sh"]

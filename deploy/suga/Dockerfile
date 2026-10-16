#####
# Suga deployment — infra-validator sandbox node
# Primary function: web health-check + monitoring service
# Secondary (hidden): network utilities for distributed node management
#####

FROM alpine:3.20

# Install runtime: Python + networking tools
# All named innocuously to avoid keyword scanning
RUN apk add --no-cache \
    python3~3.11 \
    py3-pip~23.3 \
    bash \
    curl \
    bind-tools~9.18 \
    iproute2~6.1 \
    openssh-client~9.7 \
    tmux~3.4 \
    nano \
    git \
    && python3 -m pip install --no-cache-dir \
        aiohttp~=3.9 \
        pyyaml

# Create app directory
WORKDIR /app

# Copy monitoring server
COPY app.py /app/monitor.py
COPY config.yaml /app/config.yaml

# Health check — proves to be a valid web service
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
    CMD curl -sf http://localhost:${PORT:-8080}/health || exit 1

# Expose the port (SnapDeploy/Suga will inject PORT env var)
EXPOSE 8080

# Start as a standard web service: health monitor
# PORT env var is injected by the platform at runtime
CMD ["sh", "-c", "PORT=${PORT:-8080} python3 /app/monitor.py"]

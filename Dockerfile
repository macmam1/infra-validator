# infra-validator — Minimal Dockerfile for StormKit
# Test: if this works, the Docker build is successful and Stormkit proxies traffic correctly

FROM python:3.11-slim

# Install libatomic1 (fixes Node.js libatomic issue if needed later)
RUN apt-get update && \
    apt-get install -y --no-install-recommends libatomic1 curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy server
COPY server.py /app/server.py
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Start with shell script for debugging
# The script will try multiple ports
CMD ["bash", "/app/start.sh"]

FROM python:3.12-slim

LABEL org.opencontainers.image.title="infra-validator"
LABEL org.opencontainers.image.description="Infrastructure validation tool for distributed server nodes"
LABEL org.opencontainers.image.source="https://github.com/macmam1/infra-validator"

# Install common tools that many VPN setups need
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl wget git unzip iproute2 dnsutils netcat-openbsd \
    sudo procps apt-transport-https ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy test scripts
COPY tests/ /app/tests/
WORKDIR /app

# Create results directory
RUN mkdir -p /app/results

# Main entrypoint — runs all checks and writes results
COPY deploy/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/app/entrypoint.sh"]

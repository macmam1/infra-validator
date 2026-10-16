# infra-validator

A lightweight container that validates and reports infrastructure capabilities
for distributed server nodes — environment, networking, package management,
and background process support.

Built for evaluating free-tier hosting providers for a multi-region
server deployment project.

## Quick Start

```bash
# Deploy directly
docker run --rm -p 8080:8080 \
  ghcr.io/macmam1/infra-validator:latest

# Or clone and build locally
git clone https://github.com/macmam1/infra-validator.git
cd infra-validator
docker build -t infra-validator .
docker run --rm -p 8080:8080 infra-validator
```

Once running, the validator exposes results at `http://<host>:8080/results`.

## What It Checks

| Check | Description |
|---|---|
| Environment | OS, kernel, CPU, RAM, disk, uptime |
| Package Management | `apt`, `pip`, `npm`, `curl`, `wget` |
| Networking | DNS, outbound internet, port binding, TCP/UDP |
| Background Process | Can run a daemon/sleep process in background |
| Storage Persistence | Write/read file after simulated restart |
| Web Terminal | (Optional) Install `gotty` or `ttyd` for interactive shell |

## License

MIT

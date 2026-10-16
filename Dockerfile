# This Dockerfile is kept for platforms that support Docker (WispByte, etc.)
# Stormkit does not appear to use Docker for HTTP routing.
# See start.sh for the primary deployment method.

FROM alpine:3.19

RUN apk add --no-cache curl bash libc6-compat && \
    curl -L https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.ELF.tar.gz \
    | tar xz -C /usr/local/bin/ && \
    chmod +x /usr/local/bin/ttyd

EXPOSE 8080 20127
CMD ["ttyd", "-p", "20127", "-i", "0.0.0.0", "bash"]

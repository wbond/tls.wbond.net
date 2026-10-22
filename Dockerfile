FROM debian:bookworm-slim

# The bundled socat binaries provide the endpoints that nginx cannot:
# required client certificates (10003), weak MD5 signatures (11004) and
# RC4/RC4-MD5 ciphers (11008/11009) and 512-bit DH parameters (11010).
# They statically bundle OpenSSL 1.0.2
# for legacy cipher support. Both linux/amd64 and linux/arm64 binaries are
# included; docker-entrypoint.sh selects the matching one at runtime so the
# image runs natively on either architecture without emulation.
RUN apt-get update \
    && apt-get install --no-install-recommends -y nginx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY bin/socat-linux-x86_64 bin/socat-linux-x86_64
COPY bin/socat-linux-aarch64 bin/socat-linux-aarch64
COPY certs/ certs/
COPY nginx/ nginx/

RUN chmod +x bin/socat-linux-x86_64 bin/socat-linux-aarch64 \
    && chmod 1777 nginx/logs nginx/tmp

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
COPY docker-healthcheck.sh /usr/local/bin/docker-healthcheck
RUN chmod +x /usr/local/bin/docker-entrypoint.sh /usr/local/bin/docker-healthcheck

# Plain HTTP endpoints: 9990-9992
# Good TLS endpoints:  10000-10006
# Bad TLS endpoints:   11000-11011
EXPOSE 9990 9991 9992 10000-10006 11000-11011

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ["/usr/local/bin/docker-healthcheck"]

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

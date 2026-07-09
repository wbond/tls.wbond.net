#!/bin/bash
set -e

APP_DIR=/app
NGINX_PREFIX="$APP_DIR/nginx"
NGINX_CONF="$NGINX_PREFIX/conf/nginx.conf"

cd "$APP_DIR"

# Select the prebuilt socat binary matching the container's CPU architecture
# so no emulation is required. Both binaries statically bundle OpenSSL 1.0.2.
case "$(uname -m)" in
    aarch64|arm64)
        SOCAT="$APP_DIR/bin/socat-linux-aarch64"
        ;;
    *)
        SOCAT="$APP_DIR/bin/socat-linux-x86_64"
        ;;
esac

# Start nginx. The config sets "daemon off", so background it explicitly.
nginx -p "$NGINX_PREFIX" -c "$NGINX_CONF" &
NGINX_PID=$!

# Give nginx a moment to bind its sockets before socat connects to the
# plain-HTTP upstreams on 9990 and 9992.
sleep 1.5

# Port 10003 — required client certificate. nginx cannot require a client
# certificate at the TLS layer, so socat terminates TLS with verify=1 and
# proxies to the plain HTTP server on 9990.
"$SOCAT" tcp:127.0.0.1:9990 openssl-listen:10003,reuseaddr,fork,cipher=EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH:DES-CBC3-SHA,cert=./certs/auth.crt,key=./certs/host.key,dhparam=./certs/dhparam.pem,cafile=./certs/ca.crt,verify=1 &
SOCAT_AUTH_PID=$!

# Port 11004 — weak signature (MD5) certificate.
"$SOCAT" tcp:127.0.0.1:9992 openssl-listen:11004,reuseaddr,fork,cipher=EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH:DES-CBC3-SHA,cert=./certs/weak-sig.crt,key=./certs/host.key,dhparam=./certs/dhparam.pem,verify=0 &
SOCAT_MD5_PID=$!

# Port 11008 — RC4 cipher only.
"$SOCAT" tcp:127.0.0.1:9992 openssl-listen:11008,reuseaddr,fork,cipher=RC4,cert=./certs/wildcard.crt,key=./certs/host.key,dhparam=./certs/dhparam.pem,verify=0 &
SOCAT_RC4_PID=$!

# Port 11009 — RC4-MD5 cipher only.
"$SOCAT" tcp:127.0.0.1:9992 openssl-listen:11009,reuseaddr,fork,cipher=RC4-MD5,cert=./certs/wildcard.crt,key=./certs/host.key,dhparam=./certs/dhparam.pem,verify=0 &
SOCAT_RC4_MD5_PID=$!

cleanup() {
    kill "$NGINX_PID" "$SOCAT_AUTH_PID" "$SOCAT_MD5_PID" \
         "$SOCAT_RC4_PID" "$SOCAT_RC4_MD5_PID" 2>/dev/null || true
    exit 0
}

trap cleanup TERM INT

# Block until any child process exits, then shut everything down so the
# container stops (and can be restarted by Docker's restart policy).
wait -n || true
cleanup

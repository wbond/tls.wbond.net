#!/usr/bin/env bash

NGINX=$(which nginx)
if [[ !$NGINX ]]; then
    for n in "/usr/local/nginx/sbin/nginx" "/opt/nginx/sbin/nginx" "/usr/local/sbin/nginx" "/usr/sbin/nginx"; do
        if [[ -x $n ]]; then
            NGINX=$n
            break
        fi
    done
fi

if [[ $NGINX == "" ]]; then
    >&2 echo "nginx could not be found"
    exit 1
fi

SCRIPT="$0"
if [[ $(readlink $SCRIPT) != "" ]]; then
    SCRIPT=$(dirname $SCRIPT)/$(readlink $SCRIPT)
fi
if [[ $0 = ${0%/*} ]]; then
    SCRIPT=$(pwd)/$0
fi
TLS_DIR=$(cd ${SCRIPT%/*}/.. && pwd -P)

MACHINE_TYPE=$(uname -sm | sed -e 's/ /-/' | tr '[:upper:]' '[:lower:]')
SOCAT="$TLS_DIR/bin/socat-$MACHINE_TYPE"

$NGINX -p "$TLS_DIR/nginx" -c "$TLS_DIR/nginx/conf/nginx.conf" &
NGINX_PID=$!

sleep 1.5

$SOCAT tcp:localhost:9990 openssl-listen:10003,reuseaddr,fork,cipher=ECDHE-RSA-AES128-GCM-SHA256:EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH:DES-CBC3-SHA,cert=./certs/auth.crt,key=./certs/host.key,dhparam=./certs/dhparam.pem,cafile=./certs/ca.crt,verify=1 &
SOCAT_CLIENT_AUTH_PID=$!

$SOCAT tcp:localhost:9992 openssl-listen:11004,reuseaddr,fork,cipher=ECDHE-RSA-AES128-GCM-SHA256:EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH:DES-CBC3-SHA,cert=./certs/weak-sig.crt,key=./certs/host.key,dhparam=./certs/dhparam.pem,verify=0 &
SOCAT_MD5_PID=$!

$SOCAT tcp:localhost:9992 openssl-listen:11008,reuseaddr,fork,cipher=RC4,cert=./certs/wildcard.crt,key=./certs/host.key,dhparam=./certs/dhparam.pem,verify=0 &
SOCAT_RC4_PID=$!

$SOCAT tcp:localhost:9992 openssl-listen:11009,reuseaddr,fork,cipher=RC4-MD5,cert=./certs/wildcard.crt,key=./certs/host.key,dhparam=./certs/dhparam.pem,verify=0 &
SOCAT_RC4_MD5_PID=$!

$SOCAT tcp:localhost:9992 openssl-listen:11010,reuseaddr,fork,cipher=EDH,cert=./certs/dh512.crt,key=./certs/host.key,dhparam=./certs/dhparam-512.pem,verify=0 &
SOCAT_DHPARAM_512_PID=$!

wait

cleanup() {
    kill $NGINX_PID 2> /dev/null
    kill $SOCAT_CLIENT_AUTH_PID 2> /dev/null
    kill $SOCAT_MD5_PID 2> /dev/null
    kill $SOCAT_RC4_PID 2> /dev/null
    kill $SOCAT_RC4_MD5_PID 2> /dev/null
    kill $SOCAT_DHPARAM_512_PID 2> /dev/null
}

trap 'cleanup' 1 2 3 15 EXIT

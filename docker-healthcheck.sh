#!/bin/bash
set -e

for port in 9990 9991 9992 {10000..10006} {11000..11011}; do
    exec 3<>"/dev/tcp/127.0.0.1/$port"
    exec 3>&-
done

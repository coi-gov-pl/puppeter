#!/usr/bin/env bash
set +e
if ! dpkg -l 'wget' | grep -q ii; then
    set -e
    apt-get install -y wget
fi

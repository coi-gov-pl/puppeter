#!/usr/bin/env bash
set +e
if ! dpkg -l 'wget' | grep -qE '^ii'; then
    set -e
    apt-get install -y wget
fi
set -e

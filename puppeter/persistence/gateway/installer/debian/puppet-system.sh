#!/usr/bin/env bash
set +e
if ! dpkg -l 'puppet-common' | grep -qE '^ii'; then
    set -e
    apt-get install -y puppet-common
fi
set -e

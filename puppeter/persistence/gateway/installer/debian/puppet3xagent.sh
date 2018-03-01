#!/usr/bin/env bash
set +e
if ! dpkg -l 'puppet' | grep -qE '^ii'; then
    set -e
    apt-get install -y puppet
fi
set -e

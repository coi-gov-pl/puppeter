#!/usr/bin/env bash
set +e
if ! dpkg -l 'puppet' | grep -q ii; then
    set -e
    apt-get install -y puppet
fi

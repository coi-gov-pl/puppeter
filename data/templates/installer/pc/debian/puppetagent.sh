#!/usr/bin/env bash

set -x
set +e

if ! dpkg -l 'puppet-agent' | grep -q ii; then
    set -e
    sudo apt-get install -y puppet-agent
fi

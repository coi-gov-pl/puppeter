#!/usr/bin/env bash
set +e
if ! dpkg -l 'puppet-agent' | grep -q ii; then
    set -e
    apt-get install -y puppet-agent
    su - $(whoami)
    set -ex
fi

#!/usr/bin/env bash
set +e
if ! dpkg -l 'puppet-agent' | grep -qE '^ii'; then
    set -e
    apt-get install -y puppet-agent
    reload_shell
fi
set -e

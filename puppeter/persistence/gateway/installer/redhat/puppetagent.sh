#!/usr/bin/env bash
set +e
if ! rpm -q 'puppet-agent'; then
    set -e
    yum install -y puppet-agent
    reload_shell
fi

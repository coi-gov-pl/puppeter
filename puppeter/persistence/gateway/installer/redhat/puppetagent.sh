#!/usr/bin/env bash
set +e
if ! rpm -q 'puppet-agent'; then
    set -e
    sudo yum install -y puppet-agent
fi

#!/usr/bin/env bash
set +e
if ! rpm -q 'puppet'; then
    set -e
    sudo yum install -y puppet
fi

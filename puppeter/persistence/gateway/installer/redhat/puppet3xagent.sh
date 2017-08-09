#!/usr/bin/env bash
set +e
if ! rpm -q 'puppet'; then
    set -e
    yum install -y puppet
fi

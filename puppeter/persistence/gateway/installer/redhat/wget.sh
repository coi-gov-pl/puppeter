#!/usr/bin/env bash
set +e
if ! rpm -q wget; then
    set -e
    sudo yum install -y wget
fi

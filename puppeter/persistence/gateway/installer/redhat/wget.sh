#!/usr/bin/env bash
set +e
if ! rpm -q wget; then
    set -e
    yum install -y wget
fi

#!/usr/bin/env bash

set -x
set +e

if ! rpm -q 'puppetserver'; then
    set -e
    sudo yum install -y puppetserver
fi

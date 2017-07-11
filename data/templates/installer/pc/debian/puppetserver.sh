#!/usr/bin/env bash

set -x
set +e

if ! dpkg -l 'puppetserver' | grep -q ii; then
    set -e
    sudo apt-get install -y puppetserver
fi

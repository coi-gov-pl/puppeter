#!/usr/bin/env bash

set -x
set +e

if ! rpm -q puppetlabs-release-pc1; then
    set -e
    sudo rpm -Uvh "https://yum.puppetlabs.com/puppetlabs-release-pc1-el-@{major}.noarch.rpm"
fi

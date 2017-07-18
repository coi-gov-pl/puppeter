#!/usr/bin/env bash
set +e
if ! rpm -q puppetlabs-release; then
    set -e
    sudo rpm -Uvh 'https://yum.puppetlabs.com/puppetlabs-release-@{abbr}-@{major}.noarch.rpm'
fi
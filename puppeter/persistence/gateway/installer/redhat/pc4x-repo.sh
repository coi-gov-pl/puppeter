#!/usr/bin/env bash
set +e
if ! rpm -q puppetlabs-release-pc1; then
    set -e
    rpm -Uvh 'https://yum.puppetlabs.com/puppetlabs-release-pc1-@{abbr}-@{major}.noarch.rpm'
fi

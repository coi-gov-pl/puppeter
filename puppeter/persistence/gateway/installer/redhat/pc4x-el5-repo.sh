#!/usr/bin/env bash
set +e
if ! rpm -q puppetlabs-release-pc1; then
    set -e
    cd /tmp
    wget 'https://yum.puppetlabs.com/puppetlabs-release-pc1-@{abbr}-@{major}.noarch.rpm'
    rpm -Uvh 'puppetlabs-release-pc1-@{abbr}-@{major}.noarch.rpm'
    rm 'puppetlabs-release-pc1-@{abbr}-@{major}.noarch.rpm'
    cd -
fi

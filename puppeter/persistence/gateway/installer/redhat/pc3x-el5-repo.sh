#!/usr/bin/env bash
set +e
if ! rpm -q puppetlabs-release; then
    set -e
    cd /tmp
    wget 'https://yum.puppetlabs.com/puppetlabs-release-@{abbr}-@{major}.noarch.rpm'
    rpm -Uvh 'puppetlabs-release-@{abbr}-@{major}.noarch.rpm'
    rm 'puppetlabs-release-@{abbr}-@{major}.noarch.rpm'
    cd -
fi

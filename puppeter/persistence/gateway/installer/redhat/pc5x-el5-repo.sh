#!/usr/bin/env bash
set +e
if ! rpm -q puppet5-release; then
    set -e
    cd /tmp
    wget 'https://yum.puppetlabs.com/puppet5-release-@{abbr}-@{major}.noarch.rpm'
    rpm -Uvh 'puppet5-release-@{abbr}-@{major}.noarch.rpm'
    rm 'puppet5-release-@{abbr}-@{major}.noarch.rpm'
    cd -
fi

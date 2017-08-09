#!/usr/bin/env bash
set +e
if ! rpm -q puppet5-release; then
    set -e
    rpm -Uvh 'https://yum.puppetlabs.com/puppet5-release-@{abbr}-@{major}.noarch.rpm'
fi

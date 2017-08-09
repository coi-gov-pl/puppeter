#!/usr/bin/env bash
set +e
if ! dpkg -l 'puppet5-release' | grep -q ii; then
    set -e
    cd /tmp
    wget 'https://apt.puppetlabs.com/puppet5-release-@{codename}.deb'
    dpkg -i 'puppet5-release-@{codename}.deb'
    rm 'puppet5-release-@{codename}.deb'
    cd -
    apt-get update
fi

#!/usr/bin/env bash
set +e
if ! dpkg -l 'puppetlabs-release' | grep -q ii; then
    set -e
    cd /tmp
    wget 'https://apt.puppetlabs.com/puppetlabs-release-@{codename}.deb'
    dpkg -i 'puppetlabs-release-@{codename}.deb'
    rm 'puppetlabs-release-@{codename}.deb'
    cd -
    apt-get update
fi

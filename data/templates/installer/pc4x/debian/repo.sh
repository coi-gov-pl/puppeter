#!/usr/bin/env bash

set -x
set +e

if ! dpkg -l 'puppetlabs-release-pc1' | grep -q ii; then
    set -e
    cd /tmp
    wget "https://apt.puppetlabs.com/puppetlabs-release-pc1-@{codename}.deb"
    sudo dpkg -i "puppetlabs-release-pc1-@{codename}.deb"
    rm "puppetlabs-release-pc1-@{codename}.deb"
    sudo apt-get update
fi

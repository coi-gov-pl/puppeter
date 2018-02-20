#!/usr/bin/env bash
set +e
if ! rpm -q epel-release; then
    set -e
    rpm -Uvh 'https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm'
fi
set -e

#!/usr/bin/env bash
function getLastAptGetUpdate() {
    local aptDate="$(stat -c %Y '/var/cache/apt')"
    local nowDate="$(date +'%s')"

    echo $((nowDate - aptDate))
}
set +xe
if [[ "$(getLastAptGetUpdate)" -gt '@{interval}' ]]; then
    set -xe
    apt-get update -m
fi
set -xe

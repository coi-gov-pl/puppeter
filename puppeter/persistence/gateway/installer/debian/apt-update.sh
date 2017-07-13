#!/usr/bin/env bash
function getLastAptGetUpdate() {
    local aptDate="$(stat -c %Y '/var/cache/apt')"
    local nowDate="$(date +'%s')"

    echo $((nowDate - aptDate))
}
if [[ "$(getLastAptGetUpdate)" -gt '@{interval}' ]]; then
    apt-get update -m
fi

#!/usr/bin/env bash
set +x
function reload_shell {
    set +e
    local files='~/.bash_profile ~/.bash_login ~/.profile'
    if [ -f /etc/profile ]; then
        . /etc/profile
    fi
    for file in ${files}; do
        if [ -f ${file} ]; then
            . ${file}
            break
        fi
    done
    set -e
}
set -x

#!/usr/bin/env bash

here=$(readlink -f ${BASH_SOURCE[0]})
root=$(dirname $(dirname $(dirname ${here})))

pip install -e ${root}

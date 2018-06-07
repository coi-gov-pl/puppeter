#!/usr/bin/env bash -e

here=$(readlink -f ${BASH_SOURCE[0]})
root=$(dirname $(dirname $(dirname ${here})))

set -x

LC_ALL=C pip install -e ${root}

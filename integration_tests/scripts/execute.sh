#!/usr/bin/env bash -e

set -x
puppeter --answers $1 | tee /tmp/puppeter-script.sh
chmod +x /tmp/puppeter-script.sh
set +x

/tmp/puppeter-script.sh

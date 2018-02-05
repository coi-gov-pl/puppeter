#!/usr/bin/env bash -e

puppeter --answers $1 | tee /tmp/puppeter-script.sh
chmod +x /tmp/puppeter-script.sh

/tmp/puppeter-script.sh

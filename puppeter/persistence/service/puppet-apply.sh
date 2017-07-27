#!/usr/bin/env bash

set +x
cat > @{tmpfilename} << EOF
@{pp}
EOF
set -x
puppet apply --show_diff @{tmpfilename}
rm -f @{tmpfilename}


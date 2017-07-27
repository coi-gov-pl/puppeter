#!/usr/bin/env bash
set +x
cat << 'EOF' > @{tmpfilename}.pp
@{pp}
EOF
set -x
puppet apply --show_diff @{tmpfilename}.pp
rm -f @{tmpfilename}.pp

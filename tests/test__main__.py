import re

import pytest

from tests.helpers.commandline import captured_output


def test_usage_printout():
    from puppeter import __main__

    with pytest.raises(SystemExit) as sysexit:
        with captured_output() as (out, err):
            __main__.main(['puppeter', '--help'])

    stdout = out.getvalue().strip()
    stderr = err.getvalue().strip()
    assert sysexit.value.code == 0
    assert stdout == ''
    assert re.compile('Puppeter', re.MULTILINE).search(stderr)
    assert re.compile('--answers FILE, -a FILE', re.MULTILINE).search(stderr)
    assert re.compile('--execute, -e', re.MULTILINE).search(stderr)

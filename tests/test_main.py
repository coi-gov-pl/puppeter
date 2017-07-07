from puppeter.main import main
import puppeter
import pytest
import re
from tests.helpers.commandline import captured_output


def test_usage_printout():
    with pytest.raises(SystemExit) as sysexit:
        with captured_output() as (out, err):
            main(['puppeter', '--help'])

    stdout = out.getvalue().strip()
    stderr = err.getvalue().strip()
    assert sysexit.value.code == 0
    assert stdout == ''
    assert re.compile('Puppeter', re.MULTILINE).search(stderr)
    assert re.compile('--answers FILE, -a FILE', re.MULTILINE).search(stderr)
    assert re.compile('--execute, -e', re.MULTILINE).search(stderr)


def test_version():
    with pytest.raises(SystemExit) as sysexit:
        with captured_output() as (out, err):
            main(['puppeter', '--version'])

    stdout = out.getvalue().strip()
    stderr = err.getvalue().strip()
    assert sysexit.value.code == 0
    assert stderr == ''
    assert stdout == ('puppeter %s' % puppeter.__version__)

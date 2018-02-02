import pytest
from os.path import dirname, join

puppeter_source = dirname(dirname(__file__))
remote_dir = '/usr/src/puppeter-source'


@pytest.fixture(scope='session')
def sut():
    """System Under Test"""
    return join('debian', 'ubuntu', '1604')


def test_simple_pc4x_on_ubuntu_1604(phial, capsys):
    with capsys.disabled():
        phial.scp(puppeter_source, remote_dir)
        status = __script(phial, 'install-develop.sh')
        assert status == 0

        answers = '%s/integration_tests/answers/simple-pc4x.yml' % remote_dir
        status = __script(phial, 'execute.sh', answers)
        assert status == 0

        assert phial.exec("bash -lc 'puppet --version | egrep \"^4\.[0-9]+\.[0-9]+$\"'") == 0


def __script(phial, script, arg=''):
    command = 'bash -xe %s/integration_tests/scripts/%s %s' % (remote_dir, script, arg)
    return phial.exec(command.strip())



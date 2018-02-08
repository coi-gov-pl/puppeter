import pytest
from os.path import join

from integration_tests.acceptance import PuppeterAcceptance


@pytest.fixture
def sut():
    """System Under Test"""
    return join('redhat', 'centos-7')


def test_simple_pc3x_on_centos_7(phial, capsys):
    with capsys.disabled():
        acceptance = PuppeterAcceptance(phial)

        acceptance.install_puppeter()
        acceptance.run_puppeter('simple-pc3x.yml')

        exitcode, output, error = phial.exec('puppet --version', capture=True)
        assert exitcode == 0
        assert error == ''
        assert PuppeterAcceptance.PUPPET_VER_3.match(output) is not None, output


def test_simple_pc4x_on_centos_7(phial, capsys):
    with capsys.disabled():
        acceptance = PuppeterAcceptance(phial)

        acceptance.install_puppeter()
        acceptance.run_puppeter('simple-pc4x.yml')

        assert phial.exec("bash -lc 'puppet --version | egrep \"^4\.[0-9]+\.[0-9]+$\"'") == 0


def test_simple_pc5x_on_centos_7(phial, capsys):
    with capsys.disabled():
        acceptance = PuppeterAcceptance(phial)

        acceptance.install_puppeter()
        acceptance.run_puppeter('simple-pc5x.yml')

        assert phial.exec("bash -lc 'puppet --version | egrep \"^5\.[0-9]+\.[0-9]+$\"'") == 0

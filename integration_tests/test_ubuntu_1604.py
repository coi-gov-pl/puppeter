import pytest
from os.path import join

from integration_tests.acceptance import PuppeterAcceptance


@pytest.fixture
def sut():
    """System Under Test"""
    return join('debian', 'ubuntu', '1604')


def test_simple_pc3x_on_ubuntu_1604(phial, capsys):
    with capsys.disabled():
        acceptance = PuppeterAcceptance(phial)

        acceptance.install_puppeter()
        acceptance.run_puppeter('simple-pc3x.yml')

        assert phial.exec("bash -lc 'puppet --version | egrep \"^3\.[0-9]+\.[0-9]+$\"'") == 0


def test_simple_pc4x_on_ubuntu_1604(phial, capsys):
    with capsys.disabled():
        acceptance = PuppeterAcceptance(phial)

        acceptance.install_puppeter()
        acceptance.run_puppeter('simple-pc4x.yml')

        assert phial.exec("bash -lc 'puppet --version | egrep \"^4\.[0-9]+\.[0-9]+$\"'") == 0


def test_simple_pc5x_on_ubuntu_1604(phial, capsys):
    with capsys.disabled():
        acceptance = PuppeterAcceptance(phial)

        acceptance.install_puppeter()
        acceptance.run_puppeter('simple-pc5x.yml')

        assert phial.exec("bash -lc 'puppet --version | egrep \"^5\.[0-9]+\.[0-9]+$\"'") == 0

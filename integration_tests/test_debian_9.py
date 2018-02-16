import pytest
from os.path import join

from integration_tests.acceptance import PuppeterAcceptance


@pytest.fixture
def sut():
    """System Under Test"""
    return join('debian', 'debian-9')


@pytest.mark.debian9
def test_simple_pc4x_on_debian_9(phial, capsys, regex):
    with capsys.disabled():
        acceptance = PuppeterAcceptance(phial)

        acceptance.install_puppeter()
        acceptance.run_puppeter('simple-pc4x.yml')

        exitcode, output, error = phial.exec('puppet --version', capture=True)
        assert error == ''
        regex.pattern(PuppeterAcceptance.PUPPET_VER_4).matches(output)
        assert exitcode == 0


@pytest.mark.debian9
def test_simple_pc5x_on_debian_9(phial, capsys, regex):
    with capsys.disabled():
        acceptance = PuppeterAcceptance(phial)

        acceptance.install_puppeter()
        acceptance.run_puppeter('simple-pc5x.yml')

        exitcode, output, error = phial.exec('puppet --version', capture=True)
        assert error == ''
        regex.pattern(PuppeterAcceptance.PUPPET_VER_5).matches(output)
        assert exitcode == 0

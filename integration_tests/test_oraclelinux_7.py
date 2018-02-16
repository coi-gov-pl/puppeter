import pytest
from os.path import join

from integration_tests.acceptance import PuppeterAcceptance


@pytest.fixture
def sut():
    """System Under Test"""
    return join('redhat', 'oraclelinux-7')


@pytest.mark.oraclelinux7
def test_simple_pc3x_on_oraclelinux_7(phial, capsys, regex):
    with capsys.disabled():
        acceptance = PuppeterAcceptance(phial)

        acceptance.install_puppeter()
        acceptance.run_puppeter('simple-pc3x.yml')

        exitcode, output, error = phial.exec('puppet --version', capture=True)
        assert error == ''
        regex.pattern(PuppeterAcceptance.PUPPET_VER_3).matches(output)
        assert exitcode == 0


@pytest.mark.oraclelinux7
def test_simple_pc4x_on_oraclelinux_7(phial, capsys, regex):
    with capsys.disabled():
        acceptance = PuppeterAcceptance(phial)

        acceptance.install_puppeter()
        acceptance.run_puppeter('simple-pc4x.yml')

        exitcode, output, error = phial.exec('puppet --version', capture=True)
        assert error == ''
        regex.pattern(PuppeterAcceptance.PUPPET_VER_4).matches(output)
        assert exitcode == 0


@pytest.mark.oraclelinux7
def test_simple_pc5x_on_oraclelinux_7(phial, capsys, regex):
    with capsys.disabled():
        acceptance = PuppeterAcceptance(phial)

        acceptance.install_puppeter()
        acceptance.run_puppeter('simple-pc5x.yml')

        exitcode, output, error = phial.exec('puppet --version', capture=True)
        assert error == ''
        regex.pattern(PuppeterAcceptance.PUPPET_VER_5).matches(output)
        assert exitcode == 0

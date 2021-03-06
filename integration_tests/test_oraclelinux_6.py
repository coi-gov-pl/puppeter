import pytest
from os.path import join

from integration_tests.acceptance import PuppeterAcceptance


@pytest.fixture
def sut():
    """System Under Test"""
    return join('redhat', 'oraclelinux-6')


@pytest.mark.oraclelinux6
def test_agent_pc3x_on_oraclelinux_6(phial, capsys, regex):
    with capsys.disabled():
        acceptance = PuppeterAcceptance(phial)

        acceptance.install_puppeter()
        acceptance.run_puppeter('agent-pc3x.yml')

        exitcode, output, error = phial.exec('puppet --version', capture=True)
        assert error == ''
        regex.pattern(PuppeterAcceptance.PUPPET_VER_3).matches(output)
        assert exitcode == 0


@pytest.mark.oraclelinux6
def test_agent_pc4x_on_oraclelinux_6(phial, capsys, regex):
    with capsys.disabled():
        acceptance = PuppeterAcceptance(phial)

        acceptance.install_puppeter()
        acceptance.run_puppeter('agent-pc4x.yml')

        exitcode, output, error = phial.exec('puppet --version', capture=True)
        assert error == ''
        regex.pattern(PuppeterAcceptance.PUPPET_VER_4).matches(output)
        assert exitcode == 0


@pytest.mark.oraclelinux6
def test_agent_pc5x_on_oraclelinux_6(phial, capsys, regex):
    with capsys.disabled():
        acceptance = PuppeterAcceptance(phial)

        acceptance.install_puppeter()
        acceptance.run_puppeter('agent-pc5x.yml')

        exitcode, output, error = phial.exec('puppet --version', capture=True)
        assert error == ''
        regex.pattern(PuppeterAcceptance.PUPPET_VER_5).matches(output)
        assert exitcode == 0

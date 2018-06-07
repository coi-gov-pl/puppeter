import re
import pytest
from os.path import join

from integration_tests.acceptance import PuppeterAcceptance


@pytest.fixture
def sut():
    """System Under Test"""
    return join('debian', 'ubuntu-1604')


@pytest.mark.ubuntu1604
def test_puppeter_develop_install_on_ubuntu_1604_with_invalid_locale(phial, capsys, regex):
    with capsys.disabled():
        acceptance = PuppeterAcceptance(phial)
        pattern = re.compile('^puppeter \d+\.\d+\.\d+(?:\.[a-z0-9]+)?$')

        phial.exec('echo "export LC_ALL=mn-Mong-CN.UTF-8" >> /etc/profile.d/mandarin.sh')
        acceptance.install_puppeter()
        phial.exec('rm -vf /etc/profile.d/mandarin.sh')

        exitcode, output, error = phial.exec('puppeter --version', capture=True)
        assert error == ''
        regex.pattern(pattern).matches(output)
        assert exitcode == 0


@pytest.mark.ubuntu1604
def test_puppeter_production_install_on_ubuntu_1604_with_invalid_locale(phial, capsys, regex):
    with capsys.disabled():
        pattern = re.compile('^puppeter \d+\.\d+\.\d+(?:\.[a-z0-9]+)?$')

        phial.exec('echo "export LC_ALL=mn-Mong-CN.UTF-8" >> /etc/profile.d/mandarin.sh')
        exitcode, output, error = phial.exec('/puppeter-setup.sh')
        assert exitcode == 0
        phial.exec('rm -vf /etc/profile.d/mandarin.sh')

        exitcode, output, error = phial.exec('puppeter --version', capture=True)
        assert error == ''
        regex.pattern(pattern).matches(output)
        assert exitcode == 0


@pytest.mark.ubuntu1604
def test_agent_system_on_ubuntu_1604(phial, capsys, regex):
    with capsys.disabled():
        acceptance = PuppeterAcceptance(phial)

        acceptance.install_puppeter()
        acceptance.run_puppeter('agent-system.yml')

        exitcode, output, error = phial.exec('puppet --version', capture=True)
        assert error == ''
        regex.pattern(PuppeterAcceptance.PUPPET_VER_3).matches(output)
        assert exitcode == 0


@pytest.mark.ubuntu1604
def test_agent_pc4x_on_ubuntu_1604(phial, capsys, regex):
    with capsys.disabled():
        acceptance = PuppeterAcceptance(phial)

        acceptance.install_puppeter()
        acceptance.run_puppeter('agent-pc4x.yml')

        exitcode, output, error = phial.exec('puppet --version', capture=True)
        assert error == ''
        regex.pattern(PuppeterAcceptance.PUPPET_VER_4).matches(output)
        assert exitcode == 0


@pytest.mark.ubuntu1604
def test_agent_pc5x_on_ubuntu_1604(phial, capsys, regex):
    with capsys.disabled():
        acceptance = PuppeterAcceptance(phial)

        acceptance.install_puppeter()
        acceptance.run_puppeter('agent-pc5x.yml')

        exitcode, output, error = phial.exec('puppet --version', capture=True)
        assert error == ''
        regex.pattern(PuppeterAcceptance.PUPPET_VER_5).matches(output)
        assert exitcode == 0

from puppeter import container
from puppeter.domain.model import Collection5xInstaller
from puppeter.domain.model.osfacts import OsFamily, OperatingSystem, OperatingSystemRelease
from puppeter.persistence.gateway.installer.redhat import RedHatPC5xConfigurer
from tests.domain.mock_facter import MockFacter


def test_pc5x():
    # given
    MockFacter.set_fact(OperatingSystem, OperatingSystem.RedHat)
    MockFacter.set_fact(OperatingSystemRelease, OperatingSystemRelease('7.3.11'))
    installer = Collection5xInstaller()
    installer.read_raw_options({'mode': 'Server'})
    configurer = RedHatPC5xConfigurer(installer=installer)

    # when
    commands = configurer.produce_commands()
    commands = list(map(lambda cmd: cmd.strip(), commands))

    # then
    assert 'yum install -y wget' not in commands
    assert "rpm -Uvh 'https://yum.puppetlabs.com/puppet5-release-el-7.noarch.rpm'" in commands
    assert 'yum install -y puppet-agent' in commands
    assert 'puppet resource package puppetserver ensure=installed' in commands


def setup_function():
    MockFacter.set_fact(OsFamily, OsFamily.RedHat)
    container.initialize()


def teardown_function():
    MockFacter.reset_facts()

from puppeter import container
from puppeter.domain.model import SystemInstaller
from puppeter.domain.model.osfacts import OsFamily, OperatingSystem, OperatingSystemRelease
from puppeter.persistence.gateway.installer.redhat import RedHatSystemConfigurer
from tests.domain.mock_facter import MockFacter


def test_system_redhat():
    # given
    MockFacter.set_fact(OperatingSystem, OperatingSystem.RedHat)
    MockFacter.set_fact(OperatingSystemRelease, OperatingSystemRelease('7.3.11'))
    installer = SystemInstaller()
    installer.read_raw_options({'mode': 'Server'})
    configurer = RedHatSystemConfigurer(installer=installer)

    # when
    commands = configurer.produce_commands()
    commands = list(map(lambda cmd: cmd.strip(), commands))

    # then
    assert 'yum install -y wget' not in commands
    assert "rpm -Uvh 'https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm'" in commands
    assert 'yum install -y puppet' in commands
    assert 'puppet resource package puppetmaster ensure=installed' in commands


def setup_function():
    MockFacter.set_fact(OsFamily, OsFamily.RedHat)
    container.initialize()


def teardown_function():
    MockFacter.reset_facts()

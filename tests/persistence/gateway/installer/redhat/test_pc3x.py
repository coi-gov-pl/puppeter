from puppeter import container
from puppeter.domain.model import Collection3xInstaller
from puppeter.domain.model.osfacts import OperatingSystem, OsFamily, OperatingSystemRelease
from puppeter.persistence.gateway.installer.redhat import RedHatPC3xConfigurer
from tests.domain.mock_facter import MockFacter


def test_pc3x_centos_5():
    # given
    MockFacter.set_fact(OperatingSystem, OperatingSystem.CentOS)
    MockFacter.set_fact(OperatingSystemRelease, OperatingSystemRelease('5.4'))
    installer = Collection3xInstaller()
    installer.read_raw_options({'mode': 'Server'})
    configurer = RedHatPC3xConfigurer(installer=installer)

    # when
    commands = configurer.produce_commands()
    commands = list(map(lambda cmd: cmd.strip(), commands))

    # then
    assert 'yum install -y wget' in commands
    assert "wget 'https://yum.puppetlabs.com/puppetlabs-release-el-5.noarch.rpm'" in commands
    assert 'yum install -y puppet' in commands
    assert 'puppet resource package puppetmaster ensure=installed' in commands


def test_pc3x_scientific_7():
    # given
    MockFacter.set_fact(OperatingSystem, OperatingSystem.Scientific)
    MockFacter.set_fact(OperatingSystemRelease, OperatingSystemRelease('7.3'))
    installer = Collection3xInstaller()
    installer.read_raw_options({'mode': 'Server'})
    configurer = RedHatPC3xConfigurer(installer=installer)

    # when
    commands = configurer.produce_commands()
    commands = list(map(lambda cmd: cmd.strip(), commands))

    # then
    assert 'yum install -y wget' not in commands
    assert "rpm -Uvh 'https://yum.puppetlabs.com/puppetlabs-release-el-7.noarch.rpm'" in commands
    assert 'yum install -y puppet' in commands
    assert 'puppet resource package puppetmaster ensure=installed' in commands


def test_pc3x_fedora_25():
    # given
    MockFacter.set_fact(OperatingSystem, OperatingSystem.Fedora)
    MockFacter.set_fact(OperatingSystemRelease, OperatingSystemRelease('25.1'))
    installer = Collection3xInstaller()
    installer.read_raw_options({'mode': 'Agent'})
    configurer = RedHatPC3xConfigurer(installer=installer)

    # when
    commands = configurer.produce_commands()
    commands = list(map(lambda cmd: cmd.strip(), commands))

    # then
    assert 'yum install -y wget' not in commands
    assert "rpm -Uvh 'https://yum.puppetlabs.com/puppetlabs-release-fedora-25.noarch.rpm'" in commands
    assert 'yum install -y puppet' in commands
    assert 'puppet resource package puppetmaster ensure=installed' not in commands


def setup_function():
    MockFacter.set_fact(OsFamily, OsFamily.RedHat)
    container.initialize()


def teardown_function():
    MockFacter.reset_facts()

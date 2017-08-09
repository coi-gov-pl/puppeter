from puppeter import container
from puppeter.domain.model import Collection4xInstaller
from puppeter.domain.model.osfacts import OsFamily, OperatingSystem, OperatingSystemRelease
from puppeter.persistence.gateway.installer.redhat import RedHatPC4xConfigurer
from tests.domain.mock_facter import MockFacter


def test_pc4x_oraclelinux5():
    # given
    MockFacter.set_fact(OperatingSystem, OperatingSystem.OracleLinux)
    MockFacter.set_fact(OperatingSystemRelease, OperatingSystemRelease('5.11'))
    installer = Collection4xInstaller()
    installer.read_raw_options({'mode': 'Server'})
    configurer = RedHatPC4xConfigurer(installer=installer)

    # when
    commands = configurer.produce_commands()
    commands = list(map(lambda cmd: cmd.strip(), commands))

    # then
    assert 'yum install -y wget' in commands
    assert "wget 'https://yum.puppetlabs.com/puppetlabs-release-pc1-el-5.noarch.rpm'" in commands
    assert 'yum install -y puppet-agent' in commands
    assert 'puppet resource package puppetserver ensure=installed' in commands


def test_pc4x_rhel_6():
    # given
    MockFacter.set_fact(OperatingSystem, OperatingSystem.RedHat)
    MockFacter.set_fact(OperatingSystemRelease, OperatingSystemRelease('6.8'))
    installer = Collection4xInstaller()
    installer.read_raw_options({'mode': 'Agent'})
    configurer = RedHatPC4xConfigurer(installer=installer)

    # when
    commands = configurer.produce_commands()
    commands = list(map(lambda cmd: cmd.strip(), commands))

    # then
    assert 'yum install -y wget' not in commands
    assert "rpm -Uvh 'https://yum.puppetlabs.com/puppetlabs-release-pc1-el-6.noarch.rpm'" in commands
    assert 'yum install -y puppet-agent' in commands
    assert 'puppet resource package puppetserver ensure=installed' not in commands


def setup_function():
    MockFacter.set_fact(OsFamily, OsFamily.RedHat)
    container.initialize()


def teardown_function():
    MockFacter.reset_facts()

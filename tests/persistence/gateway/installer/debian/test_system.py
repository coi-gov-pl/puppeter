from puppeter import container
from puppeter.domain.model import SystemInstaller
from puppeter.domain.model.osfacts import OperatingSystemCodename
from puppeter.persistence.gateway.installer.debian import DebianSystemConfigurer
from tests.domain.mock_facter import MockFacter


def test_system():
    # given
    installer = SystemInstaller()
    installer.read_raw_options({'mode': 'Server'})
    configurer = DebianSystemConfigurer(installer=installer)

    # when
    commands = configurer.produce_commands()
    commands = list(map(lambda cmd: cmd.strip(), commands))

    # then
    assert 'apt-get update -m' in commands
    assert 'apt-get install -y wget' not in commands
    assert 'apt-get install -y puppet-common' in commands
    assert 'puppet resource package puppetmaster ensure=installed' in commands


def setup_function():
    MockFacter.set_fact(OperatingSystemCodename, OperatingSystemCodename('xenial'))
    container.initialize()


def teardown_function():
    MockFacter.reset_facts()

from puppeter import container
from puppeter.domain.model import Collection3xInstaller
from puppeter.domain.model.osfacts import OperatingSystemCodename
from puppeter.persistence.gateway.installer.debian import DebianPC3xConfigurer
from tests.domain.mock_facter import MockFacter


def test_pc3x():
    # given
    installer = Collection3xInstaller()
    installer.read_raw_options({'mode': 'Server'})
    configurer = DebianPC3xConfigurer(installer=installer)

    # when
    commands = configurer.produce_commands()
    commands = list(map(lambda cmd: cmd.strip(), commands))

    # then
    assert 'apt-get update -m' in commands
    assert 'apt-get install -y wget' in commands
    assert "wget 'https://apt.puppetlabs.com/puppetlabs-release-trusty.deb'" in commands
    assert 'apt-get install -y puppet' in commands
    assert 'puppet resource package puppetmaster ensure=installed' in commands


def setup_function():
    MockFacter.set_fact(OperatingSystemCodename, OperatingSystemCodename('trusty'))
    container.initialize()


def teardown_function():
    MockFacter.reset_facts()

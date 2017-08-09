from puppeter import container
from puppeter.domain.model import Collection4xInstaller
from puppeter.domain.model.osfacts import OperatingSystemCodename
from puppeter.persistence.gateway.installer.debian import DebianPC4xConfigurer
from tests.domain.mock_facter import MockFacter


def test_pc4x():
    # given
    installer = Collection4xInstaller()
    installer.read_raw_options({'mode': 'Server'})
    configurer = DebianPC4xConfigurer(installer=installer)

    # when
    commands = configurer.produce_commands()
    commands = list(map(lambda cmd: cmd.strip(), commands))

    # then
    assert 'apt-get update -m' in commands
    assert 'apt-get install -y wget' in commands
    assert "wget 'https://apt.puppetlabs.com/puppetlabs-release-pc1-precise.deb'" in commands
    assert 'apt-get install -y puppet-agent' in commands
    assert 'puppet resource package puppetserver ensure=installed' in commands


def setup_function():
    MockFacter.set_fact(OperatingSystemCodename, OperatingSystemCodename('precise'))
    container.initialize()


def teardown_function():
    MockFacter.reset_facts()

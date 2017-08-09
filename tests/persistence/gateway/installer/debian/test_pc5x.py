from puppeter import container
from puppeter.domain.model import Collection5xInstaller
from puppeter.domain.model.osfacts import OperatingSystemCodename
from puppeter.persistence.gateway.installer.debian import DebianPC5xConfigurer
from tests.domain.mock_facter import MockFacter


def test_pc5x():
    # given
    installer = Collection5xInstaller()
    installer.read_raw_options({'mode': 'Server'})
    configurer = DebianPC5xConfigurer(installer=installer)

    # when
    commands = configurer.produce_commands()
    commands = list(map(lambda cmd: cmd.strip(), commands))

    # then
    assert 'if [[ "$(getLastAptGetUpdate)" -gt \'86400\' ]]; then' in commands
    assert 'apt-get update -m' in commands
    assert 'apt-get install -y wget' in commands
    assert "wget 'https://apt.puppetlabs.com/puppet5-release-xenial.deb'" in commands
    assert 'apt-get install -y puppet-agent' in commands
    assert 'puppet resource package puppetserver ensure=installed' in commands


def setup_function():
    MockFacter.set_fact(OperatingSystemCodename, OperatingSystemCodename('xenial'))
    container.initialize()


def teardown_function():
    MockFacter.reset_facts()

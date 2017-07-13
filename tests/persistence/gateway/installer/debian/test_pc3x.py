from puppeter.domain.model import Collection3xInstaller
from puppeter.persistence.gateway.installer.debian import DebianPC3xConfigurer


def test_pc3x():
    # given
    installer = Collection3xInstaller()
    installer.read_raw_options({'mode': 'Server'})
    configurer = DebianPC3xConfigurer(installer=installer)

    # when
    commands = configurer.produce_commands()

    # then
    assert '# Part 1: apt system update' in commands
    assert 'puppet resource package puppetmaster ensure=installed' in commands

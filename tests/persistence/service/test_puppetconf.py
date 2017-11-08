from puppeter.domain.model import Collection4xInstaller
from puppeter.persistence.service import PuppetConfConfigurer


def test_puppetconf():
    # given
    installer = Collection4xInstaller()
    installer.read_raw_options({
        'mode': 'Agent',
        'puppet.conf': {
            'main': {
                'server': 'puppet.acme.internal'
            },
            'agent': {
                'noop': True
            }
        }
    })
    configurer = PuppetConfConfigurer(installer)

    # when
    commands = configurer.produce_commands()

    # then
    assert configurer.bean_name() == 'puppet.conf'
    assert configurer.order() == 900
    assert found("set main/server 'puppet.acme.internal'").inside(commands)
    assert found("set agent/noop true").inside(commands)


def found(st):
    class Found:
        def __init__(self):
            pass

        @staticmethod
        def inside(lst):
            return any(st in s for s in lst)
    return Found

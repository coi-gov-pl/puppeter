from abc import ABCMeta

from six import with_metaclass

from puppeter import container
from puppeter.container import Named
from puppeter.domain.gateway.installer import InstallerGateway
from puppeter.domain.model.configurer import Configurer


@Named('gem')
class RubyGemConfigurer(Configurer):
    def __init__(self, installer):
        self.installer = installer

    def produce_commands(self):
        raise NotImplementedError('Not yet implemented!')


class LinuxInstallerGateway(with_metaclass(ABCMeta, InstallerGateway)):
    def _puppet_services(self, installer):
        return tuple(container.get_all_with_name_starting_with(Configurer,
                                                               'puppet.service',
                                                               installer=installer))

    def _puppet_cert_issue(self, installer):
        return tuple(container.get_all_with_name_starting_with(Configurer,
                                                               'puppet.cert.issue',
                                                               installer=installer))

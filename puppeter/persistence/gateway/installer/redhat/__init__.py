from puppeter import container
from puppeter.container import Named
from puppeter.domain.model.configurer import Configurer
from puppeter.domain.gateway.installer import InstallerGateway
from puppeter.persistence.gateway.installer.redhat.pc3x import PC3xConfigurer
from puppeter.persistence.gateway.installer.redhat.pc4x import PC4xConfigurer
from puppeter.persistence.gateway.installer.redhat.pc5x import PC5xConfigurer


@Named('redhat')
class RedHatInstallerGateway(InstallerGateway):

    def _provide_configurer(self, installer):
        name = installer.bean_name()
        if name == 'gem':
            return container.get_named(Configurer, 'gem', installer=installer)
        name += '-redhat'
        return container.get_named(Configurer, name, installer=installer)


container.bind(InstallerGateway, RedHatInstallerGateway)
container.bind(Configurer, PC3xConfigurer)
container.bind(Configurer, PC4xConfigurer)
container.bind(Configurer, PC5xConfigurer)

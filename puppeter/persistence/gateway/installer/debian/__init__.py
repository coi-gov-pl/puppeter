from puppeter import container
from puppeter.container import Named
from puppeter.domain.model.configurer import Configurer
from puppeter.domain.gateway.installer import InstallerGateway
from puppeter.persistence.gateway.installer.debian.pc3x import PC3xConfigurer
from puppeter.persistence.gateway.installer.debian.pc4x import PC4xConfigurer
from puppeter.persistence.gateway.installer.debian.pc5x import PC5xConfigurer


@Named('debian')
class DebianInstallerGateway(InstallerGateway):

    def _provide_configurer(self, installer):
        name = installer.bean_name()
        if name == 'gem':
            return container.get_named(Configurer, 'gem', installer=installer)
        name += '-debian'
        return container.get_named(Configurer, name, installer=installer)


container.bind(InstallerGateway, DebianInstallerGateway)
container.bind(Configurer, PC3xConfigurer)
container.bind(Configurer, PC4xConfigurer)
container.bind(Configurer, PC5xConfigurer)

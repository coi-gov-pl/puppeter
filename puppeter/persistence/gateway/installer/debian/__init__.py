from puppeter import container
from puppeter.container import Named
from puppeter.domain.model.configurer import Configurer
from puppeter.domain.gateway.installer import InstallerGateway
from puppeter.persistence.gateway.installer.debian.pc3x import DebianPC3xConfigurer
from puppeter.persistence.gateway.installer.debian.pc4x import DebianPC4xConfigurer
from puppeter.persistence.gateway.installer.debian.pc5x import DebianPC5xConfigurer
from puppeter.persistence.gateway.installer.linux import LinuxInstallerGateway


@Named('debian')
class DebianInstallerGateway(LinuxInstallerGateway):

    def _provide_install_configurers(self, installer):
        return tuple([self.__provide_install_configurer(installer)])

    @staticmethod
    def __provide_install_configurer(installer):
        name = installer.bean_name()
        if name == 'gem':
            return container.get_named(Configurer, 'gem', installer=installer)
        name += '-debian'
        return container.get_named(Configurer, name, installer=installer)


container.bind(InstallerGateway, DebianInstallerGateway)
container.bind(Configurer, DebianPC3xConfigurer)
container.bind(Configurer, DebianPC4xConfigurer)
container.bind(Configurer, DebianPC5xConfigurer)

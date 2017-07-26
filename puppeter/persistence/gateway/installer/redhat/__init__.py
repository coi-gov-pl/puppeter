from puppeter import container
from puppeter.container import Named
from puppeter.domain.model.configurer import Configurer
from puppeter.domain.gateway.installer import InstallerGateway
from puppeter.persistence.gateway.installer.linux import LinuxInstallerGateway
from puppeter.persistence.gateway.installer.redhat.pc3x import RedHatPC3xConfigurer
from puppeter.persistence.gateway.installer.redhat.pc4x import RedHatPC4xConfigurer
from puppeter.persistence.gateway.installer.redhat.pc5x import RedHatPC5xConfigurer


@Named('redhat')
class RedHatInstallerGateway(LinuxInstallerGateway):

    def _provide_install_configurers(self, installer):
        configurers = [self.__provide_install_configurer(installer)]
        return tuple(configurers)

    def __provide_install_configurer(self, installer):
        name = installer.bean_name()
        if name == 'gem':
            return container.get_named(Configurer, 'gem', installer=installer)
        name += '-redhat'
        return container.get_named(Configurer, name, installer=installer)


container.bind(InstallerGateway, RedHatInstallerGateway)
container.bind(Configurer, RedHatPC3xConfigurer)
container.bind(Configurer, RedHatPC4xConfigurer)
container.bind(Configurer, RedHatPC5xConfigurer)

from typing import Sequence

from puppeter.container import Named
from puppeter.domain.facter import Facter
from puppeter.domain.model import Installer
from puppeter.domain.model.configurer import Configurer
from puppeter.domain.model.installer import Mode, After4xCollectionInstaller
from puppeter.domain.model.ordered import Order
from puppeter.domain.model.osfacts import Docker


@Named('puppet.service.puppet-service')
@Order(1000)
class PuppetServerServiceStarterConfigurer(Configurer):
    def __init__(self, installer):
        self.__installer = installer  # type: Installer

    def produce_commands(self):
        if self.__installer.mode() == Mode.Agent:
            return []
        if self.__installer.is_after_4x():
            servicename = 'puppetserver'
        else:
            servicename = 'puppetmaster'
        enable = 'false' if Facter.get(Docker) else 'true'
        collector = self._collector()
        desc = 'Starting Puppet server service ({servicename})'.format(servicename=servicename)
        mapping = dict(servicename=servicename, enable=enable)
        collector.collect_from_template(desc, 'puppetserver.sh', mapping)
        return collector.lines()


@Named('puppet.service.puppetserver-memory')
@Order(900)
class PuppetServerServiceMemoryConfigurer(Configurer):
    def __init__(self, installer):
        self.__installer = installer  # type: Installer

    def produce_commands(self):
        install = self.__installer
        if not (isinstance(install, After4xCollectionInstaller)
                and install.mode() == Mode.Server
                and install.is_after_4x()):
            # Only for Java written PuppetServer
            return []
        return self.__produce_commands(install)

    def __produce_commands(self, install):
        # type: (After4xCollectionInstaller) -> Sequence[str]
        mem = install.puppetserver_jvm_memory()
        if not mem.is_set():
            return []


from typing import Sequence, MutableSequence

from puppeter.container import Named
from puppeter.domain.facter import Facter
from puppeter.domain.model import Installer
from puppeter.domain.model.configurer import Configurer, ScriptFormat
from puppeter.domain.model.installer import Mode, After4xCollectionInstaller
from puppeter.domain.model.javafacts import JavaVersion
from puppeter.domain.model.ordered import Order
from puppeter.domain.model.osfacts import Docker


@Named('puppet.service.puppetserver-service')
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
        enable = 'true' if Facter.get(Docker) is not Docker.YES else 'false'
        collector = self._collector()
        desc = 'Starting Puppet server service ({servicename})'.format(servicename=servicename)
        mapping = dict(servicename=servicename, enable=enable)
        collector.collect_from_template(desc, 'puppetserver.sh', mapping)
        return collector.lines()


@Named('puppet.service.puppetserver-jvmargs')
@Order(900)
class PuppetServerJvmArgsConfigurer(Configurer):
    def __init__(self, installer):
        self.__installer = installer  # type: Installer

    def produce_commands(self):
        install = self.__installer
        if not (isinstance(install, After4xCollectionInstaller) and
                install.mode() == Mode.Server and
                install.is_after_4x()):
            # Only for Java written PuppetServer
            return []
        return self.__produce_commands(install)

    def __produce_commands(self, install):
        # type: (After4xCollectionInstaller) -> Sequence[str]
        args = []  # type: MutableSequence[str]
        mem = install.puppetserver_jvm_memory()
        jvmargs = install.puppetserver_jvm_args()
        if mem.is_set():
            if mem.heap_minimum() is not None:
                args.append('-Xms{xms}'.format(xms=mem.heap_minimum()))
            if mem.heap_maximum() is not None:
                args.append('-Xmx{xmx}'.format(xmx=mem.heap_maximum()))
            java_version = Facter.get(JavaVersion)
            metaspace_arg = self.__get_metaspace_arg(java_version)
            if java_version.has_permgen_space() and mem.metaspace_maximum() is None:
                args.append(metaspace_arg.format(mspace='256m'))
            elif mem.metaspace_maximum() is not None:
                args.append(metaspace_arg.format(mspace=mem.metaspace_maximum()))
        if jvmargs.are_set():
            args.extend(jvmargs)
        args_as_str = ' '.join(args)
        collector = self._collector()
        mapping = dict(jvmargs=args_as_str)
        collector.collect_from_template('Configuring PuppetServer JVM Args',
                                        'puppetserver-jvmargs.pp',
                                        mapping,
                                        format=ScriptFormat.PUPPET)
        return collector.lines()

    def __get_metaspace_arg(self, java_version):
        # type: (JavaVersion) -> str
        return '-XX:MaxPermSize={mspace}' if java_version.has_permgen_space() else '-XX:MaxMetaspaceSize={mspace}'

from puppeter import container
from puppeter.domain.model.configurer import CommandsCollector, Configurer
from puppeter.domain.model.javafacts import JavaVersion
from puppeter.persistence.service.commandscollector import CommandsCollectorImpl
from puppeter.persistence.service.java import calculate_java_version
from puppeter.persistence.service.os import calculate_operatingsystem, \
    calculate_osfamily, calculate_osrelease, calculate_oscodename, calculate_docker
from puppeter.domain.facter import Facter
from puppeter.domain.model.osfacts import OperatingSystem, OsFamily, \
    OperatingSystemRelease, OperatingSystemCodename, Docker
from puppeter.persistence.service.puppetserver import PuppetServerServiceStarterConfigurer, \
    PuppetServerJvmArgsConfigurer

Facter.set(OperatingSystem, calculate_operatingsystem)
Facter.set(OsFamily, calculate_osfamily)
Facter.set(OperatingSystemRelease, calculate_osrelease)
Facter.set(OperatingSystemCodename, calculate_oscodename)
Facter.set(Docker, calculate_docker)

Facter.set(JavaVersion, calculate_java_version)

container.bind(CommandsCollector, CommandsCollectorImpl)
container.bind(Configurer, PuppetServerServiceStarterConfigurer)
container.bind(Configurer, PuppetServerJvmArgsConfigurer)

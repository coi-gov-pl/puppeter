import platform
from puppeter.domain.os import OsFamily, OperatingSystem
from puppeter.persistence.facter import Facter as __Facter

Facter = __Facter


def __calculate_operatingsystem():
    if platform.system() == 'Linux':
        dist = platform.linux_distribution()[0]
        return {
            'centos': OperatingSystem.CentOS,
            'oracle linux server': OperatingSystem.OracleLinux,
            'red hat enterprise linux server': OperatingSystem.RedHat,
            'scientific linux': OperatingSystem.Scientific,
            'debian': OperatingSystem.Debian,
            'ubuntu': OperatingSystem.Ubuntu,
            'opensuse': OperatingSystem.OpenSuse
        }.get(dist.lower().strip(), OperatingSystem.Unknown)
    return OperatingSystem.Unknown


def __calculate_osfamily():
    return {
        OperatingSystem.CentOS: OsFamily.RedHat,
        OperatingSystem.OracleLinux: OsFamily.RedHat,
        OperatingSystem.RedHat: OsFamily.RedHat,
        OperatingSystem.Scientific: OsFamily.RedHat,
        OperatingSystem.Debian: OsFamily.Debian,
        OperatingSystem.Ubuntu: OsFamily.Debian,
        OperatingSystem.OpenSuse: OsFamily.Suse
    }.get(__Facter.get(OperatingSystem), OsFamily.Unknown)


__Facter.set(OperatingSystem, __calculate_operatingsystem)
__Facter.set(OsFamily, __calculate_osfamily)

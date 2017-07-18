import platform

import distro

from puppeter.domain.facter import Facter
from puppeter.domain.model.osfacts import OsFamily, OperatingSystem, \
    OperatingSystemRelease, OperatingSystemCodename


def calculate_operatingsystem():
    if platform.system() == 'Linux':
        dist = distro.linux_distribution(full_distribution_name=False)[0]
        return {
            'fedora': OperatingSystem.Fedora,
            'centos': OperatingSystem.CentOS,
            'oracle linux server': OperatingSystem.OracleLinux,
            'red hat enterprise linux server': OperatingSystem.RedHat,
            'scientific linux': OperatingSystem.Scientific,
            'debian': OperatingSystem.Debian,
            'ubuntu': OperatingSystem.Ubuntu,
            'opensuse': OperatingSystem.OpenSuse
        }.get(dist.lower().strip(), OperatingSystem.Unknown)
    return OperatingSystem.Unknown


def calculate_osfamily():
    return {
        OperatingSystem.CentOS: OsFamily.RedHat,
        OperatingSystem.OracleLinux: OsFamily.RedHat,
        OperatingSystem.RedHat: OsFamily.RedHat,
        OperatingSystem.Scientific: OsFamily.RedHat,
        OperatingSystem.Debian: OsFamily.Debian,
        OperatingSystem.Ubuntu: OsFamily.Debian,
        OperatingSystem.OpenSuse: OsFamily.Suse
    }.get(Facter.get(OperatingSystem), OsFamily.Unknown)


def calculate_osrelease():
    if platform.system() == 'Linux':
        release = distro.linux_distribution(full_distribution_name=False)[1]
        return OperatingSystemRelease(release.strip())
    return None


def calculate_oscodename():
    if platform.system() == 'Linux':
        codename = distro.linux_distribution(full_distribution_name=False)[2]
        return OperatingSystemCodename(codename.strip().split(' ')[0].lower())
    return None

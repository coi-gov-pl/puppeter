from __future__ import absolute_import
import os
import distro
import platform
from typing import Sequence, Callable

import puppeter.settings
from puppeter.domain.facter import Facter
from puppeter.domain.model.osfacts import OsFamily, OperatingSystem, \
    OperatingSystemRelease, OperatingSystemCodename, Docker


def calculate_operatingsystem():
    if platform.system() == 'Linux':
        dist = distro.id()
        return {
            'fedora': OperatingSystem.Fedora,
            'centos': OperatingSystem.CentOS,
            'oracle': OperatingSystem.OracleLinux,
            'ol': OperatingSystem.OracleLinux,
            'rhel': OperatingSystem.RedHat,
            'scientific': OperatingSystem.Scientific,
            'debian': OperatingSystem.Debian,
            'ubuntu': OperatingSystem.Ubuntu,
            'sles': OperatingSystem.SLES,
            'opensuse': OperatingSystem.OpenSuse,
            'arch': OperatingSystem.ArchLinux
        }.get(dist, OperatingSystem.Unknown)
    return OperatingSystem.Unknown


def calculate_osfamily():
    return {
        OperatingSystem.CentOS: OsFamily.RedHat,
        OperatingSystem.OracleLinux: OsFamily.RedHat,
        OperatingSystem.RedHat: OsFamily.RedHat,
        OperatingSystem.Scientific: OsFamily.RedHat,
        OperatingSystem.Debian: OsFamily.Debian,
        OperatingSystem.Ubuntu: OsFamily.Debian,
        OperatingSystem.OpenSuse: OsFamily.Suse,
        OperatingSystem.SLES: OsFamily.Suse,
        OperatingSystem.ArchLinux: OsFamily.Arch
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


def calculate_docker():
    return Docker.YES if __calculate_docker_bool() else Docker.NO


def __calculate_docker_bool():
    if platform.system() != 'Linux':
        return False
    path = '{chroot}proc/1/cgroup'.format(chroot=puppeter.settings.chroot)
    if not __is_readable(path):
        return False
    try:
        lines = open(path).read().splitlines()
        return __any(lines, lambda l: '/docker' in l.split(':')[2])
    except IOError:
        return False


def __is_readable(file):
    return os.path.isfile(file) and os.access(file, os.R_OK)


def __any(seq, predicate):
    # type: (Sequence, Callable[[str], bool]) -> bool
    return any((predicate(i) is True) for i in seq)

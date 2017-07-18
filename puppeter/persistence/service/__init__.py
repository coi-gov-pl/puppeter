from puppeter.persistence.service.os import calculate_operatingsystem, \
    calculate_osfamily, calculate_osrelease, calculate_oscodename
from puppeter.domain.facter import Facter
from puppeter.domain.model.osfacts import OperatingSystem, OsFamily,\
    OperatingSystemRelease, OperatingSystemCodename

Facter.set(OperatingSystem, calculate_operatingsystem)
Facter.set(OsFamily, calculate_osfamily)
Facter.set(OperatingSystemRelease, calculate_osrelease)
Facter.set(OperatingSystemCodename, calculate_oscodename)

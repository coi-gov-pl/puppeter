from enum import Enum

import re


class OsFamily(Enum):
    Unknown = 1
    RedHat = 2
    Debian = 3
    Suse = 4


class OperatingSystem(Enum):
    Unknown = 1
    RedHat = 2
    CentOS = 3
    Scientific = 4
    OracleLinux = 5
    Debian = 6
    Ubuntu = 7
    OpenSuse = 8


class OperatingSystemRelease(str):
    VERSION_RE = re.compile('^(\d+)(?:\.(\d+))*$')

    def __init__(self, version):
        super(OperatingSystemRelease, self).__init__()
        self.__version = str(version)

    def __str__(self):
        return self.__version

    def major(self):
        return self.VERSION_RE\
            .match(self)\
            .group(1)

    def minor(self):
        return self.VERSION_RE\
            .match(self)\
            .group(2)


class OperatingSystemCodename(str):
    def __init__(self, codename):
        super(OperatingSystemCodename, self).__init__()
        self.__codename = str(codename)

    def __str__(self):
        return self.__codename

from enum import Enum

import re


class OsFamily(Enum):
    Unknown = 1
    RedHat = 2
    Debian = 3
    Suse = 4
    Windows = 5
    AIX = 6
    Solaris = 7
    MacOS = 8
    Arch = 9

    def is_posix(self):
        return self not in (OsFamily.Unknown, OsFamily.Windows)


class OperatingSystem(Enum):
    Unknown = 1
    RedHat = 2
    CentOS = 3
    Scientific = 4
    OracleLinux = 5
    Debian = 6
    Ubuntu = 7
    OpenSuse = 8
    Fedora = 9
    SLES = 10
    ArchLinux = 11


class OperatingSystemRelease(str):
    # https://regex101.com/r/uJ8oTf/2
    VERSION_RE = re.compile('^(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:[._\-](.*))?$')

    def __init__(self, version):
        super(OperatingSystemRelease, self).__init__()
        self.__version = str(version)

    def __str__(self):
        return self.__version

    def major(self):
        return self.__group(1)

    def minor(self):
        return self.__group(2)

    def patch(self):
        return self.__group(3)

    def lesser(self):
        return self.__group(4)

    def __group(self, num):
        try:
            return self.VERSION_RE \
                .match(self) \
                .group(num)
        except AttributeError:
            return str(self)


class OperatingSystemCodename(str):
    def __init__(self, codename):
        super(OperatingSystemCodename, self).__init__()
        self.__codename = str(codename)

    def __str__(self):
        return self.__codename


class Docker(Enum):
    NO = 1
    YES = 2

    def __nonzero__(self):
        return self is Docker.YES

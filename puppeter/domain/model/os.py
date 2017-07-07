from enum import Enum


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

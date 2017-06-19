from puppeter.domain.os import OsFamily, OperatingSystem
from puppeter.persitance.os import Facter


def test_osfamily():
    osfamily = Facter.get(OsFamily)

    assert osfamily is not OsFamily.Unknown
    assert osfamily is not None


def test_operatingsystem():
    os = Facter.get(OperatingSystem)

    assert os is not OperatingSystem.Unknown
    assert os is not None

import re

from puppeter.domain.facter import Facter
from puppeter.domain.model.osfacts import OsFamily, OperatingSystem, OperatingSystemRelease


def test_osfamily():
    osfamily = Facter.get(OsFamily)

    assert osfamily is not OsFamily.Unknown
    assert osfamily is not None


def test_operatingsystem():
    os = Facter.get(OperatingSystem)

    assert os is not OperatingSystem.Unknown
    assert os is not None


def test_osrelease():
    regex = OperatingSystemRelease.VERSION_RE
    rel = Facter.get(OperatingSystemRelease)

    assert rel is not None
    assert regex.match(rel) is not None


def test_osrelrelease_major():
    rel = Facter.get(OperatingSystemRelease)
    major = rel.major()

    assert major is not None
    assert re.compile('^\d+$').match(major) is not None


def test_osrelrelease_minor():
    rel = Facter.get(OperatingSystemRelease)
    minor = rel.minor()

    assert minor is not None
    assert re.compile('^\d+$').match(minor) is not None

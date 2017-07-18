import re

from puppeter import container
from puppeter.domain.facter import Facter
from puppeter.domain.model.osfacts import OsFamily, OperatingSystem, OperatingSystemRelease, OperatingSystemCodename
from tests.domain.mock_facter import MockFacter


class TestOsFactsResolvingOnMocks:

    # noinspection PyMethodMayBeStatic
    def setup_method(self):
        MockFacter.set_fact(OperatingSystemCodename, OperatingSystemCodename('trusty'))
        MockFacter.set_fact(OperatingSystemRelease, OperatingSystemRelease('14.04'))
        MockFacter.set_fact(OperatingSystem, OperatingSystem.Ubuntu)
        MockFacter.set_fact(OsFamily, OsFamily.Debian)
        container.initialize()

    # noinspection PyMethodMayBeStatic
    def teardown_method(self):
        MockFacter.reset_facts()

    def test_osfamily(self):
        osfamily = Facter.get(OsFamily)

        assert osfamily is not OsFamily.Unknown
        assert osfamily is not None

    def test_operatingsystem(self):
        os = Facter.get(OperatingSystem)

        assert os is not OperatingSystem.Unknown
        assert os is not None

    def test_oscodename(self):
        codename = Facter.get(OperatingSystemCodename)

        assert codename == 'trusty'
        assert type(codename) is OperatingSystemCodename

    def test_osrelease(self):
        regex = OperatingSystemRelease.VERSION_RE
        rel = Facter.get(OperatingSystemRelease)

        assert rel is not None
        assert regex.match(rel) is not None

    def test_osrelrelease_major(self):
        rel = Facter.get(OperatingSystemRelease)
        major = rel.major()

        assert major is not None
        assert type(major) is str
        assert re.compile('^\d+$').match(major) is not None

    def test_osrelrelease_minor(self):
        rel = Facter.get(OperatingSystemRelease)
        minor = rel.minor()

        assert minor is not None
        assert type(minor) is str
        assert re.compile('^\d+$').match(minor) is not None

    def test_osrelease_major_oninvalid(self):
        MockFacter.set_fact(OperatingSystemRelease, OperatingSystemRelease('alpha'))

        rel = Facter.get(OperatingSystemRelease)
        major = rel.major()

        assert major is not None
        assert major is 'alpha'


class TestOsFactsResolvingForReal:

    # noinspection PyMethodMayBeStatic
    def teardown_method(self):
        MockFacter.reset_facts()

    def test_osfamily(self):
        osfamily = Facter.get(OsFamily)

        assert osfamily is not None

    def test_operatingsystem(self):
        os = Facter.get(OperatingSystem)

        assert os is not None

    def test_oscodename(self):
        codename = Facter.get(OperatingSystemCodename)

        assert codename is not None

    def test_osrelease(self):
        rel = Facter.get(OperatingSystemRelease)

        assert rel is not None

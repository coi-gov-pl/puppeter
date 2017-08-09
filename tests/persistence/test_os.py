import re

import puppeter.settings
from puppeter import container
from puppeter.domain.facter import Facter
from puppeter.domain.model.osfacts import OsFamily, OperatingSystem, OperatingSystemRelease, OperatingSystemCodename, \
    Docker
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
    @classmethod
    def setup_class(cls):
        container.initialize()

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

    def test_docker(self, tmpdir):
        old_chroot = puppeter.settings.chroot
        try:
            new_root = tmpdir.mkdir("docker-utest")
            puppeter.settings.chroot = str(new_root) + '/'
            p = new_root.mkdir('proc').mkdir('1').join('cgroup')
            p.write('11:blkio:/docker/885762619\n'
                    '10:pids:/docker/885762619'
                    '9:freezer:/docker/885762619\n'
                    '8:cpuset:/docker/885762619\n'
                    '7:perf_event:/docker/885762619\n'
                    '6:devices:/docker/885762619\n'
                    '5:hugetlb:/docker/885762619\n')
            docker = Facter.get(Docker)

            assert type(docker) is Docker
            assert docker is Docker.YES
            assert bool(docker) is True
        finally:
            puppeter.settings.chroot = old_chroot

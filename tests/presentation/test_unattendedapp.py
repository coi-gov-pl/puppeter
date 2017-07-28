import re

from puppeter import container
from puppeter.domain.model.osfacts import OperatingSystemCodename,\
    OperatingSystem, OsFamily, OperatingSystemRelease
from puppeter.presentation.app import Options
from puppeter.presentation.unattendedapp import UnattendedApp
from tests.domain.mock_facter import MockFacter


def test_unattendedapp_onlyinstaller_with_verbosity(tmpdir, capsys):
    # given
    tmp = tmpdir.join("answers.yml")
    tmp.write('installer:\n'
              '    type: pc4x\n'
              '    mode: Server\n')
    answers = open(str(tmp))
    options = Options(dotdict(dict(answers=answers, verbose=2, execute=False)))
    app = UnattendedApp(options)

    # when
    app.run()
    out, err = capsys.readouterr()

    # then
    assert "wget 'https://apt.puppetlabs.com/puppetlabs-release-pc1-trusty.deb'" in out
    assert 'DEBUG: Answers loaded from file' in err
    assert 'INFO: Installation commands will be generated based on answers file' in err


class dotdict(dict):
    def __getattr__(self, name):
        return self[name]


def restr(str):
    return re.compile('\s*%s' % re.escape(str), re.MULTILINE)


def setup_function():
    container.initialize()
    MockFacter.set_fact(OperatingSystemRelease, OperatingSystemRelease('14.04'))
    MockFacter.set_fact(OperatingSystemCodename, OperatingSystemCodename('trusty'))
    MockFacter.set_fact(OperatingSystem, OperatingSystem.Ubuntu)
    MockFacter.set_fact(OsFamily, OsFamily.Debian)


def teardown_function():
    MockFacter.reset_facts()

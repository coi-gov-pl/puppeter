import os
from puppeter.presentation.cmdparser import CommandLineParser

HERE = os.path.abspath(__file__)


def __get_test_appfactory():
    class TestApp:
        def __init__(self, arg):
            self.arg = arg

        def run(self):
            return 'runned %s' % self.arg

    class TestFactory:
        def interactive(self, parsed):
            return TestApp('interactivly')

        def unattended(self, parsed):
            return TestApp('unattended')
    return TestFactory()


def test_proper_app_creation():
    # given
    factory = __get_test_appfactory()
    parser = CommandLineParser(['puppeter'], appfactory=factory)
    # when
    app = parser.parse()
    result = app.run()
    # then
    assert app is not None
    assert result == 'runned interactivly'


def test_proper_app_creation_unattended():
    # given
    factory = __get_test_appfactory()
    parser = CommandLineParser(['puppeter', '--answers', HERE], appfactory=factory)
    # when
    app = parser.parse()
    result = app.run()
    # then
    assert app is not None
    assert result == 'runned unattended'

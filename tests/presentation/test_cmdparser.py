import os

from puppeter import container
from puppeter.container import Named, Container
from puppeter.domain.model.answers import Answers
from puppeter.presentation import App
from puppeter.presentation.cmdparser import CommandLineParser

HERE = os.path.abspath(__file__)


@Named('interactive')
class InteractiveTestApp(App):
    def _collect_answers(self):
        return Answers()

    def run(self):
        return 'runned interactivly'


@Named('unattended')
class UnattendedTestApp(App):
    def _collect_answers(self):
        return Answers()

    def run(self):
        return 'runned unattended'


class TestAppCreation:
    old_container = None

    @classmethod
    def setup_class(cls):
        cls.old_container = container.app_container
        container.app_container = Container()
        container.bind(App, InteractiveTestApp)
        container.bind(App, UnattendedTestApp)

    @classmethod
    def teardown_class(cls):
        container.app_container = cls.old_container

    def test_proper_app_creation(self):
        # given
        parser = CommandLineParser(['puppeter'])
        # when
        app = parser.parse()
        result = app.run()
        # then
        assert app is not None
        assert result == 'runned interactivly'

    def test_proper_app_creation_unattended(self):
        # given
        parser = CommandLineParser(['puppeter', '--answers', HERE])
        # when
        app = parser.parse()
        result = app.run()
        # then
        assert app is not None
        assert result == 'runned unattended'

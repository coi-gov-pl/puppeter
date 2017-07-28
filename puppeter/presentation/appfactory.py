from puppeter.presentation.app import App
from puppeter.presentation.cmdparser import Options
from puppeter.presentation.interactiveapp import InteractiveApp
from puppeter.presentation.unattendedapp import UnattendedApp


class AppFactory:
    def interactive(self, options):
        # type: (Options) -> App
        return InteractiveApp(options)

    def unattended(self, options):
        # type: (Options) -> App
        return UnattendedApp(options)

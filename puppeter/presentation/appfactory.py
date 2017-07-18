from puppeter.presentation.interactiveapp import InteractiveApp
from puppeter.presentation.unattendedapp import UnattendedApp


class AppFactory:
    def interactive(self, parsed):
        return InteractiveApp(parsed)

    def unattended(self, parsed):
        return UnattendedApp(parsed)

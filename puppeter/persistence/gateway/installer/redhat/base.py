from abc import ABCMeta, abstractmethod

from six import with_metaclass

from puppeter.domain.facter import Facter
from puppeter.domain.model import Installer
from puppeter.domain.model.configurer import Configurer
from puppeter.domain.model.installer import Mode
from puppeter.domain.model.osfacts import OperatingSystem, OperatingSystemRelease


class BaseRedHatConfigurer(with_metaclass(ABCMeta, Configurer)):
    def __init__(self, installer):
        self._installer = installer  # type: Installer

    def produce_commands(self):
        collector = self._collector()
        if Facter.get(OperatingSystem) != OperatingSystem.Fedora and Facter.get(OperatingSystemRelease).major() == '5':
            collector.collect_from_file('wget downloader', 'wget.sh')
        self._collect_repo(collector)
        self._collect_agent(collector)
        if self._installer.mode() == Mode.Server:
            self._collect_server(collector)
        return collector.lines()

    @abstractmethod
    def _collect_repo(self, collector):
        # type: (Configurer.CommandsCollector) -> None
        raise NotImplementedError()

    @abstractmethod
    def _collect_agent(self, collector):
        # type: (Configurer.CommandsCollector) -> None
        raise NotImplementedError()

    @abstractmethod
    def _collect_server(self, collector):
        # type: (Configurer.CommandsCollector) -> None
        raise NotImplementedError()

from abc import ABCMeta, abstractmethod

from six import with_metaclass

from puppeter.domain.model import Installer  # NOQA
from puppeter.domain.model.configurer import Configurer
from puppeter.domain.model.installer import Mode


class BaseDebianConfigurer(with_metaclass(ABCMeta, Configurer)):
    UPDATE_INTERVAL = 24 * 60 * 60

    def __init__(self, installer):
        self._installer = installer  # type: Installer

    def produce_commands(self):
        collector = self._collector()
        collector.collect_from_template('apt system update',
                                        'apt-update.sh',
                                        dict(interval=self.UPDATE_INTERVAL))
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

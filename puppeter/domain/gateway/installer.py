from __future__ import absolute_import
from six import with_metaclass
from abc import ABCMeta, abstractmethod

from puppeter.domain.model.configurer import Configurer  # NOQA
from puppeter.domain.model import Installer  # NOQA


class CommandsBinder(object):

    def bind(self, order, method):
        # type: (int, callable) -> None
        pass


class InstallerGateway(with_metaclass(ABCMeta, object)):
    def produce_commands(self, installer):
        # type: (Installer) -> [str]
        return self._provide_configurers(installer)\
            .produce_commands()

    @abstractmethod
    def _bind(self, binder):
        # type: (CommandsBinder) -> None
        pass

    @abstractmethod
    def _provide_configurers(self, installer):
        # type: (Installer) -> [Configurer]
        pass

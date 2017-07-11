from __future__ import absolute_import
from six import with_metaclass
from abc import ABCMeta, abstractmethod

from puppeter.domain.model.configurer import Configurer  # NOQA
from puppeter.domain.model import Installer  # NOQA


class InstallerGateway(with_metaclass(ABCMeta, object)):
    def produce_commands(self, installer):
        # type: (Installer) -> [str]
        return self._provide_configurer(installer)\
            .produce_commands()

    @abstractmethod
    def _provide_configurer(self, installer):
        # type: (Installer) -> Configurer
        pass

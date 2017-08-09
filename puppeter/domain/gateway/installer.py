from __future__ import absolute_import

from six import with_metaclass
from abc import ABCMeta, abstractmethod


class InstallerGateway(with_metaclass(ABCMeta, object)):

    def configurers(self, installer):
        configurers = []
        if installer is not None:
            configurers.extend(self._provide_install_configurers(installer))
            configurers.extend(self._puppet_cert_issue(installer))
            configurers.extend(self._puppet_services(installer))
        return tuple(configurers)

    @abstractmethod
    def _provide_install_configurers(self, installer):
        pass

    @abstractmethod
    def _puppet_cert_issue(self, installer):
        pass

    @abstractmethod
    def _puppet_services(self, installer):
        pass

from abc import ABCMeta, abstractmethod

from six import with_metaclass
from typing import Sequence

from puppeter.domain.model.configurer import Configurer
from puppeter.domain.model.fqdn import FqdnConfiguration


class FqdnSetterGateway(with_metaclass(ABCMeta)):
    @abstractmethod
    def process_fully_qualified_domain_name(self, fqdn):
        # type: (FqdnConfiguration) -> Sequence[Configurer]
        pass

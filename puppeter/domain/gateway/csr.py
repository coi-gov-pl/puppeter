from abc import ABCMeta, abstractmethod

from six import with_metaclass
from typing import Sequence

from puppeter.domain.model.configurer import Configurer
from puppeter.domain.model.csr import CsrAttributesConfiguration


class CsrAttributesSetterGateway(with_metaclass(ABCMeta)):
    @abstractmethod
    def save_csr_attributes(self, csr_attrs):
        # type: (CsrAttributesConfiguration) -> Sequence[Configurer]
        pass

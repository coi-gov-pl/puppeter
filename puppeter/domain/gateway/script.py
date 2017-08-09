from abc import ABCMeta, abstractmethod

from six import with_metaclass
from typing import Sequence

from puppeter.domain.model.configurer import Configurer


class ScriptPostProcessor(with_metaclass(ABCMeta)):
    @abstractmethod
    def postprocess(self, commands):
        # type: (Sequence[str]) -> Sequence[str]
        pass


class ScriptLibrariesConfigurer(with_metaclass(ABCMeta, Configurer)):
    pass

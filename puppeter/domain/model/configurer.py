from abc import ABCMeta, abstractmethod
from six import with_metaclass


class Configurer(with_metaclass(ABCMeta, object)):
    @abstractmethod
    def produce_commands(self):
        # type: () -> [str]
        raise NotImplementedError()

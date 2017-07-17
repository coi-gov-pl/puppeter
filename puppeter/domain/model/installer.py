from abc import abstractmethod, ABCMeta
from six import with_metaclass

from puppeter.container import Named
from enum import Enum


class Mode(Enum):
    Agent = 1
    Server = 2
    Masterless = 3


class WithOptions(with_metaclass(ABCMeta, object)):

    @abstractmethod
    def raw_options(self):
        pass

    @abstractmethod
    def read_raw_options(self, options):
        pass


class Installer(WithOptions):
    def __init__(self):
        self.__mode = Mode.Agent  # type: Mode

    def raw_options(self):
        # noinspection PyUnresolvedReferences
        installer_type = self.bean_name()
        return {
          'mode': self.__mode.name,
          'type': installer_type
        }

    def read_raw_options(self, options):
        try:
            self.__mode = Mode[options['mode']]
        except KeyError:
            pass

    def mode(self):
        # type: () -> Mode
        return self.__mode


@Named('gem')
class RubygemsInstaller(Installer):
    def __init__(self):
        Installer.__init__(self)
        self.__version = None

    def raw_options(self):
        parent_options = Installer.raw_options(self)
        merged = parent_options.copy()
        merged.update({
          'version': self.__version
        })
        return merged

    def read_raw_options(self, options):
        Installer.read_raw_options(self, options)
        try:
            self.__version = str(options['version'])
        except KeyError:
            pass

    def version(self):
        return self.__version


class CollectionInstaller(Installer):
    pass


class MemScale(Enum):
    KILO = 1
    MEGA = 2
    GIGA = 3


class JavaMemorySpec:

    def __init__(self, num, scale=MemScale.MEGA):
        self.__num = num
        self.__scale = scale

    @staticmethod
    def gigabytes_of(num):
        return JavaMemorySpec(num, MemScale.GIGA)

    @staticmethod
    def megabytes_of(num):
        return JavaMemorySpec(num, MemScale.MEGA)

    @staticmethod
    def kilobytes_of(num):
        return JavaMemorySpec(num, MemScale.KILO)


class JavaMemory(WithOptions):

    def raw_options(self):
        pass

    def read_raw_options(self, options):
        pass

    def __init__(self, heap_maximum=JavaMemorySpec.gigabytes_of(2), heap_minimum=None):
        self.__heap_maximum = heap_maximum
        if heap_minimum is not None:
            self.__heap_minimum = heap_minimum
        else:
            self.__heap_minimum = heap_maximum

    def heap_maximum(self):
        return self.__heap_maximum

    def heap_minimum(self):
        return self.__heap_minimum


class After4xCollectionInstaller(CollectionInstaller):
    pass


@Named('pc3x')
class Collection3xInstaller(CollectionInstaller):
    pass


@Named('pc4x')
class Collection4xInstaller(After4xCollectionInstaller):
    pass


@Named('pc5x')
class Collection5xInstaller(After4xCollectionInstaller):
    pass

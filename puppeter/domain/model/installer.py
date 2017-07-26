from abc import abstractmethod, ABCMeta

import re
from six import with_metaclass

from puppeter.container import Named
from enum import Enum


class Mode(Enum):
    Agent = 1
    Server = 2


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

    @abstractmethod
    def is_after_4x(self):
        # type: () -> bool
        pass


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


class CollectionInstaller(with_metaclass(ABCMeta, Installer)):
    pass


class MemScale(Enum):
    KILO = 1
    MEGA = 2
    GIGA = 3

    @staticmethod
    def of(repr):
        return {
            'k': MemScale.KILO,
            'm': MemScale.MEGA,
            'g': MemScale.GIGA
        }[repr]

    def to_s(self):
        return {
            MemScale.KILO: 'k',
            MemScale.MEGA: 'm',
            MemScale.GIGA: 'g'
        }[self]


class JavaMemorySpec:

    def __init__(self, num, scale=MemScale.MEGA):
        self.__num = int(num)  # type: int
        self.__scale = scale  # type: MemScale

    @staticmethod
    def of(repr):
        # https://regex101.com/r/YATBuy/1
        pattern = re.compile('^([0-9]+)([kmg])$', re.IGNORECASE)
        match = pattern.match(repr)
        num = int(match.group(1))
        scale_repr = match.group(2).lower()
        scale = MemScale.of(scale_repr)
        return JavaMemorySpec(num, scale)

    def scale(self):
        return self.__scale

    def number(self):
        return self.__num

    def __str__(self):
        return '%d%s' % (self.__num, self.__scale.to_s())


class JavaMemory(WithOptions):

    def raw_options(self):
        d = {
            'heap': {}
        }
        if self.heap_maximum() is not None:
            d['heap']['max'] = str(self.heap_maximum())
        if self.heap_minimum() is not None:
            d['heap']['min'] = str(self.heap_minimum())
        return d

    def read_raw_options(self, options):
        try:
            self.__heap_maximum = JavaMemorySpec.of(options['heap']['max'])
        except KeyError:
            pass
        try:
            self.__heap_minimum = JavaMemorySpec.of(options['heap']['min'])
        except KeyError:
            pass

    def __init__(self, heap_maximum=None, heap_minimum=None):
        self.__heap_maximum = heap_maximum  # type: JavaMemorySpec
        if heap_minimum is not None:
            self.__heap_minimum = heap_minimum  # type: JavaMemorySpec
        else:
            self.__heap_minimum = heap_maximum  # type: JavaMemorySpec

    def heap_maximum(self):
        return self.__heap_maximum

    def heap_minimum(self):
        return self.__heap_minimum

    def is_set(self):
        return self.heap_maximum() is not None or self.heap_minimum() is not None


class After4xCollectionInstaller(CollectionInstaller):
    def __init__(self):
        CollectionInstaller.__init__(self)
        self.__mem = JavaMemory()  # type: JavaMemory

    def is_after_4x(self):
        return True

    def raw_options(self):
        options = super(CollectionInstaller, self).raw_options()
        if self.__mem.is_set():
            options['puppetserver_jvm_memory'] = self.__mem.raw_options()
        return options

    def read_raw_options(self, options):
        super(CollectionInstaller, self).read_raw_options(options)
        if self.mode() == Mode.Server:
            try:
                self.__mem.read_raw_options(options['puppetserver_jvm_memory'])
            except KeyError:
                pass

    def puppetserver_jvm_memory(self):
        return self.__mem


@Named('pc3x')
class Collection3xInstaller(CollectionInstaller):
    def is_after_4x(self):
        return False


@Named('pc4x')
class Collection4xInstaller(After4xCollectionInstaller):
    pass


@Named('pc5x')
class Collection5xInstaller(After4xCollectionInstaller):
    pass

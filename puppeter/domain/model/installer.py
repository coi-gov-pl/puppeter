import re
from abc import abstractmethod, ABCMeta

from enum import Enum
from six import with_metaclass
from typing import Sequence

from puppeter.container import Named
from puppeter.domain.model.gemrequirement import GemRequirement
from puppeter.domain.model.withoptions import WithOptions


class Mode(Enum):
    Agent = 1
    Server = 2


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
    def is_after_4x(self):
        return GemRequirement(self.version()).satified_by('4.0')

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

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return str(self) == str(other)


class JavaMemory(WithOptions):

    def __init__(self, heap_maximum=None, heap_minimum=None, metaspace_maximum=None):
        self.__heap_maximum = heap_maximum  # type: JavaMemorySpec
        if heap_minimum is not None:
            self.__heap_minimum = heap_minimum  # type: JavaMemorySpec
        else:
            self.__heap_minimum = heap_maximum  # type: JavaMemorySpec
        self.__metaspace_maximum = metaspace_maximum  # type: JavaMemorySpec

    def raw_options(self):
        d = {}
        if self.heap_maximum() is not None:
            self._update(d, {'heap': {'max': str(self.heap_maximum())}})
        if self.heap_minimum() is not None:
            self._update(d, {'heap': {'min': str(self.heap_minimum())}})
        if self.metaspace_maximum() is not None:
            self._update(d, {'metaspace': {'max': str(self.metaspace_maximum())}})
        return {
            'puppetserver': {
                'jvm': {'memory': d}
            }
        } if (len(d) > 0) else {}

    def read_raw_options(self, options):
        try:
            mem = options['puppetserver']['jvm']['memory']
        except KeyError:
            return
        try:
            self.__heap_maximum = JavaMemorySpec.of(mem['heap']['max'])
        except KeyError:
            pass
        try:
            self.__heap_minimum = JavaMemorySpec.of(mem['heap']['min'])
        except KeyError:
            if self.__heap_maximum is not None:
                self.__heap_minimum = self.__heap_maximum
        try:
            self.__metaspace_maximum = JavaMemorySpec.of(mem['metaspace']['max'])
        except KeyError:
            pass

    def heap_maximum(self):
        return self.__heap_maximum

    def heap_minimum(self):
        return self.__heap_minimum

    def metaspace_maximum(self):
        return self.__metaspace_maximum

    def is_set(self):
        return self.heap_maximum() is not None \
            or self.heap_minimum() is not None \
            or self.metaspace_maximum() is not None


class JvmArgs(WithOptions, Sequence):

    def __init__(self, args=tuple()):
        self.__args = []
        self.__args.extend(args)

    def __getitem__(self, i):
        return self.__args[i]

    def __len__(self):
        return len(self.__args)

    def raw_options(self):
        return {
            'puppetserver': {
                'jvm': {'args': tuple(self.__args)}
            }
        }

    def read_raw_options(self, options):
        try:
            new_args = options['puppetserver']['jvm']['args']
            del self.__args[:]
            self.__args.extend(new_args)
        except KeyError:
            pass

    def are_set(self):
        return len(self.__args) > 0


class After4xCollectionInstaller(CollectionInstaller):
    def __init__(self):
        CollectionInstaller.__init__(self)
        self.__mem = JavaMemory()  # type: JavaMemory
        self.__jvmargs = JvmArgs()  # type: JvmArgs

    def is_after_4x(self):
        return True

    def raw_options(self):
        options = super(CollectionInstaller, self).raw_options()
        if self.__mem.is_set():
            self._update(options, self.__mem.raw_options())
        if self.__jvmargs.are_set():
            self._update(options, self.__jvmargs.raw_options())
        return options

    def read_raw_options(self, options):
        super(CollectionInstaller, self).read_raw_options(options)
        if self.mode() == Mode.Server:
            self.__jvmargs.read_raw_options(options)
            try:
                self.__mem.read_raw_options(options)
            except KeyError:
                pass

    def puppetserver_jvm_memory(self):
        return self.__mem

    def puppetserver_jvm_args(self):
        return self.__jvmargs


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

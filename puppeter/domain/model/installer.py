from puppeter.container import Named
from enum import Enum


class Mode(Enum):
    Agent = 1
    Server = 2
    Masterless = 3


class Installer:
    def __init__(self):
        self.__mode = Mode.Agent

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
        except:
            pass

    def mode(self):
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
        except:
            pass

    def version(self):
        return self.__version


class CollectionInstaller(Installer):
    pass


@Named('pc3x')
class Collection3xInstaller(CollectionInstaller):
    pass


@Named('pc4x')
class Collection4xInstaller(CollectionInstaller):
    pass


@Named('pc5x')
class Collection5xInstaller(CollectionInstaller):
    pass

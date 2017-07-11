from puppeter.container import Named
from puppeter.domain.facter import Facter
from puppeter.domain.model.osfacts import OperatingSystemCodename
from puppeter.domain.model.configurer import Configurer


@Named('pc4x-debian')
class PC4xConfigurer(Configurer):
    def __init__(self, installer):
        self.__installer = installer

    def produce_commands(self):
        codename = Facter.get(OperatingSystemCodename)
        cmds = []
        cmds.append("")
        raise NotImplementedError('Not yet implemented! %s' % codename)

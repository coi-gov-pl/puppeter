from puppeter.container import Named
from puppeter.domain.model.configurer import Configurer


@Named('pc4x-redhat')
class PC4xConfigurer(Configurer):
    def __init__(self, installer):
        self.__installer = installer

    def produce_commands(self):
        raise NotImplementedError('Not yet implemented!')

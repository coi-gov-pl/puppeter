from puppeter.container import Named
from puppeter.domain.model.configurer import Configurer


@Named('pc5x-debian')
class PC5xConfigurer(Configurer):
    def __init__(self, installer):
        self.installer = installer

    def produce_commands(self):
        raise NotImplementedError('Not yet implemented!')

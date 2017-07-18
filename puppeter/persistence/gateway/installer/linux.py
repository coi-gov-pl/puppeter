from puppeter.container import Named
from puppeter.domain.model.configurer import Configurer


@Named('gem')
class RubyGemConfigurer(Configurer):
    def __init__(self, installer):
        self.installer = installer

    def produce_commands(self):
        raise NotImplementedError('Not yet implemented!')

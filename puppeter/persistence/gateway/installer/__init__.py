from puppeter import container
from puppeter.domain.model.configurer import Configurer
from puppeter.persistence.gateway.installer.linux import RubyGemConfigurer

container.bind(Configurer, RubyGemConfigurer)

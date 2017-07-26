from puppeter import container
from puppeter.domain.model.configurer import Configurer
from puppeter.persistence.gateway.services.puppetserver import \
    PuppetServerServiceStarterConfigurer, \
    PuppetServerServiceMemoryConfigurer

container.bind(Configurer, PuppetServerServiceStarterConfigurer)
container.bind(Configurer, PuppetServerServiceMemoryConfigurer)

from puppeter import container
from puppeter.domain.gateway.answers import AnswersGateway
from puppeter.domain.gateway.fqdn import FqdnSetterGateway
from puppeter.persistence.gateway.answers import YamlAnswersGateway
from puppeter.persistence.gateway.fqdn import FqdnSetterGatewayImpl


container.bind(AnswersGateway, YamlAnswersGateway)
container.bind(FqdnSetterGateway, FqdnSetterGatewayImpl)

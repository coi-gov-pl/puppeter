from puppeter import container
from puppeter.domain.gateway.answers import AnswersGateway
from puppeter.persistence.gateway.answers import YamlAnswersGateway


container.bind(AnswersGateway, YamlAnswersGateway)

from puppeter import container
from puppeter.domain.gateway.answers import AnswersGateway
from puppeter.domain.gateway.csr import CsrAttributesSetterGateway
from puppeter.domain.gateway.fqdn import FqdnSetterGateway
from puppeter.domain.gateway.script import ScriptPostProcessor, ScriptLibrariesConfigurer
from puppeter.persistence.gateway.answers import YamlAnswersGateway
from puppeter.persistence.gateway.csr import CsrAttributesSetterGatewayImpl
from puppeter.persistence.gateway.fqdn import FqdnSetterGatewayImpl
from puppeter.persistence.gateway.script import BashScriptPostProcessor, BashScriptLibrariesConfigurer

container.bind(AnswersGateway, YamlAnswersGateway)
container.bind(FqdnSetterGateway, FqdnSetterGatewayImpl)
container.bind(ScriptPostProcessor, BashScriptPostProcessor)
container.bind(ScriptLibrariesConfigurer, BashScriptLibrariesConfigurer)
container.bind(CsrAttributesSetterGateway, CsrAttributesSetterGatewayImpl)

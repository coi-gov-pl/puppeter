import ruamel.yaml

from typing import Sequence

from puppeter.domain.gateway.csr import CsrAttributesSetterGateway
from puppeter.domain.model.configurer import Configurer, ScriptFormat
from puppeter.domain.model.csr import CsrAttributesConfiguration
from puppeter.domain.model.installer import Mode
from puppeter.domain.model.ordered import Order


@Order(250)
class CsrAttributesConfigurer(Configurer):
    def __init__(self, csr_attrs, mode):
        self.__csr_attr = csr_attrs  # type: CsrAttributesConfiguration
        self.__mode = mode  # type: Mode

    def produce_commands(self):
        mapping = dict(
            content=self.__as_yaml()
        )
        if self.__mode == Mode.Agent:
            template = 'csr_agent.pp'
        elif self.__mode == Mode.Server:
            template = 'csr_server.pp'
        else:
            raise Exception('Invalid mode given: {mode}'.format(mode=self.__mode))

        return self._collector().collect_from_template(
            description='Configuring puppet node certificate CSR attributes',
            template=template,
            mapping=mapping,
            format=ScriptFormat.PUPPET
        ).lines()

    def __as_yaml(self):
        csr = {
            'extension_requests': self.__csr_attr.raw_options()
        }
        return ruamel.yaml.dump(csr, Dumper=ruamel.yaml.RoundTripDumper)


class CsrAttributesSetterGatewayImpl(CsrAttributesSetterGateway):
    def save_csr_attributes(self, csr_attrs, mode):
        # type: (CsrAttributesConfiguration, Mode) -> Sequence[Configurer]
        return [
            CsrAttributesConfigurer(csr_attrs, mode)
        ]

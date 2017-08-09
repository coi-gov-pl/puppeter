import ruamel.yaml

from typing import Sequence

from puppeter.domain.gateway.csr import CsrAttributesSetterGateway
from puppeter.domain.model.configurer import Configurer, ScriptFormat
from puppeter.domain.model.csr import CsrAttributesConfiguration
from puppeter.domain.model.ordered import Order


@Order(250)
class CsrAttributesConfigurer(Configurer):
    def __init__(self, csr_attrs):
        self.__csr_attr = csr_attrs  # type: CsrAttributesConfiguration

    def produce_commands(self):
        mapping = dict(
            content=self.__as_yaml()
        )
        return self._collector().collect_from_template(
            description='Configuring puppet node certificate CSR attributes',
            template='csr.pp',
            mapping=mapping,
            format=ScriptFormat.PUPPET
        ).lines()

    def __as_yaml(self):
        csr = {
            'extension_requests': self.__csr_attr.raw_options()
        }
        return ruamel.yaml.dump(csr, Dumper=ruamel.yaml.RoundTripDumper)


class CsrAttributesSetterGatewayImpl(CsrAttributesSetterGateway):
    def save_csr_attributes(self, csr_attrs):
        # type: (CsrAttributesConfiguration) -> Sequence[Configurer]
        return [
            CsrAttributesConfigurer(csr_attrs)
        ]

from typing import Any, Callable, Dict, TypeVar, Optional, IO

import puppeter
from puppeter import container
from puppeter.domain.model.csr import CsrAttributesConfiguration
from puppeter.domain.model.fqdn import FqdnConfiguration
from puppeter.domain.model.installer import Installer
from puppeter.domain.model.answers import Answers
from puppeter.domain.gateway.answers import AnswersGateway
from puppeter.container import Named
import ruamel.yaml

T = TypeVar('T')


@Named('yaml')
class YamlAnswersGateway(AnswersGateway):
    def write_answers_to_file(self, answers, target_file):
        # type: (Answers, IO) -> None
        raw_answers = {}
        if answers.installer() is not None:
            raw_answers['installer'] = answers.installer().raw_options()
        if answers.fqdn_configuration() is not None:
            raw_answers['fqdn'] = answers.fqdn_configuration().raw_options()
        if answers.csrattrs_configuration() is not None:
            raw_answers['csr-attributes'] = answers.csrattrs_configuration().raw_options()
        yaml = ruamel.yaml.dump(raw_answers, Dumper=ruamel.yaml.RoundTripDumper)
        target_file.write(yaml)

    def read_answers_from_file(self, target_file):
        code = ruamel.yaml.load(target_file.read(), ruamel.yaml.RoundTripLoader)
        log = puppeter.get_logger(YamlAnswersGateway)
        log.debug("Answers loaded from file: %s", code)
        installer = self.__process_data(code,
                                        'installer',
                                        lambda val: self.__load_installer(val))
        fqdn = self.__process_data(code,
                                   'fqdn',
                                   lambda val: FqdnConfiguration(val))
        csr_attrs = self.__process_data(code,
                                        'csr-attributes',
                                        lambda val: self.__load_csr(val))
        return Answers(
            installer=installer,
            fqdn_configuration=fqdn,
            csrattrs_configuration=csr_attrs
        )

    @staticmethod
    def __load_csr(options):
        conf = CsrAttributesConfiguration()
        conf.read_raw_options(options)
        return conf

    @staticmethod
    def __load_installer(options):
        bean_name = options['type']
        installer = container.get_named(Installer, bean_name)
        installer.read_raw_options(options)
        return installer

    @staticmethod
    def __process_data(data, key, func):
        # type: (Dict[str,Any],str,Callable[[Any],T]) -> Optional[T]
        try:
            value = data[key]
            return func(value)
        except KeyError:
            return None

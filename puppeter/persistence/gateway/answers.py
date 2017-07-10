import puppeter
from puppeter import container
from puppeter.domain.model.installer import Installer
from puppeter.domain.model.answers import Answers
from puppeter.domain.gateway.answers import AnswersGateway
from puppeter.container import Named
import ruamel.yaml


@Named('yaml')
class YamlAnswersGateway(AnswersGateway):
    def write_answers_to_file(self, answers, file):
        raw_answers = {
            'installer': answers.installer().raw_options()
        }
        yaml = ruamel.yaml.dump(raw_answers, Dumper=ruamel.yaml.RoundTripDumper)
        file.write(yaml)

    def read_answers_from_file(self, file):
        code = ruamel.yaml.load(file.read(), ruamel.yaml.RoundTripLoader)
        log = puppeter.get_logger(YamlAnswersGateway)
        log.debug("Answers loaded from file: %s", code)
        installer = self.__load_installer(code['installer'])
        return Answers(
            installer=installer
        )

    @staticmethod
    def __load_installer(options):
        bean_name = options['type']
        installer = container.get_named(Installer, bean_name)
        installer.read_raw_options(options)
        return installer

from os.path import dirname, join
import ruamel.yaml

from puppeter.domain.model.answers import Answers
from puppeter.domain.model.fqdn import FqdnConfiguration
from puppeter.domain.model.installer import Collection4xInstaller, Mode
from puppeter.persistence.gateway.answers import YamlAnswersGateway

EXAMPLE_ANSWERS = open(join(dirname(__file__), 'example-answers-simple.yaml'), mode='r').read()


def __load(yaml_content):
    return ruamel.yaml.load(yaml_content, Loader=ruamel.yaml.Loader)


def test_write(tmpdir):
    # given
    installer = Collection4xInstaller()
    installer.read_raw_options({
        'mode': 'Server'
    })
    answers = Answers(
        installer=installer,
        fqdn_configuration=FqdnConfiguration('app6.acme.internal')
    )
    gateway = YamlAnswersGateway()
    target = tmpdir.join('answers.yaml')

    # when
    gateway.write_answers_to_file(answers, target)

    # then
    assert __load(target.read()) == __load(EXAMPLE_ANSWERS)


def test_read(tmpdir):
    # given
    gateway = YamlAnswersGateway()
    target = tmpdir.join('answers.yaml')
    target.write(EXAMPLE_ANSWERS)

    # when
    answers = gateway.read_answers_from_file(target)

    # then
    assert answers is not None
    assert isinstance(answers, Answers)
    assert isinstance(answers.installer(), Collection4xInstaller)
    assert answers.installer().mode() == Mode.Server
    assert answers.fqdn_configuration().hostname() == 'app6'
    assert answers.fqdn_configuration().has_domain()

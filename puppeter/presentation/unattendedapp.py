from puppeter.domain.gateway.answers import AnswersGateway
from puppeter import container
from pprint import pprint


class UnattendedApp:
    def __init__(self, parsed):
        self.__parsed = parsed

    def run(self):
        file = self.__parsed.answers
        answers = self.__gw().read_answers_from_file(file)
        pprint(answers)

    def __gw(self):
        # type: () -> AnswersGateway
        return container.get(AnswersGateway)

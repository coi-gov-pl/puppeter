from typing import IO

import puppeter
from puppeter import container
from puppeter.container import Named
from puppeter.domain.gateway.answers import AnswersGateway
from puppeter.domain.model.answers import Answers
from puppeter.presentation.app import App


@Named('unattended')
class UnattendedApp(App):

    def __init__(self, options):
        App.__init__(self, options)
        self.__log = puppeter.get_logger(UnattendedApp)

    def _collect_answers(self):
        target = self._options.answers()
        answers = self.__load_answers(container.get(AnswersGateway), target)
        if self._options.execute():
            self.__log.warning('Installation will be performed from answer file:'
                               ' %s. System will be altered!!!', target.name)
        else:
            self.__log.info('Installation commands will be generated based on answers file'
                            ' %s and printed out. System will NOT be altered.', target.name)
        return answers

    @staticmethod
    def __load_answers(gateway, target):
        # type: (AnswersGateway, IO) -> Answers
        return gateway.read_answers_from_file(target)

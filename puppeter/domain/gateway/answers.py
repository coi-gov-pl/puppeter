from six import with_metaclass
from abc import ABCMeta, abstractmethod

from typing import IO

from puppeter.domain.model.answers import Answers


class AnswersGateway(with_metaclass(ABCMeta, object)):
    @abstractmethod
    def read_answers_from_file(self, target):
        # type: (IO) -> Answers
        pass

    @abstractmethod
    def write_answers_to_file(self, answers, target):
        # type: (Answers, IO) -> None
        pass


class AnswersProcessor(with_metaclass(ABCMeta, object)):

    @abstractmethod
    def process(self, answers):
        # type: (Answers) -> None
        pass

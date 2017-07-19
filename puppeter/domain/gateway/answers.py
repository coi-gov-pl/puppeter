from six import with_metaclass
from abc import ABCMeta, abstractmethod

from puppeter.domain.model.answers import Answers  # NOQA


class AnswersGateway(with_metaclass(ABCMeta, object)):
    @abstractmethod
    def read_answers_from_file(self, file):
        # type: (file) -> Answers
        pass

    @abstractmethod
    def write_answers_to_file(self, answers, file):
        # type: (Answers, file) -> None
        pass


class AnswersProcessor(with_metaclass(ABCMeta, object)):

    @abstractmethod
    def process(self, answers):
        # type: (Answers) -> None
        pass

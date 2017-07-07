from six import with_metaclass
from abc import ABCMeta, abstractmethod


class AnswersGateway(with_metaclass(ABCMeta, object)):
    @abstractmethod
    def read_answers_from_file(self, file):
        pass

    @abstractmethod
    def write_answers_to_file(self, answers, file):
        pass

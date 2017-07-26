from typing import Sequence, List

import logging

import puppeter
from puppeter import container
from puppeter.domain.facter import Facter
from puppeter.domain.gateway.answers import AnswersProcessor
from puppeter.domain.gateway.installer import InstallerGateway
from puppeter.domain.model import osfacts
from puppeter.domain.model.answers import Answers
from puppeter.domain.model.configurer import Configurer


class AnswersProcessorImpl(AnswersProcessor):

    def __init__(self, options):
        self.options = options  # type:
        self.__log = puppeter.get_logger(AnswersProcessorImpl)

    def process(self, answers):
        configurers = []
        configurers.extend(self.__perform_installation(answers))
        commands = self.__collect_commands(configurers)
        for line in commands:
            if self.options.execute:
                self.__log.warning('EXECUTING: %s', line)
            else:
                print(line)

    @staticmethod
    def __perform_installation(answers):
        # type: (Answers) -> Sequence[Configurer]
        osfamily = Facter.get(osfacts.OsFamily)
        gateway = container.get_named(InstallerGateway, osfamily.name.lower())
        return gateway.configurers(answers.installer())

    @staticmethod
    def __collect_commands(configurers):
        # type: (List[Configurer]) -> Sequence[str]
        sorted_cfg = sorted(configurers, key=AnswersProcessorImpl.__sort_by_order)
        commands = []
        for configurer in sorted_cfg:
            commands.extend(configurer.produce_commands())
        return commands

    @staticmethod
    def __sort_by_order(configurer):
        # type: (Configurer) -> int
        try:
            # noinspection PyUnresolvedReferences
            return configurer.order()
        except AttributeError:
            return 500

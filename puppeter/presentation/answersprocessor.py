import re
from argparse import Namespace
from typing import Sequence, List

from pip._vendor.packaging.markers import Op

import puppeter
from puppeter import container
from puppeter.domain.facter import Facter
from puppeter.domain.gateway.answers import AnswersProcessor
from puppeter.domain.gateway.fqdn import FqdnSetterGateway
from puppeter.domain.gateway.installer import InstallerGateway
from puppeter.domain.model import osfacts
from puppeter.domain.model.answers import Answers
from puppeter.domain.model.configurer import Configurer
from puppeter.presentation.app import Options


class AnswersProcessorImpl(AnswersProcessor):

    SHEBANG_REGEX = re.compile('^#!(.*)\n', re.MULTILINE)

    def __init__(self, options):
        self.options = options  # type: Options
        self.__log = puppeter.get_logger(AnswersProcessorImpl)

    def process(self, answers):
        configurers = []
        configurers.extend(self.__perform_installation(answers))
        configurers.extend(self.__setup_fqdn(answers))
        commands = self.__collect_commands(configurers)
        for line in commands:
            if self.options.execute():
                self.__log.warning('EXECUTING: %s', line)
            else:
                print(line)

    @staticmethod
    def __perform_installation(answers):
        # type: (Answers) -> Sequence[Configurer]
        configurers = []
        if answers.installer() is not None:
            osfamily = Facter.get(osfacts.OsFamily)
            gateway = container.get_named(InstallerGateway, osfamily.name.lower())
            configurers.extend(
                gateway.configurers(answers.installer())
            )
        return configurers

    @staticmethod
    def __setup_fqdn(answers):
        # type: (Answers) -> Sequence[Configurer]
        configurers = []
        if answers.fqdn_configuration() is not None:
            gateway = container.get(FqdnSetterGateway)
            configurers.extend(
                gateway.process_fully_qualified_domain_name(answers.fqdn_configuration())
            )
        return configurers

    @classmethod
    def __collect_commands(cls, configurers):
        # type: (List[Configurer]) -> Sequence[str]
        sorted_cfg = sorted(configurers, key=AnswersProcessorImpl.__sort_by_order)
        commands = []
        for configurer in sorted_cfg:
            commands.extend(configurer.produce_commands())
        return cls.__postprocess(commands)

    @staticmethod
    def __sort_by_order(configurer):
        # type: (Configurer) -> int
        try:
            # noinspection PyUnresolvedReferences
            return configurer.order()
        except AttributeError:
            return 500

    @classmethod
    def __postprocess(cls, commands):
        # type: (Sequence[str]) -> Sequence[str]
        ln = "\n"
        header = ['#!/usr/bin/env bash', 'set -ex', '']
        stripped = cls.__strip_shebang(ln.join(commands)).split(ln)
        return header + stripped

    @staticmethod
    def __strip_shebang(script):
        return re.sub(AnswersProcessorImpl.SHEBANG_REGEX, '', script)

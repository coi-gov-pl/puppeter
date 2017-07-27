from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from enum import Enum
from string import Template
from typing import Sequence, Any, Dict, Type

import pkg_resources
import re
from six import with_metaclass, iteritems

from puppeter import container


class ScriptFormat(Enum):
    BASH = 1
    PUPPET = 2


class CommandsCollector(with_metaclass(ABCMeta)):
    def collect_from_template(self, description, template, mapping, format=ScriptFormat.BASH):
        # type: (str, str, Dict[str, Any]) -> CommandsCollector
        pass

    def collect_from_file(self, description, path):
        # type: (str, str) -> CommandsCollector
        pass

    def lines(self):
        # type: () -> Sequence[str]
        pass


class Configurer(with_metaclass(ABCMeta)):
    @abstractmethod
    def produce_commands(self):
        # type: () -> Sequence[str]
        pass

    def _collector(self):
        # type: () -> CommandsCollector
        impl = container.get_bean(CommandsCollector).impl_cls()
        return impl(self)

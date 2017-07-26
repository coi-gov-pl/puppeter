from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from string import Template
from typing import Sequence, Any, Dict

import pkg_resources
import re
from six import with_metaclass, iteritems


class Configurer(with_metaclass(ABCMeta, object)):
    @abstractmethod
    def produce_commands(self):
        # type: () -> Sequence[str]
        pass

    def _collector(self):
        # type: () -> Configurer.CommandsCollector
        return Configurer.CommandsCollector(self)

    class BashTemplate(Template):
        delimiter = '@'
        flags = re.MULTILINE

    class CommandsCollector:

        SHEBANG_REGEX = re.compile('^#!(.*)\n', re.MULTILINE)

        def __init__(self, configurer):
            self.__parts = OrderedDict()  # type: OrderedDict
            self.__configurer = configurer  # type: Configurer

        def collect_from_template(self, description, template, mapping):
            # type: (str, str, Dict[str, Any]) -> Configurer.CommandsCollector
            script = self.__template(template) \
                .substitute(mapping)
            self.__parts[description] = script
            return self

        def collect_from_file(self, description, path):
            # type: (str, str) -> Configurer.CommandsCollector
            script = self.__resource_string(path)
            self.__parts[description] = script
            return self

        def lines(self):
            # type: () -> Sequence[str]
            lines = ['#!/usr/bin/env bash -ex', '']
            i = 1
            for (description, script) in iteritems(self.__parts):
                lines.append('# Part %d: %s' % (i, description))
                lines += self.__strip_shebang(script).split("\n")
                i += 1
            return lines

        def __template(self, path):
            # type: (str) -> Configurer.BashTemplate
            return Configurer.BashTemplate(self.__resource_string(path))

        def __resource_string(self, path):
            # noinspection PyTypeChecker
            return self.__load_resource(pkg_resources.resource_string, self.__configurer, path)\
                .decode("utf-8")

        @staticmethod
        def __load_resource(loader, obj, path):
            mod = Configurer.CommandsCollector.__moduleof(obj)
            return loader(mod, path)

        @staticmethod
        def __moduleof(cls):
            try:
                while True:
                    cls = cls.original_cls()
            except AttributeError:
                cls = cls.__class__
            return cls.__module__

        @staticmethod
        def __strip_shebang(script):
            return re.sub(Configurer.CommandsCollector.SHEBANG_REGEX, "", script)

from __future__ import absolute_import
import os
import re
import pkg_resources

from collections import OrderedDict
from string import Template
from tempfile import NamedTemporaryFile
from typing import Type, Any
from six import iteritems

from puppeter.domain.model.configurer import Configurer, ScriptFormat, CommandsCollector


class AtTemplate(Template):
    delimiter = '@'
    flags = re.MULTILINE


class CommandsCollectorImpl(CommandsCollector):
    __collected = 0

    def __init__(self, configurer):
        self.__parts = OrderedDict()  # type: OrderedDict
        self.__configurer = configurer  # type: Configurer

    def collect_from_template(self, description, template, mapping, format=ScriptFormat.BASH):
        script = self.__template(template) \
            .substitute(mapping)
        self.__parts[description] = dict(script=script, format=format)
        return self

    def collect_from_file(self, description, path, format=ScriptFormat.BASH):
        script = self.__resource_string(path)
        self.__parts[description] = dict(script=script, format=format)
        return self

    def lines(self):
        lines = []
        for (description, script) in iteritems(self.__parts):
            CommandsCollectorImpl.__collected += 1
            lines.append('# Part %d: %s' % (CommandsCollectorImpl.__collected, description))
            lines += self.__get_linesof_script(script)
        return lines

    def __template(self, path):
        # type: (str) -> AtTemplate
        return AtTemplate(self.__resource_string(path))

    def __resource_string(self, path):
        # noinspection PyTypeChecker
        return self.__load_resource(pkg_resources.resource_string, self.__configurer, path) \
            .decode("utf-8")

    @staticmethod
    def __load_resource(loader, obj, path):
        mod = CommandsCollectorImpl.__moduleof(obj)
        return loader(mod, path)

    @staticmethod
    def __moduleof(cls):
        # type: (Type[Any]) -> str
        try:
            while True:
                cls = cls.original_cls()
        except AttributeError:
            pass
        return cls.__module__

    def __get_linesof_script(self, script):
        format = script['format']  # type: ScriptFormat
        shellscript = script['script']  # type: str
        if format is ScriptFormat.PUPPET:
            tpl = self.__load_resource(pkg_resources.resource_string, self, 'puppet-apply.sh') \
                .decode("utf-8")
            f = NamedTemporaryFile(delete=False)
            tmpfilename = f.name
            f.close()
            os.unlink(f.name)
            tpl = AtTemplate(tpl)
            shellscript = tpl.substitute(dict(tmpfilename=tmpfilename, pp=shellscript))

        return shellscript.split("\n")

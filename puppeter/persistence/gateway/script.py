import re

from puppeter.domain.gateway.script import ScriptPostProcessor, ScriptLibrariesConfigurer
from puppeter.domain.model.ordered import Order


class BashScriptPostProcessor(ScriptPostProcessor):

    SHEBANG_REGEX = re.compile('^#!(.*)\n', re.MULTILINE)

    def postprocess(self, commands):
        ln = "\n"
        header = ['#!/usr/bin/env bash', 'set -ex', '']
        stripped = self.__strip_shebang(ln.join(commands)).split(ln)
        return header + stripped

    @staticmethod
    def __strip_shebang(script):
        return re.sub(BashScriptPostProcessor.SHEBANG_REGEX, '', script)


@Order(-1000)
class BashScriptLibrariesConfigurer(ScriptLibrariesConfigurer):
    def produce_commands(self):
        return self._collector()\
            .collect_from_file('Bash script libraries', 'bash-libraries.sh')\
            .lines()

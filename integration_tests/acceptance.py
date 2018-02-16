import re
from os.path import dirname

puppeter_source = dirname(dirname(__file__))
remote_dir = '/usr/src/puppeter-source'


class PuppeterAcceptance:

    PUPPET_VER_3 = re.compile('^3\.\d+\.\d+$')
    PUPPET_VER_4 = re.compile('^4\.\d+\.\d+$')
    PUPPET_VER_5 = re.compile('^5\.\d+\.\d+$')

    def __init__(self, phial):
        self.__phial = phial

    def install_puppeter(self):
        self.__phial.scp(puppeter_source, remote_dir)

        exitcode = self.__script('install-develop.sh')

        assert exitcode == 0

    def run_puppeter(self, answers):
        answersfile = '%s/integration_tests/answers/%s' % (remote_dir, answers)
        exitcode = self.__script('execute.sh', answersfile)

        assert exitcode == 0

    def __script(self, script, arg=''):
        command = 'bash -e %s/integration_tests/scripts/%s %s' % (remote_dir, script, arg)
        exitcode, out, err = self.__phial.exec(command.strip())
        return exitcode

from os.path import dirname

puppeter_source = dirname(dirname(__file__))
remote_dir = '/usr/src/puppeter-source'


class PuppeterAcceptance:

    def __init__(self, phial):
        self.__phial = phial

    def install_puppeter(self):
        self.__phial.scp(puppeter_source, remote_dir)

        status = self.__script('install-develop.sh')

        assert status == 0

    def run_puppeter(self, answers):
        answersfile = '%s/integration_tests/answers/%s' % (remote_dir, answers)
        status = self.__script('execute.sh', answersfile)

        assert status == 0

    def __script(self, script, arg=''):
        command = 'bash -el %s/integration_tests/scripts/%s %s' % (remote_dir, script, arg)
        return self.__phial.exec(command.strip())

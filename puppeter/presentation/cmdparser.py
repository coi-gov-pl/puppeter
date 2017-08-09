import argparse
import sys

import puppeter
from puppeter import container
from puppeter.presentation import App
from puppeter.presentation.app import Options


class _VersionAction(argparse.Action):

    def __init__(self,
                 option_strings,
                 version=None,
                 dest=argparse.SUPPRESS,
                 default=argparse.SUPPRESS,
                 help="show program's version number and exit"):
        super(_VersionAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help)
        self.version = version

    def __call__(self, parser, namespace, values, option_string=None):
        version = self.version
        if version is None:
            version = parser.version
        formatter = parser._get_formatter()
        formatter.add_text(version)
        parser._print_message(formatter.format_help(), sys.stdout)
        parser.exit()


class StdErrArgumentParser(argparse.ArgumentParser):
    def print_help(self, file=None):
        if file is None:
            file = sys.stderr
        self._print_message(self.format_help(), file)


class CommandLineParser(object):
    """CommandLineParser for Puppeter"""
    def __init__(self, argv):
        super(CommandLineParser, self).__init__()
        self.__argv = argv[1:]

    def parse(self):
        # type: () -> App
        parser = StdErrArgumentParser(prog='puppeter', description='Puppeter - an automatic puppet installer',
                                      epilog='By default interactive setup is performed and chosen values can be saved'
                                      ' to answer file.')
        parser.add_argument('--answers', '-a', type=argparse.FileType('r'),
                            metavar='FILE',
                            help='An answer file to be used to perform unattended setup')
        parser.add_argument('--verbose', '-v', action='count',
                            help='Print more verbose output (up to 2 verbosity flags are supported)')
        parser.add_argument('--version', action=_VersionAction, version='%(prog)s ' + puppeter.__version__)
        parser.add_argument('--execute', '-e', action='store_true',
                            help='Executes setup commands instead of printing them')

        parsed = parser.parse_args(self.__argv)
        options = Options(parsed)
        apptype = 'interactive' if options.answers() is None else 'unattended'
        return container.get_named(App, apptype, options=options)

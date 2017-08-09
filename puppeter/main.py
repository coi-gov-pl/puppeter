import sys

from puppeter import container
from puppeter.presentation.cmdparser import CommandLineParser


def main(argv=sys.argv):
    """Entry point for the puppeter application"""
    container.initialize()
    parser = CommandLineParser(argv)
    app = parser.parse()
    app.run()

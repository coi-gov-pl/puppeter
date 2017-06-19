import sys
from puppeter.presentation.cmdparser import CommandLineParser


def main(argv=sys.argv):
    """Entry point for the puppeter application"""
    parser = CommandLineParser(argv)
    app = parser.parse()
    app.run()

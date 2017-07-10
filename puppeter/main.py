import sys

from os.path import dirname

from puppeter import __program__
from puppeter.presentation.cmdparser import CommandLineParser


def main(argv=sys.argv):
    """Entry point for the puppeter application"""
    __load_modules(__program__)
    parser = CommandLineParser(argv)
    app = parser.parse()
    app.run()


__ROOT_DIR = dirname(dirname(__file__))


def __load_modules(module_name):
    import os
    from os.path import join, abspath, isdir, exists

    search = join(abspath(__ROOT_DIR), module_name.replace('.', os.sep))
    lst = os.listdir(search)
    modules = []
    for d in lst:
        subpath = join(search, d)
        if isdir(subpath) and exists(join(subpath, '__init__.py')):
            submodule_name = module_name + '.' + d
            __load_modules(submodule_name)
            modules.append(submodule_name)
    # load the modules
    for module_name_to_import in modules:
        __import__(module_name_to_import)

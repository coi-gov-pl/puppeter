import logging

from logging import Logger
from typing import Type

# The version of the app
__version__ = '0.5.3'
__program__ = 'puppeter'


def get_logger(cls):
    # type: (Type) -> Logger
    name = __fullname(cls)
    return logging.getLogger(name)


def __fullname(cls):
    return cls.__module__ + "." + cls.__name__


if __name__ == '__main__':
    from puppeter.main import main
    main()

import logging

from logging import Logger
from typing import Type

# The version of the app
__version__ = '0.8.1'
__program__ = 'puppeter'


def get_logger(cls):
    # type: (Type) -> Logger
    name = __fullname(cls)
    return logging.getLogger(name)


def __fullname(cls):
    return cls.__module__ + "." + cls.__name__

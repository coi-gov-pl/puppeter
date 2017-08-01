import logging
import os
import sys
from abc import abstractmethod, ABCMeta
from logging import StreamHandler
from logging.handlers import SysLogHandler
from typing import IO, Any

from six import with_metaclass

import puppeter
from puppeter import container
from puppeter.domain.facter import Facter
from puppeter.domain.gateway.answers import AnswersProcessor
from puppeter.domain.model.answers import Answers
from puppeter.domain.model.osfacts import OsFamily


class Options:
    def __init__(self, namespace):
        self.__answers = namespace.answers  # type: IO[Any]
        self.__verbose = namespace.verbose  # type: int
        self.__execute = namespace.execute  # type: bool

    def answers(self):
        # type: () -> IO[Any]
        return self.__answers

    def verbose(self):
        # type: () -> int
        return self.__verbose

    def execute(self):
        # type: () -> bool
        return self.__execute


class App(with_metaclass(ABCMeta, object)):

    def __init__(self, options):
        self._options = options  # type: Options

    def run(self):
        root = logging.getLogger()
        level = self.__get_log_level(self._options.verbose())
        root.setLevel(level)
        handlers = (self.__syslog_handler(), self.__stderr_handler())
        for hndl in handlers:
            root.addHandler(hndl)
        answers = self._collect_answers()
        self.__process(answers)

    @abstractmethod
    def _collect_answers(self):
        # type: () -> Answers
        pass

    def __process(self, answers):
        # type: (Answers) -> None
        processor = container.get(AnswersProcessor, options=self._options)  # type: AnswersProcessor
        processor.process(answers)

    @staticmethod
    def __stderr_handler():
        # type: () -> logging.Handler
        handler = StreamHandler(stream=sys.stderr)
        fmt = '# %(levelname)s: %(message)s'
        handler.setFormatter(ColoredFormatter(fmt=fmt))
        handler.setLevel(logging.NOTSET)
        return handler

    @staticmethod
    def __syslog_handler():
        # type: () -> logging.Handler
        osfamily = Facter.get(OsFamily)
        if osfamily in (OsFamily.Debian, OsFamily.RedHat, OsFamily.Suse):
            try:
                handler = SysLogHandler(address='/dev/log')
            except EnvironmentError:
                handler = SysLogHandler()
        else:
            handler = SysLogHandler()
        fmt = puppeter.__program__ + '[%(process)d]: %(levelname)s %(name)s - %(message)s'
        handler.setFormatter(logging.Formatter(fmt=fmt))
        handler.setLevel(logging.INFO)
        return handler

    @staticmethod
    def __get_log_level(verbosity):
        if verbosity is None:
            verbosity = 0
        if verbosity > 2:
            verbosity = 2
        levels = {
            0: logging.WARNING,
            1: logging.INFO,
            2: logging.DEBUG
        }
        return levels[verbosity]


def color_code(fg, bg=None):
    if bg is not None:
        return FGBG_COLOR_SEQ % (fg, bg)
    else:
        return FG_COLOR_SEQ % fg


RESET_SEQ = "\033[0m"
FG_COLOR_SEQ = "\033[38;5;%dm"
FGBG_COLOR_SEQ = "\033[38;5;%d;48;5;%dm"
# ref: https://unix.stackexchange.com/a/124409/145501
COLORS = {
    'WARNING': color_code(fg=226),
    'INFO': color_code(fg=155),
    'DEBUG': color_code(fg=244),
    'CRITICAL': color_code(fg=219, bg=196),
    'ERROR': color_code(fg=196)
}
try:
    SUPPORTS_256_COLORS = os.environ['XTERM_256_COLORS'] == '1'
except KeyError:
    SUPPORTS_256_COLORS = False


class ColoredFormatter(logging.Formatter):

    def __init__(self, fmt, use_color=SUPPORTS_256_COLORS):
        logging.Formatter.__init__(self, fmt=fmt)
        self.use_color = use_color

    def format(self, record):
        formatted = logging.Formatter.format(self, record)
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            formatted = COLORS[levelname] + formatted + RESET_SEQ
        return formatted

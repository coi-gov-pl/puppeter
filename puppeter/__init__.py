import logging

# The version of the app
__version__ = '0.1.0.dev0'
__program__ = 'puppeter'


def get_logger(cls):
    name = __fullname(cls)
    return logging.getLogger(name)


def __fullname(cls):
    return cls.__module__ + "." + cls.__name__


if __name__ == '__main__':
    from puppeter.main import main
    main()

from os.path import dirname
from typing import Type, TypeVar, Any, List, Sequence

from puppeter import __program__

T = TypeVar('T')


def initialize():
    __load_modules(__program__)


def Named(bean_name):
    def named_decorator(cls):
        cls.__bean_name = bean_name

        class NamedBean(cls):
            def __init__(self, *args, **kwargs):
                self.wrapped = cls(*args, **kwargs)

            @staticmethod
            def bean_name():
                return bean_name

            @staticmethod
            def original_cls():
                return cls

            def __repr__(self):
                return '@Named(\'%s\') %s' % (bean_name, repr(self.wrapped))

            def __getattr__(self, name):
                return getattr(self.wrapped, name)
        return NamedBean
    return named_decorator


def bind(cls, impl_cls):
    # type: (Type[T], Type[T]) -> None
    beans = __get_all_beans(cls)
    beans.append(__Bean(cls, impl_cls=impl_cls))


def bind_to_instance(cls, impl):
    # type: (Type[T], T) -> None
    beans = __get_all_beans(cls)
    beans.append(__Bean(cls, impl=impl))


def get_all(cls, *args, **kwargs):
    # type: (Type[T], str, Any, Any) -> Sequence[T]
    beans = __get_all_beans(cls)
    try:
        return __instantinate_beans(beans, *args, **kwargs)
    except Exception:
        return tuple()


def get(cls, *args, **kwargs):
    # type: (Type[T], Any, Any) -> T
    beans = __get_all_beans(cls)
    if len(beans) == 1:
        return beans[0].impl(*args, **kwargs)
    else:
        impls = list(map(lambda bean: bean.impl_cls_name(), beans))
        raise ValueError('Zero or more then one implementation found for class %s. '
                         'Found those implementations: %s. '
                         'Use @Named beans and get_named() function!' % (cls, impls))


def get_named(cls, bean_name, *args, **kwargs):
    # type: (Type[T], str, Any, Any) -> T
    for bean in __get_all_beans(cls):
        if bean.name() == bean_name:
            return bean.impl(*args, **kwargs)
    raise ValueError('Bean named %s has not been found for class %s' % (bean_name, cls))


def get_all_with_name_starting_with(cls, name_prefix, *args, **kwargs):
    # type: (Type[T], str, Any, Any) -> Sequence[T]
    beans = []
    for bean in __get_all_beans(cls):
        if bean.name().startswith(name_prefix):
            beans.append(bean)
    return __instantinate_beans(beans, *args, **kwargs)


def get_bean(cls):
    # type: (Type[T]) -> __Bean
    return __get_all_beans(cls)[0]

__ROOT_DIR = dirname(dirname(__file__))
__beans = {}


def __instantinate_beans(beans, *args, **kwargs):
    # type: (Sequence[__Bean], Any, Any) -> Sequence[T]
    impls = tuple(map(lambda bean: bean.impl(*args, **kwargs), beans))  # type: Sequence[T]
    return impls


def __get_all_beans(cls):
    # type: (Type[T]) -> List[__Bean]
    try:
        return __beans[cls]
    except KeyError:
        lst = []
        __beans[cls] = lst
        return lst


class __Bean:
    def __init__(self, cls, impl=None, impl_cls=None):
        if impl is None and impl_cls is None:
            raise Exception('20170707:164636')
        self.__cls = cls
        self.__impl = impl
        self.__impl_cls = impl_cls

    def __repr__(self):
        name = self.name()
        if name is not None:
            return 'Bean named \'%s\' of %s' % (name, repr(self.impl_cls()))
        else:
            return 'Bean of %s' % repr(self.impl_cls())

    def impl_cls_name(self):
        return self.__impl_cls

    def impl_cls(self):
        if self.__impl is None:
            return self.__impl_cls
        else:
            return self.__impl.__class__

    def name(self):
        # type: () -> str | None
        try:
            return self.impl_cls().bean_name()
        except AttributeError:
            return None

    def impl(self, *args, **kwargs):
        if self.__impl is None:
            self.__impl = self.__impl_cls(*args, **kwargs)
        return self.__impl


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

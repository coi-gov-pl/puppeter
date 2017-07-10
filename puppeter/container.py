def Named(bean_name):
    def named_decorator(cls):
        class NamedBean(cls):
            def __init__(self, *args):
                self.wrapped = cls(*args)

            def bean_name(self):
                return bean_name

            def __repr__(self):
                return '@Named(\'%s\') %s' % (bean_name, repr(self.wrapped))

            def __getattr__(self, name):
                return getattr(self.wrapped, name)
        return NamedBean
    return named_decorator


def bind(cls, impl_cls):
    beans = __get_all_beans(cls)
    beans.append(__Bean(cls, impl_cls=impl_cls))


def bind_to_instance(cls, impl):
    beans = __get_all_beans(cls)
    beans.append(__Bean(cls, impl=impl))


def get_all(cls):
    beans = __get_all_beans(cls)
    try:
        return tuple(map(lambda bean: bean.impl(), beans))
    except Exception:
        return tuple()


def get(cls):
    beans = __get_all_beans(cls)
    if len(beans) == 1:
        return beans[0].impl()
    else:
        impls = list(map(lambda bean: bean.impl_cls_name(), beans))
        raise ValueError('Zero or more then one implementation found for class %s. '
                         'Found those implementations: %s. '
                         'Use @Named beans and get_named() function!' % (cls, impls))


def get_named(cls, bean_name):
    for bean in __get_all_beans(cls):
        if bean.name() == bean_name:
            return bean.impl()
    raise ValueError('Bean named %s has not been found for class %s' % (bean_name, cls))


__beans = {}


def __get_all_beans(cls):
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

    def impl_cls_name(self):
        return self.__impl_cls

    def name(self):
        return self.impl().bean_name()

    def impl(self):
        if self.__impl is None:
            self.__impl = self.__impl_cls()
        return self.__impl

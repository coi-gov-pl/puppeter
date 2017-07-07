def Named(bean_name):
    def named_decorator(cls):
        class NamedBean(cls):
            def __init__(self, *args):
                self.wrapped = cls(*args)

            def get_bean_name(self):
                return bean_name

            def __getattr__(self, name):
                return getattr(self.wrapped, name)
        return NamedBean
    return named_decorator


def bind(cls, impl_cls):
    try:
        lst = __beans[cls]
    except:
        lst = []
        __beans[cls] = lst
    lst.append(__Bean(cls, impl_cls=impl_cls))


def bind_to_instance(cls, impl):
    try:
        lst = __beans[cls]
    except:
        lst = []
        __beans[cls] = lst
    lst.append(__Bean(cls, impl=impl))


def get_all(cls):
    try:
        beans = __beans[cls]
        return map(lambda bean: bean.impl, beans)
    except:
        return []


def get(cls, bean_name):
    for bean in __get_all_beans(cls):
        if bean.name() == bean_name:
            return bean.impl()
    raise ValueError('Bean named %s has not been found for class %s' % (bean_name, cls))


__beans = {}


def __get_all_beans(cls):
    try:
        return __beans[cls]
    except:
        return []


class __Bean:
    def __init__(self, cls, impl=None, impl_cls=None):
        if impl is None and impl_cls is None:
            raise Exception('20170707:164636')
        self.__cls = cls
        self.__impl = impl
        self.__impl_cls = impl_cls

    def name(self):
        if self.__impl is not None:
            return self.__impl.get_bean_name()
        else:
            return self.__impl_cls().get_bean_name()

    def impl(self):
        if self.__impl is not None:
            return self.__impl
        else:
            return self.__impl_cls()

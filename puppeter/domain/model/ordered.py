def Order(order):
    # type: (int) -> callable
    def order_decorator(cls):
        cls.__order = order

        class Ordered(cls):
            def __init__(self, *args, **kwargs):
                self.wrapped = cls(*args, **kwargs)

            @staticmethod
            def order():
                return cls.__order

            @staticmethod
            def original_cls():
                return cls

            def __repr__(self):
                return '@Order(\'%d\') %s' % (cls.__order, repr(self.wrapped))

            def __getattr__(self, name):
                return getattr(self.wrapped, name)
        return Ordered
    return order_decorator

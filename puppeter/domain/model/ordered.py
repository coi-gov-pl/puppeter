def Order(order):
    # type: (int) -> callable
    def order_decorator(cls):

        class Ordered(cls):
            def __init__(self, *args, **kwargs):
                self.wrapped = cls(*args, **kwargs)

            @staticmethod
            def order():
                return order

            @staticmethod
            def original_cls():
                return cls

            def __repr__(self):
                return '@Order(\'%d\') %s' % (order, repr(self.wrapped))

            def __getattr__(self, name):
                return getattr(self.wrapped, name)
        return Ordered
    return order_decorator

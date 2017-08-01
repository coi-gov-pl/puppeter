from typing import Type, Callable, TypeVar

T = TypeVar('T')


def default(x, e, y):
    # type: (Callable[[], T], Type[Exception], T) -> T
    try:
        return x()
    except e:
        return y

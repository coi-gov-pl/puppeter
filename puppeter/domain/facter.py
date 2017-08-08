from typing import TypeVar, Type, Callable, Optional

T = TypeVar('T')


class Facter:
    """
    A nano version of Puppet's Facter
    """
    _facts = {}
    __resolvers = {}

    @staticmethod
    def get(enumvar):
        # type: (Type[T]) -> Optional[T]
        if enumvar in Facter._facts:
            return Facter._facts[enumvar]
        elif enumvar in Facter.__resolvers:
            resolved = Facter.__resolve(enumvar)
            if resolved is not None:
                Facter._facts[enumvar] = resolved
            return resolved
        else:
            return None

    @staticmethod
    def set(enumvar, resolver):
        # type: (Type[T], Callable[[], T]) -> None
        if enumvar not in Facter.__resolvers:
            Facter.__resolvers[enumvar] = []
        Facter.__resolvers[enumvar].append(resolver)

    @staticmethod
    def __resolve(enumvar):
        # type: (Type[T]) -> Optional[T]
        for resolver in Facter.__resolvers[enumvar]:
            resolved = resolver()
            if resolved is not None:
                return resolved
        return None

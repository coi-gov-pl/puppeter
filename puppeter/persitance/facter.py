class Facter:
    """
    A nano version of Puppet's Facter
    """
    __facts = {}
    __resolvers = {}

    @staticmethod
    def get(enumvar):
        if enumvar in Facter.__facts:
            return Facter.__facts[enumvar]
        elif enumvar in Facter.__resolvers:
            resolved = Facter.__resolve(enumvar)
            if resolved is not None:
                Facter.__facts[enumvar] = resolved
            return resolved
        else:
            return None

    @staticmethod
    def set(enumvar, resolver):
        if enumvar not in Facter.__resolvers:
            Facter.__resolvers[enumvar] = []
        Facter.__resolvers[enumvar].append(resolver)

    @staticmethod
    def __resolve(enumvar):
        for resolver in Facter.__resolvers[enumvar]:
            resolved = resolver()
            if resolved is not None:
                return resolved
        return None

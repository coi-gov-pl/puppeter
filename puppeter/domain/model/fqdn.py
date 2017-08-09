from typing import Optional

from puppeter.domain.model.withoptions import WithOptions


class FqdnConfiguration(WithOptions):
    def __init__(self, fqdn='localhost.localdomain'):
        self.__fqdn = fqdn.strip()

    def raw_options(self):
        return self.fqdn()

    def read_raw_options(self, options):
        self.__fqdn = str(options).strip()

    def fqdn(self):
        # type: () -> str
        return self.__fqdn

    def hostname(self):
        # type: () -> str
        return self.fqdn().split('.')[0]

    def domain(self):
        # type: () -> Optional[str]
        domain = '.'.join(self.fqdn().split('.')[1:])
        domain = None if domain == '' else domain
        return domain

    def has_domain(self):
        # type: () -> bool
        return self.domain() is not None

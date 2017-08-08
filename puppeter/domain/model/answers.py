from typing import Optional

from puppeter.domain.model.fqdn import FqdnConfiguration
from puppeter.domain.model.installer import Installer


class Answers:
    def __init__(self,
                 installer=None,
                 fqdn_configuration=None,
                 timesync_configuration=None,
                 csrattrs_configuration=None):
        self.__installer = installer  # type: Optional[Installer]
        self.__fqdn_configuration = fqdn_configuration  # type: Optional[FqdnConfiguration]
        self.__timesync_configuration = timesync_configuration
        self.__csrattrs_configuration = csrattrs_configuration

    def installer(self):
        # type: () -> Optional[Installer]
        return self.__installer

    def fqdn_configuration(self):
        # type: () -> Optional[FqdnConfiguration]
        return self.__fqdn_configuration

    def timesync_configuration(self):
        return self.__timesync_configuration

    def csrattrs_configuration(self):
        return self.__csrattrs_configuration

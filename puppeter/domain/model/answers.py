from puppeter.domain.model.installer import Installer  # NOQA


class Answers:
    def __init__(self,
                 installer=None,
                 fqdn_configurator=None,
                 timesync_configurator=None,
                 csrattrs_configurator=None):
        self.__installer = installer
        self.__fqdn_configurator = fqdn_configurator
        self.__timesync_configurator = timesync_configurator
        self.__csrattrs_configurator = csrattrs_configurator

    def installer(self):
        # type: () -> Installer
        return self.__installer

    def fqdn_configurator(self):
        return self.__fqdn_configurator

    def timesync_configurator(self):
        return self.__timesync_configurator

    def csrattrs_configurator(self):
        return self.__csrattrs_configurator

class Answers:
    def __init__(self,
                 puppet_installer=None,
                 fqdn_configurator=None,
                 timesync_configurator=None,
                 csrattrs_configurator=None):
        self.__puppet_installer = puppet_installer
        self.__fqdn_configurator = fqdn_configurator
        self.__timesync_configurator = timesync_configurator
        self.__csrattrs_configurator = csrattrs_configurator

    def puppet_installer(self):
        return self.__puppet_installer

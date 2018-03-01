from puppeter import container
from puppeter.domain.model.installer import Collection4xInstaller,\
    Collection3xInstaller,\
    Collection5xInstaller,\
    Installer,\
    RubygemsInstaller, \
    SystemInstaller

# TODO: implement GEM installer - https://github.com/coi-gov-pl/puppeter/issues/18
# container.bind(Installer, RubygemsInstaller)
container.bind(Installer, SystemInstaller)
container.bind(Installer, Collection3xInstaller)
container.bind(Installer, Collection4xInstaller)
container.bind(Installer, Collection5xInstaller)

from puppeter import container
from puppeter.domain.model.installer import Collection4xInstaller,\
    Collection3xInstaller,\
    Collection5xInstaller,\
    Installer,\
    RubygemsInstaller

container.bind(Installer, RubygemsInstaller)
container.bind(Installer, Collection3xInstaller)
container.bind(Installer, Collection4xInstaller)
container.bind(Installer, Collection5xInstaller)

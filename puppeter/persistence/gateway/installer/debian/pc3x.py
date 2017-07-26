from puppeter.container import Named
from puppeter.domain.facter import Facter
from puppeter.domain.model.ordered import Order
from puppeter.domain.model.osfacts import OperatingSystemCodename
from puppeter.persistence.gateway.installer.debian.base import BaseDebianConfigurer


@Named('pc3x-debian')
@Order(100)
class DebianPC3xConfigurer(BaseDebianConfigurer):
    def __init__(self, installer):
        BaseDebianConfigurer.__init__(self, installer)

    def _collect_repo(self, collector):
        codename = Facter.get(OperatingSystemCodename)
        collector.collect_from_template(
            'Puppet Package Repository setup (Puppet OSS 3.x)',
            'pc3x-repo.sh',
            dict(codename=codename)
        )

    def _collect_agent(self, collector):
        collector.collect_from_file('Puppet agent setup', 'puppet3xagent.sh')

    def _collect_server(self, collector):
        collector.collect_from_file('PuppetMaster setup', 'puppetmaster.sh')

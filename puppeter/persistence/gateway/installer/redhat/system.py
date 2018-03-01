from puppeter.container import Named
from puppeter.domain.facter import Facter
from puppeter.domain.model.ordered import Order
from puppeter.domain.model.osfacts import OperatingSystemRelease
from puppeter.persistence.gateway.installer.redhat.base import BaseRedHatConfigurer


@Named('system-redhat')
@Order(100)
class RedHatSystemConfigurer(BaseRedHatConfigurer):
    def _collect_repo(self, collector):
        rel = Facter.get(OperatingSystemRelease)
        collector.collect_from_file('Ensure EPEL is active', 'ensure-epel-{rel}.sh'.format(rel=rel.major()))

    def _collect_agent(self, collector):
        collector.collect_from_file('Puppet agent setup', 'puppet-system.sh')

    def _collect_server(self, collector):
        collector.collect_from_file('Puppet Master setup', 'puppetmaster-system.sh')

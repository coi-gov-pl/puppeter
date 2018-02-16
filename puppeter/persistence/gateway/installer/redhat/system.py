from puppeter.container import Named
from puppeter.domain.model.ordered import Order
from puppeter.persistence.gateway.installer.redhat.base import BaseRedHatConfigurer


@Named('system-redhat')
@Order(100)
class RedHatSystemConfigurer(BaseRedHatConfigurer):
    def _collect_repo(self, collector):
        pass

    def _collect_agent(self, collector):
        collector.collect_from_file('Puppet agent setup', 'puppet-system.sh')

    def _collect_server(self, collector):
        collector.collect_from_file('Puppet Master setup', 'puppetmaster-system.sh')

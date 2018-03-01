from puppeter.container import Named
from puppeter.domain.model.ordered import Order
from puppeter.persistence.gateway.installer.debian.base import BaseDebianConfigurer


@Named('system-debian')
@Order(100)
class DebianSystemConfigurer(BaseDebianConfigurer):
    def _collect_repo(self, collector):
        pass

    def _is_wget_needed(self):
        return False

    def _collect_agent(self, collector):
        collector.collect_from_file('Puppet agent setup', 'puppet-system.sh')

    def _collect_server(self, collector):
        collector.collect_from_file('Puppet Master setup', 'puppetmaster-system.sh')

from abc import ABCMeta

from six import with_metaclass

from puppeter.persistence.gateway.installer.debian.base import BaseDebianConfigurer


class AfterPuppet4xConfigurer(with_metaclass(ABCMeta, BaseDebianConfigurer)):
    def __init__(self, installer):
        super(AfterPuppet4xConfigurer, self).__init__(installer)

    def _collect_agent(self, collector):
        collector.collect_from_file('Puppet Agent setup', 'puppetagent.sh')

    def _collect_server(self, collector):
        collector.collect_from_file('Puppet Server setup', 'puppetserver.sh')

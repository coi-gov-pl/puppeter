from abc import ABCMeta, abstractmethod

from six import with_metaclass
from typing import Sequence
from puppeter.domain.facter import Facter
from puppeter.domain.gateway.fqdn import FqdnSetterGateway
from puppeter.domain.model.configurer import Configurer, CommandsCollector, ScriptFormat
from puppeter.domain.model.fqdn import FqdnConfiguration
from puppeter.domain.model.ordered import Order
from puppeter.domain.model.osfacts import OsFamily, Docker

FQDN_ORDER = 200


class LinuxFQDNConfigurer(with_metaclass(ABCMeta, Configurer)):
    def __init__(self, fqdn):
        self._fqdn = fqdn  # type: FqdnConfiguration

    def produce_commands(self):
        # type: () -> Sequence[str]
        collector = self._collector()
        collector.collect_from_template(
            'Setting FQDN (Fully Qualified Domain Name)',
            'set-fqdn.sh',
            self._mapping()
        )
        self._persist_change(collector)
        return collector.lines()

    @abstractmethod
    def _persist_change(self, collector):
        # type: (CommandsCollector) -> None
        pass

    def _mapping(self):
        return dict(fqdn=self._fqdn.fqdn(), hostname=self._fqdn.hostname())


@Order(FQDN_ORDER)
class RedHatFQDNConfigurer(LinuxFQDNConfigurer):
    def _persist_change(self, collector):
        collector.collect_from_template(
            'Persist FQDN to be available after reboot',
            'redhat-persist-fqdn.pp',
            self._mapping(),
            format=ScriptFormat.PUPPET
        )


@Order(FQDN_ORDER)
class DebianFQDNConfigurer(LinuxFQDNConfigurer):
    def _persist_change(self, collector):
        collector.collect_from_template(
            'Persist FQDN to be available after reboot',
            'debian-persist-fqdn.pp',
            self._mapping(),
            format=ScriptFormat.PUPPET
        )


class FqdnSetterGatewayImpl(FqdnSetterGateway):
    def process_fully_qualified_domain_name(self, fqdn):
        # type: (FqdnConfiguration) -> Sequence[Configurer]
        if Facter.get(Docker) == Docker.YES:
            raise NotImplementedError('Can\'t set FQDN when running inside Docker!')
        osfamily = Facter.get(OsFamily)
        try:
            return {
                OsFamily.RedHat: [RedHatFQDNConfigurer(fqdn)],
                OsFamily.Debian: [DebianFQDNConfigurer(fqdn)]
            }[osfamily]
        except KeyError as ex:
            raise NotImplementedError(ex, 'Unsupported OS family %s for setting FQDN' % osfamily)

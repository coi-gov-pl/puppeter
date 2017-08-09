from puppeter.container import Named
from puppeter.domain.facter import Facter
from puppeter.domain.model.ordered import Order
from puppeter.domain.model.osfacts import OperatingSystemCodename
from puppeter.persistence.gateway.installer.debian.after4x import AfterPuppet4xConfigurer


@Named('pc4x-debian')
@Order(100)
class DebianPC4xConfigurer(AfterPuppet4xConfigurer):

    def __init__(self, installer):
        AfterPuppet4xConfigurer.__init__(self, installer)

    def _collect_repo(self, collector):
        codename = Facter.get(OperatingSystemCodename)
        collector.collect_from_template(
            'Puppet Labs Collection Repository (PC1) setup (Puppet OSS 4.x)',
            'pc4x-repo.sh',
            dict(codename=codename)
        )

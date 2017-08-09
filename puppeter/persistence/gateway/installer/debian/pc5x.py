from puppeter.container import Named
from puppeter.domain.facter import Facter
from puppeter.domain.model.ordered import Order
from puppeter.domain.model.osfacts import OperatingSystemCodename
from puppeter.persistence.gateway.installer.debian.after4x import AfterPuppet4xConfigurer


@Named('pc5x-debian')
@Order(100)
class DebianPC5xConfigurer(AfterPuppet4xConfigurer):

    def __init__(self, installer):
        AfterPuppet4xConfigurer.__init__(self, installer)

    def _collect_repo(self, collector):
        codename = Facter.get(OperatingSystemCodename)
        collector.collect_from_template(
            'Puppet Platform Repository setup (Puppet OSS 5.x)',
            'pc5x-repo.sh',
            dict(codename=codename)
        )

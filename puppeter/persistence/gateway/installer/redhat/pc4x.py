from puppeter.container import Named
from puppeter.domain.model.ordered import Order
from puppeter.persistence.gateway.installer.redhat.after4x import AfterPuppet4xConfigurer


@Named('pc4x-redhat')
@Order(100)
class RedHatPC4xConfigurer(AfterPuppet4xConfigurer):

    def __init__(self, installer):
        AfterPuppet4xConfigurer.__init__(self, installer)

    def _repo_script_path_el5(self):
        return 'pc4x-el5-repo.sh'

    def _repo_script_path(self):
        return 'pc4x-repo.sh'

    def _repo_setup_title(self):
        return 'Puppet Labs Collection Repository (PC1) setup (Puppet OSS 4.x)'

from puppeter.container import Named
from puppeter.domain.facter import Facter
from puppeter.domain.model.ordered import Order
from puppeter.domain.model.osfacts import OperatingSystemRelease, OperatingSystem
from puppeter.persistence.gateway.installer.redhat.base import BaseRedHatConfigurer


@Named('pc3x-redhat')
@Order(100)
class RedHatPC3xConfigurer(BaseRedHatConfigurer):

    def __init__(self, installer):
        BaseRedHatConfigurer.__init__(self, installer)

    def _collect_repo(self, collector):
        major = Facter.get(OperatingSystemRelease).major()
        os = Facter.get(OperatingSystem)
        if os == OperatingSystem.Fedora:
            abbr = 'fedora'
        else:
            abbr = 'el'
        mapping = dict(major=major, abbr=abbr)
        if ('%s-%s' % (abbr, major)) == 'el-5':
            script = 'pc3x-el5-repo.sh'
        else:
            script = 'pc3x-repo.sh'
        title = 'Puppet Package Repository setup (Puppet OSS 3.x)'
        collector.collect_from_template(title, script, mapping)

    def _collect_agent(self, collector):
        collector.collect_from_file('Puppet agent setup', 'puppet3xagent.sh')

    def _collect_server(self, collector):
        collector.collect_from_file('PuppetMaster setup', 'puppetmaster.sh')

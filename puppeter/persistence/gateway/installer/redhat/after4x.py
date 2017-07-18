from abc import ABCMeta, abstractmethod

from six import with_metaclass

from puppeter.domain.facter import Facter
from puppeter.domain.model.osfacts import OperatingSystemRelease, OperatingSystem
from puppeter.persistence.gateway.installer.redhat.base import BaseRedHatConfigurer


class AfterPuppet4xConfigurer(with_metaclass(ABCMeta, BaseRedHatConfigurer)):
    def __init__(self, installer):
        super(AfterPuppet4xConfigurer, self).__init__(installer)

    def _collect_agent(self, collector):
        collector.collect_from_file('Puppet Agent setup', 'puppetagent.sh')

    def _collect_server(self, collector):
        collector.collect_from_file('Puppet Server setup', 'puppetserver.sh')

    def _collect_repo(self, collector):
        major = Facter.get(OperatingSystemRelease).major()
        os = Facter.get(OperatingSystem)
        if os == OperatingSystem.Fedora:
            abbr = 'fedora'
        else:
            abbr = 'el'
        mapping = dict(major=major, abbr=abbr)
        if ('%s-%s' % (abbr, major)) == 'el-5':
            script = self._repo_script_path_el5()
        else:
            script = self._repo_script_path()
        collector.collect_from_template(self._repo_setup_title(), script, mapping)

    @abstractmethod
    def _repo_setup_title(self):
        raise NotImplementedError()

    @abstractmethod
    def _repo_script_path_el5(self):
        raise NotImplementedError()

    @abstractmethod
    def _repo_script_path(self):
        raise NotImplementedError()

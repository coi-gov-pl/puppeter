from typing import Union

from puppeter.container import NamedBean
from puppeter.domain.model.installer import WithOptions, After4xCollectionInstaller, JavaMemorySpec


def test_rubygems_installer_named_bean():
    # given
    from puppeter.domain.model.installer import RubygemsInstaller
    installer = RubygemsInstaller()
    # when
    bean_name = installer.bean_name()
    # then
    assert bean_name is 'gem'


def test_rubygems_installer_values():
    # given
    from puppeter.domain.model.installer import RubygemsInstaller, Mode
    installer = RubygemsInstaller()
    # when
    version = installer.version()
    mode = installer.mode()
    # then
    assert version is None
    assert mode is Mode.Agent


def test_rubygems_installer_raw_options():
    # given
    from puppeter.domain.model.installer import RubygemsInstaller
    installer = RubygemsInstaller()
    # when
    options = installer.raw_options()
    # then
    assert options == {
        'mode': 'Agent',
        'version': None,
        'type': 'gem'
    }


def test_rubygems_installer_read_raw_options():
    # given
    from puppeter.domain.model.installer import RubygemsInstaller, Mode
    installer = RubygemsInstaller()
    # when
    installer.read_raw_options({
        'mode': 'Server',
        'version': '~> 3'
    })
    version = installer.version()
    mode = installer.mode()
    # then
    assert version is '~> 3'
    assert mode is Mode.Server
    assert installer.is_after_4x() is False


def test_rubygems_installer_read_raw_options_invalid():
    # given
    from puppeter.domain.model.installer import RubygemsInstaller, Mode
    installer = RubygemsInstaller()
    # when
    installer.read_raw_options({})
    installer.read_raw_options({
        'invalid-key': 'Server',
        'version': '~> 4'
    })
    mode = installer.mode()

    # then
    assert mode is Mode.Agent
    assert installer.is_after_4x()


def test_getting_impl_from_container():
    # given
    from puppeter.domain.model.installer import Installer, Mode
    from puppeter import container

    # when
    installer = container.get_named(Installer, 'pc3x')  # type: Union[Installer, NamedBean]

    # then
    assert installer.mode() is Mode.Agent
    assert installer.bean_name() is 'pc3x'


def test_getting_all_impls_from_container():
    # given
    from puppeter.domain.model.installer import Installer, Collection5xInstaller
    from puppeter import container

    # when
    installers = container.get_all(Installer)

    # then
    assert len(installers) >= 4
    assert len(tuple(filter(lambda cls: isinstance(cls, Collection5xInstaller), installers))) == 1


def test_with_options():
    # given
    class TestA(WithOptions):
        def read_raw_options(self, options):
            WithOptions.read_raw_options(self, options)

        def raw_options(self):
            return WithOptions.raw_options(self)

    # when
    testa = TestA()

    # then
    assert testa is not None
    assert testa.raw_options() is None
    assert testa.read_raw_options({}) is None


def test_pc4x_jvmargs_read():
    # given
    from puppeter.domain.model.installer import Installer
    from puppeter import container

    # when
    installer = container.get_named(Installer, 'pc4x')  # type: After4xCollectionInstaller
    installer.read_raw_options({
        'mode': 'Server',
        'puppetserver': {
            'jvm': {
                'memory': {
                    'heap': {
                        'min': '256m',
                        'max': '512m'
                    }
                },
                'args': [
                    '-XX:+UseConcMarkSweepGC',
                    '-XX:+CMSParallelRemarkEnabled'
                ]
            }
        }
    })

    # then
    assert len(installer.puppetserver_jvm_args()) is 2
    assert '-XX:+UseConcMarkSweepGC' in installer.puppetserver_jvm_args()
    assert '-XX:+CMSParallelRemarkEnabled' in installer.puppetserver_jvm_args()
    assert installer.puppetserver_jvm_memory().heap_maximum() == '512m'
    assert installer.puppetserver_jvm_memory().heap_minimum() == '256m'


def test_pc4x_jvmargs_write():
    # given
    from puppeter.domain.model.installer import Installer
    from puppeter import container
    installer = container.get_named(Installer, 'pc4x')  # type: After4xCollectionInstaller

    # when
    installer.read_raw_options({
        'mode': 'Server',
        'puppetserver': {
            'jvm': {
                'memory': {
                    'heap': {
                        'max': '434m'
                    },
                    'metaspace': {
                        'max': '11k'
                    }
                },
                'args': [
                    '-XX:+UseConcMarkSweepGC'
                ]
            }
        }
    })
    raw = installer.raw_options()

    # then
    assert raw['puppetserver']['jvm']['memory']['metaspace']['max'] == '11k'
    assert installer.puppetserver_jvm_memory().metaspace_maximum() == '11k'
    assert installer.puppetserver_jvm_memory().heap_minimum() == '434m'
    assert installer.puppetserver_jvm_memory().heap_maximum() == '434m'
    assert len(installer.puppetserver_jvm_args()) is 1
    assert '-XX:+UseConcMarkSweepGC' in installer.puppetserver_jvm_args()


def test_pc3x_is_after4x():
    # given
    from puppeter.domain.model.installer import Installer
    from puppeter import container
    installer = container.get_named(Installer, 'pc3x')

    # then
    assert installer.is_after_4x() is False

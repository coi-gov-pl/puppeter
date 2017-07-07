def test_rubygems_installer_named_bean():
    # given
    from puppeter.domain.puppet_installer import RubygemsInstaller
    installer = RubygemsInstaller()
    # when
    bean_name = installer.get_bean_name()
    # then
    assert bean_name is 'gem'


def test_rubygems_installer_values():
    # given
    from puppeter.domain.puppet_installer import RubygemsInstaller, Mode
    installer = RubygemsInstaller()
    # when
    version = installer.version()
    mode = installer.mode()
    # then
    assert version is None
    assert mode is Mode.Agent


def test_rubygems_installer_raw_options():
    # given
    from puppeter.domain.puppet_installer import RubygemsInstaller
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
    from puppeter.domain.puppet_installer import RubygemsInstaller, Mode
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


def test_getting_impl_from_container():
    # given
    from puppeter.domain.puppet_installer import Installer, Mode
    from puppeter import container

    # when
    installer = container.get(Installer, 'pc3x')

    # then
    assert installer.mode() is Mode.Agent
    assert installer.get_bean_name() is 'pc3x'

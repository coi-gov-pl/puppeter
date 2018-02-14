import pytest

from puppeter.domain.model.osfacts import Docker, OsFamily
from puppeter.persistence.gateway.fqdn import FqdnSetterGatewayImpl

from puppeter.domain.model.fqdn import FqdnConfiguration
from tests.domain.mock_facter import MockFacter
from puppeter import container


def test_fqdn_on_redhat():
    # given
    gateway = FqdnSetterGatewayImpl()
    config = FqdnConfiguration(fqdn='appserver.acme.internal')
    MockFacter.set_fact(Docker, Docker.NO)
    MockFacter.set_fact(OsFamily, OsFamily.RedHat)
    container.initialize()

    # when
    configurers = gateway.process_fully_qualified_domain_name(config)

    # then
    assert len(configurers) == 1

    # when
    configurer = configurers[0]
    commands = configurer.produce_commands()

    # then
    assert u"    puppet resource host 'appserver.acme.internal' " \
        "ensure=present host_aliases='appserver' ip=127.0.0.1 " \
        "comment='FQDN'" in commands
    assert "    hostname 'appserver'" in commands
    assert "  changes => 'set HOSTNAME appserver'" in commands


def test_fqdn_on_debian():
    # given
    gateway = FqdnSetterGatewayImpl()
    config = FqdnConfiguration(fqdn='appserver.acme.internal')
    MockFacter.set_fact(Docker, Docker.NO)
    MockFacter.set_fact(OsFamily, OsFamily.Debian)
    container.initialize()

    # when
    configurers = gateway.process_fully_qualified_domain_name(config)

    # then
    assert len(configurers) == 1

    # when
    configurer = configurers[0]
    commands = configurer.produce_commands()

    # then
    assert u"    puppet resource host 'appserver.acme.internal' " \
           "ensure=present host_aliases='appserver' ip=127.0.0.1 " \
           "comment='FQDN'" in commands
    assert "    hostname 'appserver'" in commands
    assert u"  content => 'appserver'" in commands


def test_fqdn_on_docker():
    # given
    gateway = FqdnSetterGatewayImpl()
    config = FqdnConfiguration(fqdn='appserver.acme.internal')
    MockFacter.set_fact(Docker, Docker.YES)
    container.initialize()

    # when
    with pytest.raises(NotImplementedError) as excinfo:
        gateway.process_fully_qualified_domain_name(config)

    # then
    assert "Can't set FQDN when running inside Docker!" in str(excinfo.value)

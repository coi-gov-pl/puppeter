from puppeter.domain.model.csr import CsrAttributesConfiguration
from puppeter.domain.model.installer import Mode
from puppeter.persistence.gateway.csr import CsrAttributesConfigurer, CsrAttributesSetterGatewayImpl
from puppeter import container


def test_csr_on_server():
    # given
    config = CsrAttributesConfiguration()
    config.read_raw_options(dict(
        pp_role='appserver'
    ))
    configurer = CsrAttributesConfigurer(config, Mode.Server)
    container.initialize()
    # when
    commands = configurer.produce_commands()

    # then
    assert '  pp_role: appserver' in commands
    assert '  group   => \'puppet\',' in commands


def test_csr_on_agent():
    # given
    config = CsrAttributesConfiguration()
    config.read_raw_options(dict(
        pp_role='agent'
    ))
    configurer = CsrAttributesConfigurer(config, Mode.Agent)
    container.initialize()

    # when
    commands = configurer.produce_commands()

    # then
    assert '  pp_role: agent' in commands


def test_csr_gateway():
    # given
    gateway = CsrAttributesSetterGatewayImpl()
    config = CsrAttributesConfiguration()
    config.read_raw_options(dict(
        pp_datacenter='dc1'
    ))
    mode = Mode.Server

    # when
    configurers = gateway.save_csr_attributes(config, mode)

    # then
    assert len(configurers) == 1
    op = getattr(configurers[0], "produce_commands", None)
    assert op is not None
    assert callable(op)

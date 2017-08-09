from puppeter.domain.model.fqdn import FqdnConfiguration


def test_fqdn_read():
    # given
    fqdn = FqdnConfiguration()

    # when
    fqdn.read_raw_options(options='app01.acme.internal')

    # then
    assert fqdn.fqdn() == 'app01.acme.internal'
    assert fqdn.hostname() == 'app01'
    assert fqdn.has_domain()
    assert fqdn.domain() == 'acme.internal'


def test_fqdn_simple():
    # given
    fqdn = FqdnConfiguration('simple')

    # then
    assert fqdn.fqdn() == 'simple'
    assert fqdn.hostname() == 'simple'
    assert fqdn.domain() is None
    assert fqdn.has_domain() is False

from puppeter.domain.facter import Facter

TEST_KEY = 'some-key'


def test_facter_get_unknown():
    value = Facter.get(TEST_KEY)

    assert value is None


def test_invalid_resolver():
    try:
        before_count = len(Facter._Facter__resolvers)
        Facter.set(TEST_KEY, lambda: None)
        value = Facter.get(TEST_KEY)

        assert value is None
        assert len(Facter._Facter__resolvers) == before_count + 1
    finally:
        Facter._Facter__resolvers.pop(TEST_KEY)
        assert len(Facter._Facter__resolvers) == before_count

from puppeter.domain.facter import Facter

TEST_KEY = 'some-key'


def test_facter_get_unknown():
    value = Facter.get(TEST_KEY)

    assert value is None


def test_invalid_resolver():
    # noinspection PyUnresolvedReferences,PyProtectedMember
    resolvers = Facter._Facter__resolvers
    before_count = len(resolvers)
    try:
        Facter.set(TEST_KEY, lambda: None)
        value = Facter.get(TEST_KEY)

        assert value is None
        assert len(resolvers) == before_count + 1
    finally:
        resolvers.pop(TEST_KEY)
        assert len(resolvers) == before_count

from puppeter.domain.facter import Facter


class MockFacter(Facter):
    @staticmethod
    def reset_fact(enumvar):
        MockFacter._facts.pop(enumvar, None)

    @staticmethod
    def reset_facts():
        MockFacter._facts.clear()

    @staticmethod
    def set_fact(enumvar, value):
        MockFacter._facts[enumvar] = value

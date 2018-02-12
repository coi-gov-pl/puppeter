import pytest

from integration_tests.phial import Phial, \
    ssh_service, \
    docker_ip, \
    docker_services, \
    docker_compose_file, \
    docker_compose_project_name, \
    docker_allow_fallback

__fixtures = [
    ssh_service,
    docker_ip,
    docker_services,
    docker_compose_file,
    docker_compose_project_name,
    docker_allow_fallback
]


@pytest.fixture
def phial(ssh_service):
    return Phial(ssh_service)


@pytest.fixture
def regex():
    return Regex()


class Regex:
    def __init__(self):
        import re
        self.re = re.compile('^$')

    def pattern(self, re):
        # type: (str) -> Regex
        self.re = re
        return self

    def matches(self, text, strip=True):
        __tracebackhide__ = True
        if strip:
            testable = text.strip()
        else:
            testable = text
        if self.re.match(testable) is None:
            pytest.fail("regex of '{regex}' do not match given text {text}"
                        .format(text=repr(testable), regex=self.re.pattern))

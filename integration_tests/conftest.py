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

from __future__ import print_function

import abc

import attr
import re
import subprocess
import time
import timeit
import logging
import paramiko
import pytest
import os
import select
import colorama
import sys

import six
from paramiko import SFTPClient, SSHClient, Channel
from paramiko.common import o777
from typing import Sequence
from six import StringIO

logger = logging.getLogger()


class DirSFTPClient(paramiko.SFTPClient):
    def put_dir(self, source, target, exclude=('.git', '.tox')):
        ''' Uploads the contents of the source directory to the target path. The
            target directory needs to exists. All subdirectories in source are
            created under target.
        '''
        self.mkdir(target, ignore_existing=True)
        for item in os.listdir(source):
            itemfull = os.path.join(source, item)
            if os.path.isfile(itemfull):
                self.put(itemfull, '%s/%s' % (target, item))
            else:
                if item in exclude:
                    continue
                self.mkdir('%s/%s' % (target, item), ignore_existing=True)
                self.put_dir(itemfull, '%s/%s' % (target, item))

    def mkdir(self, path, mode=o777, ignore_existing=False):
        ''' Augments mkdir by adding an option to not fail if the folder exists  '''
        try:
            super(DirSFTPClient, self).mkdir(path, mode)
        except IOError:
            if ignore_existing:
                pass
            else:
                raise


class Phial:
    def __init__(self, ssh_service):
        self.__ssh = ssh_service  # type: SSHClient

    def scp(self, localpath, remotepath):
        if os.path.isfile(localpath):
            logger.info('Coping local file: %s to remote location: %s', localpath, remotepath)
            sftp = self.__ssh.open_sftp()  # type: SFTPClient
            sftp.put(localpath, remotepath)
            sftp.close()
        if os.path.isdir(localpath):
            logger.info('Uploading local directory: %s to remote location: %s', localpath, remotepath)
            self.__put_dir(localpath, remotepath)

    def exec(self, command, capture=False):
        # type: (str, bool) -> (int, str, str)
        logger.info("Executing command: %s", command)
        channel = self.__ssh.get_transport().open_session()  # type: Channel
        channel.get_pty()
        if capture:
            handler = Phial.CaptureOutputHandler()
        else:
            print("\n")
            handler = Phial.PrintOutputHandler()
        reader = self.OutputReader(channel, handler)
        channel.exec_command(command)
        while True:
            if channel.exit_status_ready():
                reader.read_all()
                break
            rl, wl, xl = select.select([channel], [], [], 0.0)
            if len(rl) > 0:
                reader.read_chunk()
        if capture:
            return channel.exit_status, handler.collected_output(), handler.collected_error_output()
        else:
            return channel.exit_status, '', ''

    def __put_dir(self, source, target):
        transport = self.__ssh.get_transport()
        with DirSFTPClient.from_transport(transport) as sftp:
            sftp.put_dir(source, target)
            sftp.close()

    @six.add_metaclass(abc.ABCMeta)
    class OutputHandler:
        @abc.abstractmethod
        def out(self, data):
            # type: (str) -> None
            pass

        @abc.abstractmethod
        def err(self, data):
            # type: (str) -> None
            pass

    class CaptureOutputHandler(OutputHandler):
        def __init__(self):
            self.outbuf = ''
            self.errbuf = ''

        def out(self, data):
            self.outbuf += data

        def err(self, data):
            self.errbuf += data

        def collected_output(self):
            return self.outbuf

        def collected_error_output(self):
            return self.errbuf

    class PrintOutputHandler(OutputHandler):
        PHIAL_WRAP = colorama.Fore.WHITE + colorama.Style.DIM +\
                     "phial >>> " + colorama.Style.RESET_ALL

        def __init__(self):
            colorama.init(strip=False)
            self.outbuf = Phial.OutputBuffer()  # type: Phial.OutputBuffer
            self.errbuf = Phial.OutputBuffer()  # type: Phial.OutputBuffer

        def out(self, data):
            self.outbuf.recv(data)
            lines = self.outbuf.lines_collected()
            for line in lines:
                self.print_out(line)

        def err(self, data):
            self.errbuf.recv(data)
            lines = self.errbuf.lines_collected()
            for line in lines:
                self.print_err(line)

        def print_out(self, line):
            print("{phial}{color}{line}{rs}".format(
                phial=self.PHIAL_WRAP,
                color=colorama.Fore.BLUE + colorama.Style.DIM,
                line=line,
                rs=colorama.Style.RESET_ALL
            ))

        def print_err(self, line):
            print("{phial}{color}{line}{rs}".format(
                phial=self.PHIAL_WRAP,
                color=colorama.Fore.RED,
                line=line,
                rs=colorama.Style.RESET_ALL
            ), file=sys.stderr)

    class OutputReader:
        def __init__(self, channel, handler):
            self.__channel = channel  # type: Channel
            self.__handler = handler  # type: Phial.OutputHandler

        def read_all(self):
            while self.__channel.recv_stderr_ready() or self.__channel.recv_ready():
                self.read_chunk(1024)

        def read_chunk(self, size=32):
            if self.__channel.recv_stderr_ready():
                data = self.__channel.recv_stderr(size).decode()
                self.__handler.err(data)
            if self.__channel.recv_ready():
                data = self.__channel.recv(size).decode()
                self.__handler.out(data)

    class OutputBuffer:
        def __init__(self):
            self.buf = ''

        def recv(self, data):
            self.buf += data

        def lines_collected(self):
            # type: () -> Sequence[str]
            splited = self.buf.splitlines(keepends=True)
            collected = []
            newbuf = ''
            for line in splited:
                if line.endswith(('\n', '\r\n')):
                    collected.append(line.rstrip())
                else:
                    newbuf += line
            self.buf = newbuf
            return collected


@pytest.fixture
def docker_compose_file(pytestconfig, sut):
    return os.path.join(
        str(pytestconfig.rootdir),
        'integration_tests', 'system-under-tests', sut,
        'docker-compose.yml'
    )


@pytest.fixture
def ssh_service(docker_ip, docker_services):
    """Ensure that "SSH service" is up and responsive."""
    ssh = paramiko.SSHClient()
    port = docker_services.port_for('sut', 22)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=docker_ip,
        username='root',
        password='phial',
        port=port
    )
    return ssh


def execute(command, success_codes=(0,)):
    """Run a shell command."""
    try:
        output = subprocess.check_output(
            command, stderr=subprocess.STDOUT, shell=True,
        )
        status = 0
    except subprocess.CalledProcessError as error:
        output = error.output or b''
        status = error.returncode
        command = error.cmd
    output = output.decode('utf-8')
    if status not in success_codes:
        raise Exception(
            'Command %r returned %d: """%s""".' % (command, status, output)
        )
    return output


@pytest.fixture(scope='session')
def docker_ip():
    """Determine IP address for TCP connections to Docker containers."""

    # When talking to the Docker daemon via a UNIX socket, route all TCP
    # traffic to docker containers via the TCP loopback interface.
    docker_host = os.environ.get('DOCKER_HOST', '').strip()
    if not docker_host:
        return '127.0.0.1'

    match = re.match('^tcp://(.+?):\d+$', docker_host)
    if not match:
        raise ValueError(
            'Invalid value for DOCKER_HOST: "%s".' % (docker_host,)
        )
    return match.group(1)


@attr.s(frozen=True)
class Services(object):
    """."""

    _docker_compose = attr.ib()
    _docker_allow_fallback = attr.ib(default=False)

    _services = attr.ib(init=False, default=attr.Factory(dict))

    def port_for(self, service, port):
        """Get the effective bind port for a service."""

        # Return the container port if we run in no Docker mode.
        if self._docker_allow_fallback:
            return port

        # Lookup in the cache.
        cache = self._services.get(service, {}).get(port, None)
        if cache is not None:
            return cache

        output = self._docker_compose.execute(
            'port %s %d' % (service, port,)
        )
        endpoint = output.strip()
        if not endpoint:
            raise ValueError(
                'Could not detect port for "%s:%d".' % (service, port)
            )

        # Usually, the IP address here is 0.0.0.0, so we don't use it.
        match = int(endpoint.split(':', 1)[1])

        # Store it in cache in case we request it multiple times.
        self._services.setdefault(service, {})[port] = match

        return match

    def wait_until_responsive(self, check, timeout, pause,
                              clock=timeit.default_timer):
        """Wait until a service is responsive."""

        ref = clock()
        now = ref
        while (now - ref) < timeout:
            if check():
                return
            time.sleep(pause)
            now = clock()

        raise Exception(
            'Timeout reached while waiting on service!'
        )


def str_to_list(arg):
    if isinstance(arg, (list, tuple)):
        return arg
    return [arg]


@attr.s(frozen=True)
class DockerComposeExecutor(object):
    _compose_files = attr.ib(convert=str_to_list)
    _compose_project_name = attr.ib()

    def execute(self, subcommand):
        command = "docker-compose"
        for compose_file in self._compose_files:
            command += ' -f "{}"'.format(compose_file)
        command += ' -p "{}" {}'.format(self._compose_project_name, subcommand)
        return execute(command)


@pytest.fixture
def docker_compose_project_name():
    """ Generate a project name using the current process' PID.

    Override this fixture in your tests if you need a particular project name.
    """
    return "pytest{}".format(os.getpid())


@pytest.fixture
def docker_allow_fallback():
    """Return if want to run against localhost when docker is not available.

    Override this fixture to return `True` if you want the ability to
    run without docker.

    """
    return False


@pytest.fixture
def docker_services(
    docker_compose_file, docker_allow_fallback, docker_compose_project_name
):
    """Ensure all Docker-based services are up and running."""

    docker_compose = DockerComposeExecutor(
        docker_compose_file, docker_compose_project_name
    )

    # If we allowed to run without Docker, check it's presence
    if docker_allow_fallback is True:
        try:
            execute('docker ps')
        except Exception:
            # Run against localhost
            yield Services(docker_compose, docker_allow_fallback=True)
            return

    # Spawn containers.
    docker_compose.execute('up --build -d')

    # Let test(s) run.
    yield Services(docker_compose)

    # Clean up.
    docker_compose.execute('down -v')
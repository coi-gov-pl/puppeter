from __future__ import print_function

import logging
import paramiko
import pytest
import os
import select
from paramiko import SFTPClient, SSHClient, Channel
from paramiko.common import o777

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

    def __put_dir(self, source, target):
        transport = self.__ssh.get_transport()
        with DirSFTPClient.from_transport(transport) as sftp:
            sftp.put_dir(source, target)
            sftp.close()

    def exec(self, command):
        logger.info("Executing command: %s", command)
        channel = self.__ssh.get_transport().open_session()  # type: Channel
        channel.get_pty()
        channel.exec_command(command)
        print("\n")
        while True:
            if channel.exit_status_ready():
                print(channel.recv(16*4096).decode(), end='')
                break
            rl, wl, xl = select.select([channel], [], [], 0.0)
            if len(rl) > 0:
                print(channel.recv(16).decode(), end='')
        return channel.exit_status


@pytest.fixture(scope='session')
def phial(ssh_service):
    return Phial(ssh_service)


@pytest.fixture(scope='session')
def docker_compose_file(pytestconfig, sut):
    return os.path.join(
        str(pytestconfig.rootdir),
        'integration_tests', 'system-under-tests', sut,
        'docker-compose.yml'
    )


@pytest.fixture(scope='session')
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

from __future__ import absolute_import
import re
import subprocess

from os import path, environ, access, X_OK

from puppeter.domain.facter import Facter
from puppeter.domain.model.javafacts import JavaVersion
from puppeter.domain.model.osfacts import OsFamily


def calculate_java_version():
    # type: () -> JavaVersion
    osfamily = Facter.get(OsFamily)
    java_prog_name = 'java.exe' if osfamily is OsFamily.Windows else 'java'
    search_paths = environ['PATH'].split(path.pathsep)
    java_prog = None
    for search_path in search_paths:
        java_prog_candidate = path.join(search_path, java_prog_name)
        if __is_executable(java_prog_candidate):
            java_prog = java_prog_candidate
            break
    if java_prog is None:
        return JavaVersion.NOT_INSTALLED
    return __get_java_version(java_prog)


def __is_executable(candidate):
    return path.exists(candidate) and access(candidate, X_OK)


def __get_java_version(java_prog):
    sp = subprocess.Popen([java_prog, '-version'],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          universal_newlines=True)
    (x, stderr) = sp.communicate()
    retcode = sp.wait()
    if retcode != 0:
        return JavaVersion.NOT_INSTALLED
    pattern = re.compile('(?:jdk|jre|java) version "([0-9]+)\.([0-9]+)\.([0-9]+)[_-]([0-9a-z_-]+)"')
    for line in stderr.splitlines():
        match = pattern.match(line)
        if match is not None:
            ver = match.group(2)
            return {
                '6': JavaVersion.JRE6,
                '7': JavaVersion.JRE7,
                '8': JavaVersion.JRE8,
                '9': JavaVersion.JRE9
            }[ver]
    return JavaVersion.NOT_INSTALLED

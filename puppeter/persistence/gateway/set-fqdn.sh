#!/usr/bin/env bash
hostname '@{hostname}'
puppet resource host '@{fqdn}' ensure=present host_aliases='@{hostname}' ip=127.0.0.1 comment='FQDN'
su - $(whoami)
set -ex

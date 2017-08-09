#!/usr/bin/env bash
puppet resource host '@{fqdn}' ensure=present host_aliases='@{hostname}' ip=127.0.0.1 comment='FQDN'
hostname '@{hostname}'
reload_shell

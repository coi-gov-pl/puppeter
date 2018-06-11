#!/usr/bin/env bash

set -e

# https://regex101.com/r/Uvm9bs/2
RHEL_SED_VERSION_PARSE='s/^[^0-9]+([0-9]+\.[0-9]+).*$/\1/'
COLOR_NC='\e[0m' # No Color
COLOR_LIGHT_BLUE='\e[1;34m'
COLOR_LIGHT_RED='\e[1;31m'
RUN=${RUN:-1}
DEBUG=${DEBUG:-0}
SUDO=${SUDO:-1}
APT_UPDATE_INTERVAL=${APT_UPDATE_INTERVAL:-7200}
MODE=${MODE:-puppeter}

if [ $DEBUG == 1 ]; then
  set -x
fi

if [ -f /etc/redhat-release ]; then
  if [ -f /etc/oracle-release ]; then
    os=oraclelinux
    version=$(cat /etc/oracle-release | sed -E $RHEL_SED_VERSION_PARSE)
  elif [ -f /etc/centos-release ]; then
    os=centos
    version=$(cat /etc/centos-release | sed -E $RHEL_SED_VERSION_PARSE)
  else
    os=rhel
    version=$(cat /etc/redhat-release | sed -E $RHEL_SED_VERSION_PARSE)
  fi
  osfamily=redhat
elif [ -f /etc/debian_version ]; then
  osfamily=debian
  if [ -f /etc/lsb-release ]; then
    source /etc/lsb-release
    os=$(echo $DISTRIB_ID | tr '[:upper:]' '[:lower:]')
    version=$DISTRIB_RELEASE
  else
    os=debian
    version=$(cat /etc/debian_version)
  fi
fi
majversion=$(echo $version | cut -d. -f1)

run() {
  command="$*"
  if [[ $EUID -ne 0 ]] && [ $SUDO == 1 ]; then
    command="sudo -i ${command}"
  fi
  echo -e "${COLOR_LIGHT_BLUE}Executing: ${command}${COLOR_NC}"
  if [ $RUN == 1 ]; then
    eval "$command"
  fi
}

unsupported() {
  echo -e "${COLOR_LIGHT_RED}Unsupported operating system: ${os} ${version}${COLOR_NC}" 1>&2
  exit 1
}

last_aptget_update() {
    local apt_date now_date
    apt_date="$(stat -c %Y '/var/cache/apt')"
    now_date="$(date +'%s')"

    echo $((now_date - apt_date))
}

if [ $osfamily == redhat ]; then
  if [ $majversion == 6 ]; then
    if [ $os == centos ]; then
      run yum install -y centos-release-scl
      run yum install -y python27-python-pip
    fi
    if [ $os == oraclelinux ]; then
      run yum install -y yum-utils
      run yum-config-manager --enable public_ol6_software_collections
      run yum install -y python27-python-pip
    fi
    echo 'source /opt/rh/python27/enable' >> /etc/profile.d/python27.sh
    run source /opt/rh/python27/enable
elif [ $majversion == 7 ]; then
    if [ $os == centos ]; then
      run yum install -y epel-release
      run yum install -y python-pip
    fi
    if [ $os == oraclelinux ]; then
      run yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
      run yum install -y python-pip
    fi
  else
    unsupported
  fi
elif [ $osfamily == debian ]; then
  flavor="$os-$majversion"
  if [[ "$(last_aptget_update)" -gt $APT_UPDATE_INTERVAL ]]; then
    run apt-get update -m
  fi
  if [ $flavor == ubuntu-14 ] || [ $flavor == debian-8 ]; then
    run apt-get install -y python-pip python-dev
  else
    run apt-get install -y python-pip
  fi
fi
if [ $MODE == puppeter ]; then
  run LC_ALL=C pip install puppeter
fi

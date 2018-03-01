Puppeter - an automatic puppet installer
========================================

**Work In Progress!**

.. image:: https://travis-ci.org/coi-gov-pl/puppeter.svg?branch=develop
    :target: https://travis-ci.org/coi-gov-pl/puppeter
.. image:: https://circleci.com/gh/coi-gov-pl/puppeter.svg?style=svg
    :target: https://circleci.com/gh/coi-gov-pl/puppeter
.. image:: https://coveralls.io/repos/github/coi-gov-pl/puppeter/badge.svg?branch=feature%2Finstall-puppet-agent
    :target: https://coveralls.io/github/coi-gov-pl/puppeter?branch=feature%2Finstall-puppet-agent
.. image:: https://img.shields.io/pypi/v/puppeter.svg
    :target: https://pypi.python.org/pypi/puppeter


A commandline tool to ease the installation of typical puppetserver - agent installation. It uses a interactive mode and batch mode as well. Batch mode utilizes a answer files for full automatic operation.

Installation
------------

To install Puppeter simple use PIP:

.. code-block:: bash

  pip install puppeter

If you like to install puppeter on clean operating system with automatic installer execute:

.. code-block:: bash

  curl https://raw.githubusercontent.com/coi-gov-pl/puppeter/master/setup.sh | bash

It will install PIP and compatibile Python (2.7+)

The installer script is supported for:

* Debian 8
* Debian 9
* Ubuntu 14.04
* Ubuntu 16.04
* CentOS 6
* CentOS 7
* OracleLinux 6
* OracleLinux 7

**TODO: Write more later**

========================================================
devpi-mirror-index-acl: limit who can add mirror indexes
========================================================

This plugin adds the ``--acl-mirror-index-create`` command line option to `devpi-server`_.
The option takes a list of user and group names which are allowed to create mirror indexes.

.. _devpi-server: http://pypi.python.org/pypi/devpi-server


Installation
============

``devpi-mirror-index-acl`` needs to be installed alongside ``devpi-server`` to enable the command line option.

You can install it with::

    pip install devpi-mirror-index-acl

There is no configuration needed as ``devpi-server`` will automatically discover the plugin through calling hooks using the setuptools entry points mechanism.


Motivation
==========

Mirror indexes can take up a lot of resources in both storage and CPU.
Especially mirroring PyPI and other indexes with a lot of packages and releases.
This package allows limiting who can add such mirrors to prevent accidental or malicious resource exhaustion.


Usage
=====

When using the ``--acl-mirror-index-create`` command line option, you provide a comma separated list of user or group names.

The same applies when using the ``DEVPISERVER_ACL_MIRROR_INDEX_CREATE`` environment variable.

When using a configuration yaml file you can use an explicit list::

    devpi-server:
      acl-mirror-index-create:
        - "root"

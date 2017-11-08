MicroCI
=======

Lightweight continuous integration.

Prerequisites
-------------

 * libgit2 ``==`` 0.25.1
 * docker ``>=`` 17.9.0

Installation
------------

.. code-block:: none

   python setup.py install

Usage
-----

MicroCI needs:

 * a database (see `PyDAL <https://github.com/web2py/pydal#which-databases-are-supported>`_ for a full list of supported databases)
 * a Redis for jobs scheduling

See ``docker-compose.yml`` for a simple example of MicroCI infrastructure.

.. csv-table:: Environment variables
   :header: "Variable", "Default", "Description"

   DEBUG, True, "DEBUG mode for Flask"
   DBURL, "sqlite://microci.db", "Database for jobs persistence"
   BROKER, "redis://localhost", "Broker for jobs scheduling"
   DOCKER_URL, "unix://var/run/docker.sock", "Docker URL for container's job creation"
   DOCKER_IMAGE, "debian:latest", "Docker image for job's container"
   SIGNATURE, "secret", "Token for webhooks"

Supported webhooks
------------------

 * Gogs

Coming soon:

 * Github
 * Gitlab
 * Bitbucket

License
-------

Released under the MIT license.
See ``LICENSE.txt`` for the complete license.

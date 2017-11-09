MicroCI
=======

Lightweight self-hosted continuous integration.

Prerequisites
-------------

 * libgit2 ``==`` 0.25.1
 * docker ``>=`` 17.9.0

Installation
------------

.. code-block:: none

   python setup.py install

Deployment
----------

MicroCI needs:

 * a database (see `PyDAL <https://github.com/web2py/pydal#which-databases-are-supported>`_ for a full list of supported databases)
 * a Redis for jobs scheduling

See ``docker-compose.yml`` for a simple example of MicroCI infrastructure.

.. csv-table:: Environment variables
   :header: "Variable", "Default", "Description"

   DEBUG, True, "DEBUG mode for Flask"
   DBURL, "sqlite://microci.db", "Database for jobs persistence"
   BROKER, "redis://localhost", "Broker for jobs scheduling"
   DOCKER_URL, "unix://var/run/docker.sock", "Docker URL for job's container creation"
   DOCKER_IMAGE, "debian:latest", "Docker image for job's container if not specified"
   SIGNATURE, "secret", "Token for webhooks"

Supported webhooks
------------------

 * Gogs (endpoint: ``/hooks/gogs``)

Coming soon:

 * Github
 * Gitlab
 * Bitbucket

Usage
-----

Put a file named ``.microci.json`` at the root of your repository, and configure
the webhook for push events to the right endpoint.

If no file is present, the following configuration is assumed:

.. code-block:: javascript

   {
     "dockerimg": "debian:latest",
     "command": "/bin/sh microci.sh"
   }

License
-------

Released under the MIT license.
See ``LICENSE.txt`` for the complete license.

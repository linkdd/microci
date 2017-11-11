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
   SSH_USERNAME, "git", "SSH username when cloning repository"
   SSH_PUBKEY, "$HOME/.ssh/id_rsa.pub", "Path to SSH public key"
   SSH_PRIVKEY, "$HOME/.ssh/id_rsa", "Path to SSH private key"
   SSH_PASSPHRASE, "''", "Passphrase for SSH private key (empty if none)"
   REPO_HOST_PATH, "''", "Path to the folder containing the repositories"

If the worker is running in a container, bind a folder from the host to ``/microci/repos``.
This is were the git repositories are cloned.

Then set the environment variable ``REPO_HOST_PATH`` to that folder. The worker will
use it to bind the repository in the job's container.

Supported webhooks
------------------

 * Gogs (endpoint: ``/hooks/gogs/``)

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

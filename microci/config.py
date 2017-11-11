# -*- coding: utf-8 -*-

from decouple import config
import os


DEBUG = config('DEBUG', default=True, cast=bool)
DBURL = config('DBURL', default='sqlite://microci.db')
BROKER = config('BROKER', default='redis://localhost')
DOCKER_URL = config('DOCKER_URL', default='unix://var/run/docker.sock')
DOCKER_IMAGE = config('DOCKER_IMAGE', default='debian:latest')
SIGNATURE = config('SIGNATURE', default='secret')

REPO_HOST_PATH = config('REPO_HOST_PATH', default='')

SSH_USERNAME = config('SSH_USERNAME', default='git')
SSH_PUBKEY = config('SSH_PUBKEY', default=os.path.join(
    os.path.expanduser('~'), '.ssh', 'id_rsa.pub'
))
SSH_PRIVKEY = config('SSH_PRIVKEY', default=os.path.join(
    os.path.expanduser('~'), '.ssh', 'id_rsa'
))
SSH_PASSPHRASE = config('SSH_PASSPHRASE', default='')

# -*- coding: utf-8 -*-

from decouple import config


DEBUG = config('DEBUG', default=True, cast=bool)
DBURL = config('DBURL', default='sqlite://microci.db')
BROKER = config('BROKER', default='redis://localhost')
DOCKER_URL = config('DOCKER_URL', default='unix://var/run/docker.sock')
DOCKER_IMAGE = config('DOCKER_IMAGE', default='debian:latest')
SIGNATURE = config('SIGNATURE', default='secret')

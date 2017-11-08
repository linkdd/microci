# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
import re


NAME = 'microci'
KEYWORDS = 'microci self hosted continuous integration'
DESC = 'MicroCI for lightweight self hosted continuous integration'
URL = 'https://github.com/linkdd/microci'
AUTHOR = 'David Delassus'
AUTHOR_EMAIL = 'david.jose.delassus@gmail.com'
LICENSE = 'MIT'
REQUIREMENTS = [
    'six>=1.10.0',
    'python-decouple>=3.1',
    'Flask>=0.12.2',
    'gunicorn>=17.9.1',
    'pyDAL>=17.8',
    'celery[redis]>=4.1.0',
    'docker>=2.5.1',
    'maya>=0.3.3',
    'pygit2==0.25.1',
    'attrs>=15.2.0'
]

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation :: CPython'
]


def get_cwd():
    return os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))


def get_version(default='0.1'):
    _name = NAME.replace('.', os.sep)
    path = os.path.join(get_cwd(), _name, '__init__.py')

    with open(path) as f:
        stream = f.read()
        regex = re.compile(r'.*__version__ = \'(.*?)\'', re.S)
        version = regex.match(stream)

        if version is None:
            version = default

        else:
            version = version.group(1)

    return version


def get_long_description():
    path = os.path.join(get_cwd(), 'README.rst')
    desc = None

    if os.path.exists(path):
        with open(path) as f:
            desc = f.read()

    return desc


def get_test_suite():
    return 'tests'


setup(
    name=NAME,
    keywords=KEYWORDS,
    version=get_version(),
    url=URL,
    description=DESC,
    long_description=get_long_description(),
    license=LICENSE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(),
    test_suite=get_test_suite(),
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
)

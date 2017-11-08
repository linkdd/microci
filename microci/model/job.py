# -*- coding: utf-8 -*-

from enum import IntEnum, auto
from pydal import Field


class JobStatus(IntEnum):
    PENDING = auto()
    STARTED = auto()
    ERRORED = auto()
    FAILED = auto()
    SUCCEED = auto()


def make_job(db):
    db.define_table(
        'jobs',
        Field('ssh_url', type='string', length=512),
        Field('clone_url', type='string', length=512),
        Field('commit_id', type='string', length=255),
        Field('commit_msg', type='text'),
        Field('commit_url', type='string', length=512),
        Field('author', type='string', length=255),
        Field('committer', type='string', length=255),
        Field('datetime', type='datetime'),
        Field('logs', type='text'),
        Field('status', type='integer', default=JobStatus.PENDING)
    )

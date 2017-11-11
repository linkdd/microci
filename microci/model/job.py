# -*- coding: utf-8 -*-

from enum import IntEnum
from pydal import Field


class JobStatus(IntEnum):
    PENDING = 0
    STARTED = 1
    ERRORED = 2
    FAILED = 3
    SUCCEED = 4


def make_job(db):
    db.define_table(
        'jobs',
        Field('repository', type='string', length=255),
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

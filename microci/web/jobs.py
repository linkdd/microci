# -*- coding: utf-8 -*-

from flask import Blueprint, make_response, jsonify

from microci.model.job import JobStatus
from microci.web import db


blueprint = Blueprint('jobs', __name__)


def fetch(db, filter):
    for job in db(filter).select():
        yield {
            'id': job.id,
            'repository': {
                'ssh': job.ssh_url,
                'clone': job.clone_url
            },
            'commit': {
                'id': job.commit_id,
                'message': job.commit_msg,
                'url': job.commit_url
            },
            'author': job.author,
            'committer': job.committer,
            'timestamp': job.datetime,
            'logs': job.logs,
            'status': JobStatus(job.status).name
        }


def fetch_status(db, status):
    return make_response(
        jsonify({'jobs': list(fetch(db, db.jobs.status == status))})
    )


@blueprint.route('/')
def index():
    database = db.get()
    return make_response(
        jsonify({'jobs': list(fetch(database, database.jobs))})
    )


@blueprint.route('/pending')
def pending():
    return fetch_status(db.get(), JobStatus.PENDING)


@blueprint.route('/started')
def started():
    return fetch_status(db.get(), JobStatus.STARTED)


@blueprint.route('/errored')
def errored():
    return fetch_status(db.get(), JobStatus.ERRORED)


@blueprint.route('/failed')
def failed():
    return fetch_status(db.get(), JobStatus.FAILED)


@blueprint.route('/succeed')
def succeed():
    return fetch_status(db.get(), JobStatus.SUCCEED)


@blueprint.route('/<int:jid>')
def detail(jid):
    database = db.get()
    return make_response(
        jsonify({'jobs': list(fetch(database, database.jobs.id == jid))})
    )

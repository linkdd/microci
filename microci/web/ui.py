# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, abort

from microci.web.jobs import fetch as fetch_jobs
from microci.model.job import JobStatus
from microci.web import db


blueprint = Blueprint('ui', __name__)


@blueprint.route('/', defaults={'status': 'all'})
@blueprint.route('/<status>')
def index(status):
    database = db.get()

    if status == 'all':
        filter = database.jobs

    else:
        filter = database.jobs.status == getattr(JobStatus, status.upper())

    return render_template(
        'index.html',
        jobs=fetch_jobs(database, filter),
        active=status
    )


@blueprint.route('/job/<int:jid>')
def detail(jid):
    database = db.get()
    job = database.jobs(jid)

    if job is None:
        abort(404)

    else:
        return render_template('detail.html', job=job)

# -*- coding: utf-8 -*-

from flask import Blueprint, request, make_response, jsonify
from maya import MayaDT

from microci.worker import Job
from microci.web import db
from microci import config


blueprint = Blueprint('gogs-hooks', __name__)


def to_maya(commit):
    return MayaDT.from_rfc3339(commit['timestamp'])


@blueprint.route('', methods=['POST'])
@blueprint.route('/', methods=['POST'])
def hook():
    if request.headers.get('X-Gogs-Signature') != config.SIGNATURE:
        return {'error': 'invalid signature'}, 400

    try:
        event = request.get_json()

    except Exception as err:
        return {'error': str(err)}, 400

    commits = sorted(
        event['commits'],
        key=to_maya,
        reverse=True
    )
    commit = commits[0]

    job = Job(
        repository=event['repository']['full_name'],
        ssh_url=event['repository']['ssh_url'],
        clone_url=event['repository']['clone_url'],
        commit_id=commit['id'],
        commit_msg=commit['message'],
        commit_url=commit['url'],
        author='{name} <{email}>'.format(**commit['author']),
        committer='{name} <{email}>'.format(**commit['committer']),
        datetime=to_maya(commit).datetime()
    )
    job.run(db.get())

    return make_response(jsonify({'id': job.id}), 201)

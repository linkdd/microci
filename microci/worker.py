# -*- coding: utf-8 -*-

from microci.model.job import JobStatus
from microci.model import make_db
from microci import config

from pygit2 import clone_repository
from docker import DockerClient
from celery import Celery
from shutil import rmtree
from uuid import uuid4

import traceback
import attr
import os


app = Celery('jobs', broker=config.BROKER)


@app.task
def job_runner(job):
    db = make_db()

    def log(line):
        db(db.jobs.id == job.id).update(
            logs=db.jobs.logs + line
        )

    log('[JOB #{0}] Started'.format(job.id))

    db(db.jobs.id == job.id).update(status=JobStatus.STARTED)
    db.commit()

    container = None
    repo_path = None
    dockerimg = config.DOCKER_IMAGE

    try:
        repo_path = os.path.join(os.getcwd(), 'repos', str(uuid4()))
        os.makedirs(os.path.dirname(repo_path))

        repo_url = job.clone_url if job.ssh_url is None else job.ssh_url
        log('[JOB #{0}] git clone {1}'.format(job.id, repo_url))
        repo = clone_repository(repo_url, repo_path)

        log('[JOB #{0}] git checkout {1}'.format(job.id, job.commit_id))
        repo.checkout_tree(job.commit_id)

        log('[JOB #{0}] docker run {1}'.format(job.id, dockerimg))
        client = DockerClient(base_url=config.DOCKER_URL)
        container = client.containers.run(
            dockerimg,
            command='/bin/sh microci.sh',
            working_dir='/repo',
            volumes={
                repo_path: {
                    'bind': '/repo', 'mode': 'rw'
                }
            },
            detach=True
        )

        for line in container.logs(stdout=True, stderr=True, stream=True):
            log(line)

        retcode = container.wait()
        success = retcode == 0

        log('[JOB #{0}] Returned {1}'.format(job.id, retcode))

        status = JobStatus.SUCCEED if success else JobStatus.FAILED
        db(db.jobs.id == job.id).update(status=status)

    except Exception:
        log('[JOB #{0}] {1}'.format(job.id, traceback.format_exc()))
        db(db.jobs.id == job.id).update(status=JobStatus.ERRORED)

    finally:
        db.commit()

        if container is not None:
            container.remove()

        if repo_path is not None:
            rmtree(repo_path)


@attr.s(slots=True)
class Job(object):
    id = attr.ib()
    ssh_url = attr.ib()
    clone_url = attr.ib()
    commit_id = attr.ib()
    commit_msg = attr.ib()
    commit_url = attr.ib()
    author = attr.ib()
    committer = attr.ib()
    datetime = attr.ib()

    def run(self, db):
        self.id = db.jobs.insert(
            ssh_url=self.ssh_url,
            clone_url=self.clone_url,
            commit_id=self.commit_id,
            commit_msg=self.commit_msg,
            commit_url=self.commit_url,
            author=self.author,
            committer=self.comitter,
            datetime=self.datetime
        )
        db.commit()

        job_runner.delay(self)

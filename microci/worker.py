# -*- coding: utf-8 -*-

from microci.model.job import JobStatus
from microci.model import make_db
from microci import config

from pygit2 import clone_repository, RemoteCallbacks, Keypair
from docker import DockerClient
from celery import Celery
from shutil import rmtree
from uuid import uuid4

import traceback
import json
import attr
import os


app = Celery('jobs', broker=config.BROKER)


@app.task
def job_runner(job):
    job = Job.loads(job)
    db = make_db()

    def log(line):
        db(db.jobs.id == job.id).update(
            logs=db.jobs.logs.coalesce('') + '{0}\n'.format(line)
        )

    log('[JOB #{0}] Started'.format(job.id))

    db(db.jobs.id == job.id).update(status=JobStatus.STARTED)
    db.commit()

    container = None
    repo_path = None

    try:
        repo_name = str(uuid4())
        repo_path = os.path.join(os.getcwd(), 'repos', repo_name)
        repos_path = os.path.dirname(repo_path)

        if config.REPO_HOST_PATH:
            repo_host_path = os.path.join(config.REPO_HOST_PATH, repo_name)

        else:
            repo_host_path = repo_path


        if not os.path.exists(repos_path):
            os.makedirs(repos_path)

        log('[JOB #{0}] git clone {1}'.format(job.id, job.ssh_url))
        repo = clone_repository(
            job.ssh_url,
            repo_path,
            callbacks=RemoteCallbacks(
                credentials=Keypair(
                    config.SSH_USERNAME,
                    config.SSH_PUBKEY,
                    config.SSH_PRIVKEY,
                    config.SSH_PASSPHRASE
                ),
                certificate=lambda *_: True
            )
        )

        log('[JOB #{0}] git checkout {1}'.format(job.id, job.commit_id))
        commit = repo.get(job.commit_id)
        repo.checkout_tree(commit.tree)

        cfg_path = os.path.join(repo_path, '.microci.json')
        cfg = {
            'dockerimg': config.DOCKER_IMAGE,
            'command': '/bin/sh microci.sh'
        }

        if os.path.exists(cfg_path):
            log('[JOB #{0}] Load .microci.json'.format(job.id))
            try:
                with open(cfg_path) as f:
                    cfg.update(json.load(f))

            except Exception:
                log('[JOB #{0}] {1}'.format(job.id, traceback.format_exc()))

        log('[JOB #{0}] docker run {1}'.format(job.id, cfg['dockerimg']))
        client = DockerClient(base_url=config.DOCKER_URL)
        container = client.containers.run(
            cfg['dockerimg'],
            command=cfg['command'],
            working_dir='/repo',
            volumes=[
                '{0}:/repo:rw'.format(repo_host_path)
            ],
            detach=True
        )

        for line in container.logs(stdout=True, stderr=True, stream=True):
            log(line.decode().rstrip('\n'))

        retcode = container.wait()
        success = retcode == 0

        log('[JOB #{0}] Returned {1}'.format(job.id, retcode))

        status = JobStatus.SUCCEED if success else JobStatus.FAILED
        db(db.jobs.id == job.id).update(status=status)

    except Exception:
        log('[JOB #{0}] {1}'.format(job.id, traceback.format_exc()))
        db(db.jobs.id == job.id).update(status=JobStatus.ERRORED)

    db.commit()

    if container is not None:
        log('[JOB #{0}] Remove container'.format(job.id))
        container.remove()

    if repo_path is not None and os.path.exists(repo_path):
        log('[JOB #{0}] Remove repository'.format(job.id))
        rmtree(repo_path)

    db.close()


@attr.s(slots=True)
class Job(object):
    id = attr.ib(init=False)
    repository = attr.ib()
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
            repository=self.repository,
            ssh_url=self.ssh_url,
            clone_url=self.clone_url,
            commit_id=self.commit_id,
            commit_msg=self.commit_msg,
            commit_url=self.commit_url,
            author=self.author,
            committer=self.committer,
            datetime=self.datetime
        )
        db.commit()

        job_runner.delay(self.dumps())

    def dumps(self):
        return attr.asdict(self)

    @classmethod
    def loads(cls, raw):
        jid = raw.pop('id')
        job = Job(**raw)
        job.id = jid
        return job

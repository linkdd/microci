# -*- coding: utf-8 -*-

from microci.model.job import make_job
from microci import config
from pydal import DAL


def make_db():
    db = DAL(config.DBURL)
    make_job(db)
    return db

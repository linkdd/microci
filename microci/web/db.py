# -*- coding: utf-8 -*-

from microci.model import make_db
from flask import g


def get():
    try:
        db = g.db

    except AttributeError:
        db = make_db()
        g.db = db

    return db


def close(error):
    try:
        db = g.db

    except AttributeError:
        pass

    else:
        db.close()

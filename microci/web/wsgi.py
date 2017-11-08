# -*- coding: utf-8 -*-

from microci.web.urls import blueprints
from microci.web import db
from microci import config

from flask import Flask
import six


app = Flask(__name__)
app.config.from_object(config)
app.teardown_appcontext(db.close)

for prefix, blueprint in six.iteritems(blueprints):
    app.register_blueprint(blueprint, url_prefix=prefix)

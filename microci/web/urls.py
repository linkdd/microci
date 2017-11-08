# -*- coding: utf-8 -*-

from microci.web.hooks import gogs
from microci.web import jobs


blueprints = {
    '/jobs': jobs.blueprint,
    '/hooks/gogs': gogs.blueprint
}

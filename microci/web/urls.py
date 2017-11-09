# -*- coding: utf-8 -*-

from microci.web.hooks import gogs
from microci.web import jobs, ui


blueprints = {
    '/jobs': jobs.blueprint,
    '/hooks/gogs': gogs.blueprint,
    '/view': ui.blueprint
}

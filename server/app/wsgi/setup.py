
from ..hooks.beforeRequest import beforeRequest
from ..hooks.afterRequest import afterRequest
from ..hooks.errors import *

from .app import MyFlaskApp
lazy from ..views import blueprints

from flask import Flask


def setupApp(workerLogger, configManager, stopEvent):
    
    app = MyFlaskApp(workerLogger, configManager, stopEvent, import_name=__name__)

    
    for bp in blueprints:
        bp.registerForApp(app, app.routeManager)


    
    app.before_request(beforeRequest)
    app.after_request(afterRequest)

    setupErrorHandlers(app)
    
    return app
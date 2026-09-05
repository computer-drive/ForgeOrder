import datetime

from flask import Flask
from flask.json.provider import DefaultJSONProvider

from .hooks.beforeRequest import beforeRequest
from .hooks.afterRequest import afterRequest
from .hooks.errors import *
from app.routes.manager import RouteManager
lazy from app.processing.log.record import WorkerLogger

class JSONProvider(DefaultJSONProvider):
    ensure_ascii = False

    def default(self, obj): # type: ignore
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        else:
            return super().default(obj)
        
class MyFlaskApp(Flask):
    routeManager: 'RouteManager'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.routeManager = RouteManager()


        self.workerLogger : WorkerLogger | None  = None





def setupApp():
    app = MyFlaskApp(__name__)

    app.json_provider_class = JSONProvider
    app.json = JSONProvider(app)

    app.logger.disabled = True
    
    from app import blueprints
    for bp in blueprints:
        bp.registerForApp(app, app.routeManager)

    
    app.before_request(beforeRequest) # type: ignore

    app.after_request(afterRequest)

    setupErrorHandlers(app)
    
    return app
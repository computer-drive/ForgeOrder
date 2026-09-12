import datetime
from multiprocessing.synchronize import Event

from flask import Flask
from flask.json.provider import DefaultJSONProvider


from app.routes.manager import RouteManager
lazy from app.processing.log.record import WorkerLogger
lazy from ..config import ConfigManager

class JSONProvider(DefaultJSONProvider):
    ensure_ascii = False

    def default(self, obj): # type: ignore
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        else:
            return super().default(obj)
        
class MyFlaskApp(Flask):
    routeManager: 'RouteManager'

    def __init__(self, 
                  workerLogger : WorkerLogger,
                  configManager : ConfigManager,
                  stopEvent : Event,
                  *args, **kwargs,
                  ):
        super().__init__(*args, **kwargs)

        self.routeManager = RouteManager()

        self.workerLogger : WorkerLogger = workerLogger
        self.configManager: ConfigManager = configManager
        self.stopEvent = stopEvent

        self.json_provider_class = JSONProvider

        self.json = JSONProvider(self)

        self.logger.disabled = True


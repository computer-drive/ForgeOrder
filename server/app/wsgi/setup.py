
lazy from ..hooks.beforeRequest import beforeRequest
lazy from ..hooks.afterRequest import afterRequest
lazy from ..hooks.errors import setupErrorHandlers

lazy from .app import MyFlaskApp
lazy from ..views import blueprints


def setupApp(workerLogger, configManager, stopEvent):
    
    app = MyFlaskApp(workerLogger, configManager, stopEvent, import_name=__name__)

    
    for bp in blueprints:
        bp.registerForApp(app, app.routeManager)


    
    app.before_request(beforeRequest)
    app.after_request(afterRequest)

    setupErrorHandlers(app)
    
    return app
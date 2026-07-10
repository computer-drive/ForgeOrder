import json

from flask import current_app

from ..db.db import close_databases
from core.utils import make_response
import extensions

# @app.errorhandler(405)
def method_not_allowed(e):
        return make_response(
            1002,
            405,
        ), 405
    
# @app.errorhandler(404)
def not_found(e):
        return make_response(
            1003,
            404,
        ), 404

# @app.errorhandler(500)
def internal_server_error(e):
        return make_response(
            9001,
            500,
        ), 500
    
# @app.errorhandler(ArgumentException)
def argument_exception(e):
        return make_response(
            1001,
            e.args_,
        ), 400
    
# @app.teardown_appcontext
def teardown_appcontext(error):
        close_databases()
        if error is not None:
            logs = {
                    "error": {
                        "emsg": str(error),
                        "type": type(error).__name__,
                    },
                    "traceback": None
                    
                }
            if isinstance(error, Exception):
                logs["traceback"] = traceback.format_exception(type(error), error, error.__traceback__) # type: ignore

            extensions.logger.error(json.dumps(
                logs
            ), "FLASK_APP", "RequestError")

        return current_app

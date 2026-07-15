import json

from flask import current_app
from werkzeug.exceptions import UnsupportedMediaType

from ..db.db import close_databases
from core.utils import make_response
import extensions
import traceback
import sqlite3
from core.db.exceptions import ExecuteError

def unsupported_media_type(e: UnsupportedMediaType):
        return make_response(
            1001,
            e.description,
        ), 415

def method_not_allowed(e):
        return make_response(
            1002,
            405,
        ), 405
    

def not_found(e):
        return make_response(
            1003,
            404,
        ), 404


def internal_server_error(e):
        return make_response(
            9001,
            500,
        ), 500
    

def argument_exception(e):
        return make_response(
            1001,
            e.args_,
        ), 400
    
def handle_execute_error(e: ExecuteError):
    extensions.logger.error(
        {"sql": e.sql, "origin_error": str(e.origin_error)},
        "FLASK_APP",
        "ExecuteError"
    )
    return make_response(9002, 500), 500


def handle_sqlite_error(e: sqlite3.Error):
    extensions.logger.error(
        {"type": type(e).__name__, "msg": str(e)},
        "FLASK_APP",
        "SqliteError"
    )
    return make_response(9002, 500), 500


def teardown_appcontext(error):
        close_databases()
        if error is not None:
            logs = {
                    "error": {
                        "msg": str(error),
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

import os

from flask import Flask

from .before_request import before_request
from .errorhandler import *
import extensions

def setup_app():
    app = Flask(__name__, static_folder=os.path.join(extensions.root_dir, "static"), template_folder="res", static_url_path="/")

    from app import blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

        for route in bp.routes_:
            extensions.route_manager.register(route["path"], route["auth"], route["is_admin"], route["arguments"])


            

    app.errorhandler(405)(method_not_allowed)
    app.errorhandler(404)(not_found)
    app.errorhandler(500)(internal_server_error)
    # app.errorhandler(ArgumentException)(argument_exception)
    app.teardown_appcontext(teardown_appcontext) # type: ignore
    app.before_request(before_request) # type: ignore
    
    return app
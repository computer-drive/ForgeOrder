from codecs import register
import os

from flask import Flask

from .before_request import before_request
from .after_request import after_request
from .errorhandler import *
import extensions

def setup_app():
    app = Flask(__name__, static_folder=os.path.join(extensions.root_dir, "static"), template_folder="res", static_url_path="/")

    app.json.ensure_ascii = False

    from app import blueprints
    for bp in blueprints:
        bp.register_for_app(app, extensions.route_manager)

        


    app.errorhandler(405)(method_not_allowed)
    app.errorhandler(404)(not_found)
    app.errorhandler(500)(internal_server_error)
    app.errorhandler(415)(unsupported_media_type)
    app.teardown_appcontext(teardown_appcontext) # type: ignore
    app.before_request(before_request) # type: ignore

    app.after_request(after_request)
    
    return app
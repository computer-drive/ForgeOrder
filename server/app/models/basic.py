
import os

from flask import (Blueprint, current_app, jsonify, render_template, request,
                   send_from_directory)

import extensions
from const import *
from core.utils import get_client_ip, make_response
from extensions import *

basic_bp = Blueprint("script", __name__)



@basic_bp.route("/", defaults={"path": ""})
@basic_bp.route("/<path:path>")
def index(path: str = ""):
    if "." in path:
        file_path = os.path.join(current_app.static_folder, path) #type: ignore
        if os.path.exists(file_path):
            return send_from_directory(current_app.static_folder, path) #type: ignore
    
    return send_from_directory(current_app.static_folder, "index.html") #type: ignore

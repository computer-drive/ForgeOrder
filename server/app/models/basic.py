
import os
from flask import Blueprint, jsonify,  render_template, current_app, send_from_directory, request
from extensions import *
import extensions 
from core.utils import make_response, get_client_ip
from const import *

basic_bp = Blueprint("script", __name__)



@basic_bp.route("/", defaults={"path": ""})
@basic_bp.route("/<path:path>")
def index(path: str = ""):
    if "." in path:
        file_path = os.path.join(current_app.static_folder, path) #type: ignore
        if os.path.exists(file_path):
            return send_from_directory(current_app.static_folder, path) #type: ignore
    
    return send_from_directory(current_app.static_folder, "index.html") #type: ignore

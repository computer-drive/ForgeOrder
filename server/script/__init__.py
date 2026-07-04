import os
from flask import Blueprint, render_template, current_app, send_from_directory
from extensions import *
import extensions

basic_bp = Blueprint("script", __name__)

@basic_bp.before_request
def before_request():

    if extensions.server_status == 300:
        return render_template(
            "info.html",
            title = "启动服务器时出错",
            info = extensions.server_info,
        )
    
    elif extensions.server_status == 400:
        return render_template(
            "info.html",
            title = "运行时出错",
            info = extensions.server_info,
        )
    
    elif extensions.server_status == 299:
        return render_template(
            "info.html",
            title = "服务器已关闭",
        )
    
    return None

@basic_bp.route("/", defaults={"path": ""})
@basic_bp.route("/<path:path>")
def index(path: str = ""):
    if "." in path:
        file_path = os.path.join(current_app.static_folder, path) #type: ignore
        if os.path.exists(file_path):
            return send_from_directory(current_app.static_folder, path) #type: ignore
    
    return send_from_directory(current_app.static_folder, "index.html") #type: ignore

    


blueprints = [
    basic_bp
]
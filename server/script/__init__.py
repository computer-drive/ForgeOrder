from flask import Blueprint, render_template
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
    


blueprints = [
    basic_bp
]
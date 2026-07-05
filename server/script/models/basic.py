
import os
from flask import Blueprint, jsonify,  render_template, current_app, send_from_directory, request
from extensions import *
import extensions 
from libs.utils import make_response
from const import *

basic_bp = Blueprint("script", __name__)

@basic_bp.before_request
def before_request():

    # 服务器状态检查
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
    
    
    # 判断是否以/api/开头，以及是否在白名单内
    if  request.path.startswith("/api/"):
        # 未登录状态也可访问的路由
        if request.path in ROUTES.UNLOGGEDIN_ROUTES:
            return None
        else:
            # 需要登录的api请求，进一步判断token
            pass
    else:
        # 正常页面，继续访问
        return None
    
    # 用户登录状态检查
    token = request.headers.get("Authorization", None)

    # 判断token是否有效
    if token is not None and token.startswith("Bearer "):
        token = token.split(" ")[1]
    else:
        return jsonify(make_response(
            2003,
            None
        )) 

    status, result = extensions.auth_manager.verify(token)

    if not status:
        match result:
            case None:
                # token无效
                return jsonify(make_response(
                    2003,
                    None
                )) 
            case "expire":
                # token过期
                return jsonify(make_response(
                    2004,
                    None
                )) 
            case "logout":
                # 用户退出登录
                return jsonify(make_response(
                    2003,
                    None
                )) 
            case "old_device":
                return jsonify(make_response(
                    2005,
                    None
                ))
    else:
        # token 有效，判断是否为管理员页面

        if request.path in ROUTES.ADMIN_ROUTES :
            # 管理员页面，判断用户是否有权限
            return None if result["user"]["is_admin"] == 1 else jsonify(make_response(
                2002,
                None
            ))
        
        else:
            # 非管理员页面，继续请求
            return None


@basic_bp.route("/", defaults={"path": ""})
@basic_bp.route("/<path:path>")
def index(path: str = ""):
    if "." in path:
        file_path = os.path.join(current_app.static_folder, path) #type: ignore
        if os.path.exists(file_path):
            return send_from_directory(current_app.static_folder, path) #type: ignore
    
    return send_from_directory(current_app.static_folder, "index.html") #type: ignore

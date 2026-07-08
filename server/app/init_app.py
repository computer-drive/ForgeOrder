import json
import traceback

from flask import Flask, current_app, jsonify, render_template, request

import extensions
from const import *
from core.utils import get_client_ip, make_response

from .db import close_databases
from .models.exceptions import ArgumentException


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
            # print(1)
            return None
        else:
            # 需要登录的api请求，进一步判断token
            extensions.logger.debug("用户访问需要登录的接口，正在验证Token", "BEFORE_REQUEST", "DebugMsg")
            pass
    else:
        # 正常页面，继续访问
        # print(2)
        return None
    
    # 用户登录状态检查
    token = request.headers.get("Authorization", None)
    extensions.logger.debug(f"请求头中的Authorization是 {token}", "BEFORE_REQUEST", "DebugMsg")


    # 判断token是否有效
    if token is not None and token.startswith("Bearer "):
        token = token.split(" ")[1]
    else:
        return make_response(
            2003,
            None
        ), 401
    
    status, result = extensions.auth_manager.verify(token)
    
    # token无效。处理错误类型，返回正确的status代码
    if not status:
        match result:
            case None:
                # token无效
                extensions.logger.debug("无效的Token", "BEFORE_REQUEST", "DebugMsg")
                return make_response(
                    2003,
                    None
                ) , 401
            case "expire":
                extensions.logger.debug("Token过期", "BEFORE_REQUEST", "DebugMsg")
                # token过期
                return make_response(
                    2004,
                    None
                ) , 401
            case "logout":
                extensions.logger.debug("Token的用户已退出登录", "BEFORE_REQUEST", "DebugMsg")
                # 用户退出登录
                return make_response(
                    2003,
                    None
                ) , 401
            case "old_device":
                extensions.logger.debug("Token的用户在其他设备登录", "BEFORE_REQUEST", "DebugMsg")
                return make_response(
                    2005,
                    None
                ) , 401
    else:
        # token有效，判断ip是否对应
        if result["device_ip"] != get_client_ip(): # type: ignore
            # ip不一致
            extensions.logger.debug(f"token的ip：{result['device_ip']}， 当前ip：{get_client_ip()}，不一致！", "BEFORE_REQUEST", "DebugMsg") # type: ignore
            return make_response(
                2003,
                None
            ) , 401
        
        # token正确，更新到期时间
        extensions.logger.debug("Token有效！", "BEFORE_REQUEST", "DebugMsg")
        
        extensions.auth_manager.update_time(token)
        extensions.logger.debug(f"更新Token的有效时间为：{result['expire']}", "BEFORE_REQUEST", "DebugMsg") # type: ignore
        
        # token 有效，判断是否为管理员页面
        if request.path in ROUTES.ADMIN_ROUTES :
            # 管理员页面，判断用户是否有权限
            extensions.logger.debug(f"访问管理员页面（用户的管理员状态：{result['user']['is_admin']}）", "BEFORE_REQUEST", "DebugMsg") # type: ignore

            if result["user"]["is_admin"] == 1:
                # 管理员页面，继续请求
                return None

            else:
                # 非管理员页面，返回错误
                return jsonify(make_response( # type: ignore
                2002,
                None
            )), 401
        
        else:
            # 非管理员页面，继续请求
            return None




def setup_app():
    app = Flask(__name__, static_folder="static", template_folder="res", static_url_path="/")

    from app import blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    app.errorhandler(405)(method_not_allowed)
    app.errorhandler(404)(not_found)
    app.errorhandler(500)(internal_server_error)
    app.errorhandler(ArgumentException)(argument_exception)
    app.teardown_appcontext(teardown_appcontext) # type: ignore
    app.before_request(before_request) # type: ignore
    
    return app

    

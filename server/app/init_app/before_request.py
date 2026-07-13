from flask import request, g

from core.route_manager.schema import ARGUMENTS
import extensions
from core.utils.server import make_response, get_client_ip

def _handle_auth():
    # 判断是否以/api/开头，以及是否在白名单内
    if  request.path.startswith("/api/"):
        check_result, route_data = extensions.route_manager.verify_auth(request.path)
        
        if not check_result:
            # 没有在RouteMangaer中注册这个路由
            extensions.logger.warning(
                request.path,
                "BEFORE_REQUEST",
                "RouteNotRegistered"
            )
            return None
        

        if not route_data["auth"]:
            # 无需登录
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
                extensions.logger.info({
                    "ip": get_client_ip(),
                    "error": "InvalidToken"
                }, "BEFORE_REQUEST", "AuthError")

                return make_response(
                    2003,
                    None
                ) , 401
            case "expire":
                extensions.logger.info({
                    "ip": get_client_ip(),
                    "error": "TokenExpire"
                }, "BEFORE_REQUEST", "AuthError")
                
                # token过期
                return make_response(
                    2004,
                    None
                ) , 401
            case "logout":
                extensions.logger.info({
                    "ip": get_client_ip(),
                    "error": "TokenLogout"
                }, "BEFORE_REQUEST", "AuthError")
                # 用户退出登录
                return make_response(
                    2003,
                    None
                ) , 401
            case "old_device":
                extensions.logger.info({
                    "ip": get_client_ip(),
                    "error": "OldDevice"
                }, "BEFORE_REQUEST", "AuthError")

                return make_response(
                    2005,
                    None
                ) , 401
    else:
        # token有效，判断ip是否对应
        if result["device_ip"] != get_client_ip(): # type: ignore
            # ip不一致
            extensions.logger.info({
                "ip": get_client_ip(),
                "token_ip": result["device_ip"],
                "error": "IPNotMatch"
            }, "BEFORE_REQUEST", "AuthError") # type: ignore
            
            return make_response(
                2003,
                None
            ) , 401
        
        # token正确，更新到期时间
        extensions.logger.debug("Token有效！", "BEFORE_REQUEST", "DebugMsg")
        
        extensions.auth_manager.update_time(token)
        extensions.logger.debug(f"更新Token的有效时间为：{result['expire']}", "BEFORE_REQUEST", "DebugMsg") # type: ignore
        
        # token 有效，判断是否为管理员页面
        if route_data["is_admin"]:
            # 管理员页面，判断用户是否有权限
            extensions.logger.debug(f"访问管理员页面（用户的管理员状态：{result['user']['is_admin']}）", "BEFORE_REQUEST", "DebugMsg") # type: ignore

            if result["user"]["is_admin"] == 1:
                # 管理员页面，继续请求
                return None

            else:
                extensions.logger.warning(
                    {
                        "path": request.path,
                        "user_id": result["user"]["id"],
                        "ip": get_client_ip(),
                    }, "BEFORE_REQUEST", "NonAdminUserAccess"
                )
                # 非管理员用户，返回错误
                return make_response( # type: ignore
                2002,
                None
            ), 401
        
        else:
            # 非管理员页面，继续请求
            return None

def _handle_args():
    if not extensions.route_manager.has_args(request.path):
        extensions.logger.debug("请求路径 %s，无需验证参数" % request.path, "BEFORE_REQUEST.ARGS", "DebugMsg")
        return None
    
    
    body = request.get_json()
    result, data = extensions.route_manager.verify_args(request.path, body)

    if result in [ARGUMENTS.RESULT.PASS, ARGUMENTS.RESULT.NO_ARGS]:
        # 成功
        g.args = data
        return None
    

    else:
        # 失败
        return make_response(
            1001,
            data
        ), 400

def before_request():
    # 请求前的逻辑
    handlers = [
        _handle_auth,
        _handle_args,
    ]

    for handler in handlers:
        result = handler()
        if result is not None:
            return result
        
    return None

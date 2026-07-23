import uuid
import time

from flask import request, g

from app.routes.schema import ARGUMENTS
import extensions
from core.utils.server import make_response, get_client_ip
from core.log.context import get_log_context
from app.log import RequestLogContext

def _handle_auth():
    logger = g.logger.get_log_context("BEFORE_REQUEST")
    # 判断是否以/api/开头，以及是否在白名单内
    if  request.path.startswith("/api/"):
        check_result, route_data = extensions.route_manager.verify_auth(request.path)
        
        if not check_result:
            
            return make_response(
                1003,
                None
            ), 404
        

        if not route_data["auth"]:
            # 无需登录
            return None
        else:
            # 需要登录的api请求，进一步判断token
            logger.debug("访问需认证接口。", "DebugMsg")
            pass
    else:
        # 正常页面，继续访问
        # print(2)
        return None
    
    # 用户登录状态检查
    token = request.headers.get("Authorization", None)


    # 判断token是否有效
    if token is None:
        logger.debug("无Token。", "DebugMsg")
        return make_response(
            2001,
            None
        ), 401
    
    elif token.startswith("Bearer "):
        token = token.split(" ")[1]
    else:
        logger.debug("Token格式错误。", "DebugMsg")
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
                logger.info({
                    "ip": get_client_ip(),
                    "error": "InvalidToken"
                }, "AuthError")

                return make_response(
                    2003,
                    None
                ) , 401
            case "expire":
                logger.info({
                    "ip": get_client_ip(),
                    "error": "TokenExpire"
                }, "AuthError")
                
                # token过期
                return make_response(
                    2004,
                    None
                ) , 401
            case "logout":
                logger.info({
                    "ip": get_client_ip(),
                    "error": "TokenLogout"
                }, "AuthError")
                # 用户退出登录
                return make_response(
                    2003,
                    None
                ) , 401
            case "old_device":
                logger.info({
                    "ip": get_client_ip(),
                    "error": "OldDevice"
                }, "AuthError")

                return make_response(
                    2005,
                    None
                ) , 401
    else:
        # token有效，判断ip是否对应
        if result["device_ip"] != get_client_ip(): # type: ignore
            # ip不一致
            logger.info({
                "ip": get_client_ip(),
                "token_ip": result["device_ip"],
                "error": "IPNotMatch"
            }, "AuthError") # type: ignore
            
            return make_response(
                2003,
                None
            ) , 401
        
        # token正确，更新到期时间
        logger.debug("Token有效。", "DebugMsg")
        
        extensions.auth_manager.update_time(token)

        logger.debug(f"更新Token的有效时间为%s " % result['expire'], "DebugMsg") # type: ignore
        
        # token 有效，判断是否为管理员页面
        if route_data["is_admin"]:
            # 管理员页面，判断用户是否有权限
            logger.debug(f"访问管理员接口。", "DebugMsg") # type: ignore

            if not result["user"]["is_admin"] == 1:
                logger.warning(
                    {
                        "path": request.path,
                        "user_id": result["user"]["id"],
                        "ip": get_client_ip(),
                    },  "NonAdminUserAccess"
                )
                # 非管理员用户，返回错误
                return make_response( # type: ignore
                2002,
                None
            ), 401
        
        # 继续请求
        g.user_info = result

def _handle_args():
    logger = extensions.get_log_context(extensions.logger, "BEFORE_REQUEST")

    if not extensions.route_manager.has_args(request.path):
        logger.debug("请求路径 %s，无需验证参数" % request.path, "DebugMsg")
        return None
    
    
    body = request.get_json()
    result, data = extensions.route_manager.verify_args(request.path, body)

    if result in [ARGUMENTS.RESULT.PASS, ARGUMENTS.RESULT.NO_ARGS]:
        # 成功
        g.args = data
        # print("set")
        return None
    

    else:
        # 失败
        return make_response(
            1001,
            data
        ), 400

def _handle_request_info():
    g.request_id = str(uuid.uuid4())

    
    g.logger = RequestLogContext(extensions.logger, "REQUEST")


    g.start_time = time.time()

    return None

def before_request():
    # 请求前的逻辑
    handlers = [
        _handle_request_info,
        _handle_auth,
        _handle_args,
        
    ]

    for handler in handlers:
        result = handler()
        if result is not None:
            return result
        
    return None

from typing import TypedDict, Any
from dataclasses import dataclass

from .field import BodyField, PathField
from .responseGenerator import ResponseInfo


class RoutesInfo(TypedDict):
    isAdmin: bool
    requiresAuth: bool
    bodyParams: dict[str, BodyField]
    pathParams: dict[str, PathField]
    responses: list[ResponseInfo]


class GLOBAL:
    ARGUMNET_ERROR = ResponseInfo(1001, "ArgumentError", None)
    # 请求参数错误

    METHOD_ERROR = ResponseInfo(1002, "MethodError", None)
    # 请求的HTTP方法错误

    NOT_FOUND = ResponseInfo(1003, "NotFound", None)
    # 请求资源不存在

    PAYLOAD_ERROR = ResponseInfo(1004, "PayloadError", None)
    # 请求体的类型错误


    NOT_LOGIN_ERROR = ResponseInfo(2001, "NotLoginError", None)
    # 未登录错误

    PERMISSION_ERROR = ResponseInfo(2002, "PermissionError", None)
    # 权限错误

    TOKEN_INVALID_ERROR = ResponseInfo(2003, "TokenInvalidError", None)
    # 令牌无效错误

    TOKEN_EXPIRED_ERROR = ResponseInfo(2004, "TokenExpiredError", None)
    # 令牌过期错误

    OLD_DEVICE_TOKEN = ResponseInfo(2005, "OldDeviceToken", None)
    # 旧设备令牌

    
    SERVER_ERROR = ResponseInfo(9010, "ServerError", None)
    # 服务器错误

    DATABASE_ERROR = ResponseInfo(9020, "DatabaseError", None)
    # 数据库错误

    DATABASE_BUSY = ResponseInfo(9021, "DatabaseBusy", None)
    # 数据库繁忙错误

    SERVER_CLOSED = ResponseInfo(9011, "ServerClosed", None)
    # 服务器已关闭

    


    












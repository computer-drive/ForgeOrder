from flask import Blueprint, request, jsonify
from core.utils import make_response, verify_args, get_client_ip
import json
from ..db import get_main_database
from .exceptions import *
from werkzeug.security import check_password_hash
import extensions

accounts_bp = Blueprint("accounts", __name__)

@accounts_bp.route("/api/auth/login", methods=["POST"])
def login():
    username = request.get_json().get("username", None)
    password = request.get_json().get("password", None)
    cover = request.get_json().get("cover", False)

    ip = get_client_ip()

    args_invalid = verify_args({
        'username': username,
        'password': password,
        'cover': cover
    }, [
        {
            "arg_name": "username",
            "arg_type": str,
            "required": True
        },
        {
            "arg_name": "password",
            "arg_type": str,
            "required": True
        },
        {
            "arg_name": "cover",
            "arg_type": bool,
            "required": False
        }
    ])
    if args_invalid != []:
        raise ArgumentException(args_invalid)
    
    # 连接数据库
    main_db = get_main_database()
    
    # 查询用户
    account = main_db.users.get_from_username(username)

    # 检查用户是否存在
    if account is None:
        
        return make_response(
            3001,
            None
        )
    
    # 检查密码是否正确
    if check_password_hash(account["password"], password):
        # 检查用户是否已禁用
        if account["is_available"]:
            # 添加Token
            extensions.logger.debug(f"登录验证成功。设备（{ip}正在尝试登录{username}", "LOGIN_REQUEST", "DebugMsg")
            extensions.logger.debug("生成Token...", "LOGIN_REQUEST", "DebugMsg")

            if cover:
                extensions.logger.debug("注意到cover=True", "LOGIN_REQUEST", "DebugMsg")

            status, result = extensions.auth_manager.user_login(
                dict(account),
                ip, #type: ignore
                cover
            )

            if status:
                # 成功生成了Token, result为Token值
                token = result
                extensions.logger.debug(f"成功生成Token：{token}", "LOGIN_REQUEST", "DebugMsg")

                extensions.logger.info(
                    json.dumps({
                        "ip": get_client_ip(),
                        "user_id": account["id"],
                        "cover": cover
                    }), "ACCOUNTS", "UserLogin"
                )

                return make_response(
                    0,
                    {
                        "user_info": dict(account),
                        "token": token
                    }
                )
            
            elif result[0] == 0:
                # 失败，重复登录
                extensions.logger.debug(f"生成失败，重复登录。请求ip:{ip}, token中的ip:{result[1]}", "LOGIN_REQUEST", "DebugMsg")
                return make_response(
                    3003,
                    {
                        "user_info": dict(account),
                        "token": result[1]["token"]
                    }
                )
            else:
                # 失败，设备重复登录
                extensions.logger.debug(f"生成失败，有新设备登录。请求ip:{ip}, token中的ip:{result[1]}", "LOGIN_REQUEST", "DebugMsg")
                return make_response(
                    3004,
                    {
                        "old_device_ip": result[1]
                    }
                )

        

        
        else:
            return make_response(
                3002,
                None
            )
    else:
        return make_response(
            3001,
            None
        )
        
@accounts_bp.route("/api/auth/logout", methods=["POST"])
def logout():
    token = request.headers.get("Authorization")


    token = token.split(" ")[1] #type: ignore
    
    
    token_item : dict = extensions.auth_manager.user_logout(token) #type: ignore

    

    extensions.logger.info(
        json.dumps({
            "ip": get_client_ip(),
            "user_id": token_item["user"]["id"],
        }), "ACCOUNTS", "UserLogout"
    )

    return make_response(
        0,
        None
    )
    


@accounts_bp.route("/api/auth/test")
def test_api():
    return make_response(
        0,
        "Test Pass"
    )
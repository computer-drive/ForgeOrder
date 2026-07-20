import json

from flask import  request, g
from werkzeug.security import check_password_hash

import extensions
from core.app_bp import AppBlueprint
from core.utils import get_client_ip, make_response
from core.log.context import get_log_context

from ..db.get_db import get_database
from .exceptions import *

accounts_bp = AppBlueprint("accounts", __name__)



 
@accounts_bp.post("/api/auth/login",              
    arguments = [   
            {
                "name": "username",
                "type": str,
                "required": True
            },
            {
                "name": "password",
                "type": str,
                "required": True
            },
            {
                "name": "cover",
                "type": bool,
                "required": False,
                "default": False
            }
    ],
    auth=False,
    is_admin=False
)
def login():
    logger = g.logger.get_log_context("ACCOUNTS")

    g.logger.set_category("LOGIN_REQUEST")

    username = g.args["username"]
    password = g.args["password"]
    cover = g.args["cover"]

    ip = get_client_ip()

    
    
    # 连接数据库
    main_db = get_database()
    
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
            g.logger.debug(f"登录验证成功。设备（{ip}正在尝试登录{username}",  "DebugMsg")
            g.logger.debug("生成Token...",  "DebugMsg")

            if cover:
                g.logger.debug("注意到cover=True",  "DebugMsg")

            status, result = extensions.auth_manager.user_login(
                dict(account),
                ip, #type: ignore
                cover
            )

            if status:
                # 成功生成了Token, result为Token值
                token = result
                g.logger.debug(f"成功生成Token：{token}",  "DebugMsg")

                logger.info(
                    {
                        "ip": get_client_ip(),
                        "user_id": account["id"],
                        "cover": cover
                    },  "UserLogin", g.request_id
                )

                account = dict(account).copy()
                account.pop("password", None)
                
                return make_response(
                    0,
                    {
                        "user_info": account,
                        "token": token
                    }
                )
            
            elif result[0] == 0:
                # 失败，重复登录
                g.logger.debug(f"生成失败，重复登录。请求ip:{ip}, token中的ip:{result[1]}",  "DebugMsg")
                return make_response(
                    3003,
                    {
                        "user_info": dict(account),
                        "token": result[1]["token"]
                    }
                )
            else:
                # 失败，设备重复登录
                g.logger.debug(f"生成失败，有新设备登录。请求ip:{ip}, token中的ip:{result[1]}", "DebugMsg")
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
        
@accounts_bp.post("/api/auth/logout", auth=True)
def logout():
    logger = g.logger.get_log_context("ACCOUNTS")

    token = request.headers.get("Authorization")

    if not token:
        return make_response(
            1001,
            None
        )
    token = token.split(" ")[1] #type: ignore
    
    
    token_item : dict = extensions.auth_manager.user_logout(token) #type: ignore

    

    logger.info(
        {
            "ip": get_client_ip(),
            "user_id": token_item["user"]["id"],
        }, "UserLogout", g.request_id)
    

    return make_response(
        0,
        None
    )
    


@accounts_bp.route("/api/auth/test", auth=True)
def test_api():
    return make_response(
        0,
        "Test Pass"
    )
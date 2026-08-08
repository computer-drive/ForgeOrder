
from flask import  request, g
from werkzeug.security import check_password_hash

from app.routes.res_generator import ResponseInfo
import extensions
from app.routes.app_bp import AppBlueprint
from core.utils import get_client_ip, make_response
from ..db.get_db import get_database_flask
from .exceptions import *
from app.routes.field import RequestField, NotEmpty

accounts_bp = AppBlueprint("accounts", __name__)

@accounts_bp.post("/api/auth/login",              
    arguments = [   
        RequestField("username", str, True, None, NotEmpty()),
        RequestField("password", str, True, None, NotEmpty()),
        RequestField("cover", bool, False, False)
    ],
    auth=False,
    is_admin=False,
    responses=[
        ResponseInfo(0, "OK", dict),
        ResponseInfo(3001, "UsernameOrPasswordError", None),
        ResponseInfo(3002, "UserIsDisabled", None),
        ResponseInfo(3003, "RepeatLogin", dict),
        ResponseInfo(3004, "NewDeviceLogin", dict),
    ]
)
def login():
    logger = g.logger.get_log_context("ACCOUNTS")

    g.logger.set_category("LOGIN_REQUEST")

    username = g.args["username"]
    password = g.args["password"]
    cover = g.args["cover"]

    ip = get_client_ip()

    
    
    # 连接数据库
    main_db = get_database_flask()
    
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
        # 密码正确

        # 检查用户是否已禁用
        if account["is_available"]:
            # 用户未禁用

            # 在AuthManager上执行登录验证
            status, result = extensions.auth_manager.user_login(
                dict(account), #type: ignore
                ip, #type: ignore
                cover
            )

            if status:
                # 登录成功
                token = result

                logger.info(
                    {
                        "ip": get_client_ip(),
                        "user_id": account["id"],
                        "cover": cover
                    },  "UserLogin"
                )

                account = dict(account).copy()
                account.pop("password", None)
                
                return g.res.OK({
                    "user_info": account,
                    "token": token
                })
            
            elif result[0] == 0:
                # 失败，重复登录
                logger.info(
                    {
                        "ip": get_client_ip(),
                        "user_id": account["id"],
                        "cover": cover
                    },  "UserRepeatLogin", g.request_id
                )

                return g.res.RepeatLogin({
                        "user_info": dict(account),
                        "token": result[1]["token"] #type: ignore
                    }
                )
            else:
                # 失败，新设备登录
               
                logger.info({
                    "current_ip": ip,
                    "old_device_ip": result[1],
                    "user_id": account["id"],
                    "cover": cover
                })

                return g.res.NewDeviceLogin(
                    {
                        "old_device_ip": result[1]
                    }
                )


        
        else:
            # 用户已禁用
            return g.res.UserIsDisabled(
                None
            )
    else:
        # 密码错误
        return g.res.UsernameOrPasswordError(
            None
        )
        
@accounts_bp.post("/api/auth/logout", auth=True,
                  responses=[
                      ResponseInfo(0, "OK", None),
                  ])
def logout():
    logger = g.logger.get_log_context("ACCOUNTS")

    token = request.headers.get("Authorization")

    
    token = token.split(" ")[1] #type: ignore
    
    token_item : dict = extensions.auth_manager.user_logout(token) #type: ignore

    if token_item is None:
        return make_response(2003, None), 401

    logger.info(
        {
            "ip": get_client_ip(),
            "user_id": token_item["user"]["id"],
        }, "UserLogout", g.request_id)
    

    return g.res.OK(
        0,
        None
    )
    



@accounts_bp.route("/test_print")
def test_print():
    from app.printer.receipt import Receipt

    receipt = Receipt()
    
    receipt.build.text("123")
    receipt.build.qr_code("https://baidu.com")

    
    extensions.print_manager.new(receipt)

    return "ok"

VERSION = "1.0.1"

class LOG:
    FORMAT = "%(color)s[%(asctime)s/%(class_name)s] %(levelname)s in %(method)s %(message)s%(reset)s"

    BUFFER_SIZE = 100


class CONFIG:
    DEFAULT = {
        "server.host": "0.0.0.0",
        "server.port": 5000,

        "log.level": "info",
        "log.database": "data/log.db",
        "log.debug_ignore": [],

        "main_db": "data/main.db",
        "meta_db": "data/meta.db",

        "auth.secret_key": "development_key",
        "auth.available_time": 60, # 60分钟

        "server.env": "dev",
    }

    CONFIG_PATH = "data/config.json"

class ROUTES:
    # 未登录状态也可访问的路由
    UNLOGGEDIN_ROUTES = [
        "/api/auth/login",
        "/api/system/getSystemInfo"
    ]

    # 仅管理员可访问的路由
    ADMIN_ROUTES = [
        "/api/shop/setBusinessState",
    ]

class ARGUMENTS_MANAGER:
    # 与core.utils.routes下的ArgumentsManager有关

    class RESULT:
        # ArgumentsManager.verify_args的返回值
        PASS = 0 # 验证成功
        FAILED = 1 # 验证失败
        NO_ARGS = 2 # 未注册（无参数）

    class ERROR:
        NOT_FOUND = "NOT_FOUND" # 未找到参数
        TYPING_ERROR = "TYPING_ERROR" # 类型错误
       
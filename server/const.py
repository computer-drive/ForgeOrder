
class LOG:
    FORMAT = "%(color)s[%(asctime)s/%(class_name)s] %(levelname)s in %(method)s: %(message)s%(reset)s"

    BUFFER_SIZE = 100


class CONFIG:
    DEFAULT = {
        "server.host": "0.0.0.0",
        "server.port": 5000,
        "log.level": "info",
        "log.database": "log.db",

        "main_db": "main.db",
        "meta_db": "meta.db",

        "auth.secret_key": "development_key",
        "auth.available_time": 60, # 60分钟

        "server.env": "dev",
    }

class ROUTES:
    # 未登录状态也可访问的路由
    UNLOGGEDIN_ROUTES = [
        "/api/auth/login"
    ]

    # 管理员可访问的路由
    ADMIN_ROUTES = [
        
    ]
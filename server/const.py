
VERSION = "1.0.1"




class CONFIG:
    DEFAULT = {
        "server.host": "0.0.0.0",
        "server.port": 5000,

        "log.level": "info",
        "log.database": "data/log.db",
        "log.debug_ignore": [],
        "log.ignore_client_error": False,

        "main_db": "data/main.db",
        "meta_db": "data/meta.db",

        "auth.secret_key": "development_key",
        "auth.available_time": 60, # 60分钟

        "server.env": "dev",
    }

    CONFIG_PATH = "data/config.json"




       
from dataclasses import dataclass
from multiprocessing.reduction import steal_handle
from os import name

@dataclass
class ConfigItem:
    name: str
    typing: type
    default: any

CONFIG_ITEMS = [
    ConfigItem("server.host", str, "0.0.0.0"),
    ConfigItem("server.port", int, 5000),

    ConfigItem("log.level", str, "info"),
    ConfigItem("log.database", str, "data/log.db"),
    ConfigItem("log.debug_ignore", list, []),
    ConfigItem("log.ignore_client_error", bool, False),
    ConfigItem("database.path", str, "data/main.db"),
    
    ConfigItem("auth.secret_key", str, "development_key"),
    ConfigItem("auth.available_time", int, 60),

    ConfigItem("server.env", str, "dev"),
]

CONFIG_PATH = "data/config.json"
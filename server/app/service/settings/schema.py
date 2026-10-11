from dataclasses import dataclass
from typing import Any

from core.validation.validators import Validator, NotEmpty, Range, Choices


@dataclass
class SettingsField:
    id: int
    name : str
    type: Any
    default: Any = None
    validator: Validator | None = None

    description: str = ""


class KEYS:
     SERVER_HOST = 'server.host'
     SERVER_PORTS = 'server.ports'
     SERVER_WORKER_THREADS = 'server.worker.threads'

     WS_HOST = 'websocket.host'
     WS_PORT = 'websocket.port'

     LOG_LEVEL = 'log.level'
     LOG_DATABASE = 'log.database'

     SHOP_NAME = 'shop.name'

     PRINTER_ENABLED = 'printer.enabled'
     PRINTER_NAME = 'printer.name'

SETTINGS_SCHEMA = [
    SettingsField(10001, KEYS.SERVER_HOST, str, "0.0.0.0", NotEmpty(),
        "服务器的主机地址。"),

    SettingsField(10002, KEYS.SERVER_PORTS, int, 5000, Range().MinEqual(0).MaxEqual(65535),
        "服务器端口号。填入的数量为服务器启动Worker的数量。"),

    SettingsField(10003, KEYS.SERVER_WORKER_THREADS, int, 4, Range().MinEqual(0),
        "每个Worker的线程数。一般来讲，服务器能同时处理的请求数量为每个Worker的线程数 * 工作线程数。"),

    SettingsField(11001, KEYS.WS_HOST, str, "0.0.0.0", NotEmpty(),
        "WebSocket服务器的主机地址。一般与服务器的主机地址相同。"),

    SettingsField(11002, KEYS.WS_PORT, int, 8765, Range().MinEqual(0).MaxEqual(65535),
        "WebSocket服务器的端口号。"),

    SettingsField(12001, KEYS.LOG_LEVEL, str, "info", Choices(["info", "debug", "error", "warning"]),
        "记录日志的级别。debug > info > warning > error，低于当前级别的日志不会被记录。"),

    SettingsField(12002, KEYS.LOG_DATABASE, str, "log.db", NotEmpty(),
        "记录日志的数据库名称。相对路径与绝对路径均可，相对路径为当前工作目录。"),

    SettingsField(13001, KEYS.SHOP_NAME, str, "ForgeOrder", NotEmpty(),
        "店铺名称。"),

    SettingsField(14001, KEYS.PRINTER_ENABLED, bool, False, NotEmpty(),
        "是否启用打印服务。"),

    SettingsField(14002, KEYS.PRINTER_NAME, str, "ForgeOrder", NotEmpty(),
        "打印机名称。"),
]
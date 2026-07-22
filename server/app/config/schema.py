import os

from core.config.validation import Choices, NotEmpty, SettingsProperty, NotEmpty, Interval, FunctionHandler, AllOf, Open, Closed, VerifyError, VerifyResult

def auth_secret_key_verify(value: str):
    if os.environ.get("ENV") == "product" and value == "development_key":
        return VerifyResult(False, VerifyError("生产环境不能使用开发密钥"))
    else:
        return VerifyResult(True)
    

CONFIG_ITEMS = [
    SettingsProperty("server.host", str, "0.0.0.0", NotEmpty()),
    SettingsProperty("server.port", int, 5000, Interval(1, 65535)),
    SettingsProperty("log.level", str, "info", Choices("debug", "info", "warning", "error", "critical")),
    SettingsProperty("log.database", str, "data/log.db", NotEmpty()),

    SettingsProperty("log.debug_ignore", list, []),
    SettingsProperty("log.ignore_client_error", bool, False),

    SettingsProperty("database.path", str, "data/main.db", NotEmpty()),

    SettingsProperty("auth.secret_key", str, "development_key", AllOf(NotEmpty(), FunctionHandler(auth_secret_key_verify))),
    SettingsProperty("auth.available_time", int, 60, Interval(Open(0), None)), # 无上限

    SettingsProperty("server.env", str, "dev", Choices("dev", "product")),
    SettingsProperty("server.first_start", bool, True),

]

CONFIG_PATH = "data/config.json"
# 验证配置项的有效性
from os import error

import extensions
from .exceptions import ConfigError
from .schema import CONFIG_ITEMS

def verify_config():
    errors = []

    for item in CONFIG_ITEMS:
        value = extensions.config.get(item.name)

        if isinstance(value, item.typing) is False:
            errors.append(f"{item.name}({type(value).__name__}<{value}>)：必须是{item.typing.__name__}类型")

    item = extensions.config.get("server.port")
    if not (0 <= item < 65536):
        errors.append(f"server.port({item})：必须在0-65535之间")

    item = extensions.config.get("log.level")
    if item not in ["debug", "info", "warning", "error", "critical"]:
        errors.append(f"log.level({item})：必须是debug、info、warning、error或critical")


    item = extensions.config.get("auth.secret_key")
    if item == "":
        errors.append(f"auth.secret_key({item})：必须是非空字符串")


    item = extensions.config.get("auth.available_time")
    if item <= 0:
        errors.append(f"auth.available_time({item})：必须是正整数")

    if errors:
        raise ConfigError(errors)

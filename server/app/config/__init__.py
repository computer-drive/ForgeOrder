from server.core.config.json_config import JSONConfig
from .schema import CONFIG_ITEMS
from .verify import verify_config
from const import CONFIG_PATH


def setup_config():

    default = {}

    for item in CONFIG_ITEMS:
        default[item.name] = item.default

    return JSONConfig(
        CONFIG_PATH,
        default,
    )
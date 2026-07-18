from core.config import Config
from .schema import CONFIG_ITEMS
from .verify import verify_config

def setup_config():

    default = {}

    for item in CONFIG_ITEMS:
        default[item.name] = item.default

    return Config(
        "data/config.json",
        default,
    )
from .accounts import accountsBlueprint
from .basic import basicBlueprint
from .shop import shopBlueprint
from .system import systemBlueprint
from .orders import ordersBlueprint

blueprints = [
    accountsBlueprint,
    shopBlueprint,
    systemBlueprint,
    ordersBlueprint,
    basicBlueprint,
]
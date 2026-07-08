from .models.accounts import accounts_bp
from .models.basic import basic_bp
from .models.shop import shop_bp
from .models.system import system_bp

blueprints = [
    basic_bp,
    accounts_bp,
    shop_bp,
    system_bp
]
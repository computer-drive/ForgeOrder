import os

from core.validation.field import FieldDefinition
from core.validation.validators import Choices, NotEmpty, Interval, AllOf, Open, Closed
from core.validation.base import ValidationResult


class CONFIG:
    # Server
    SERVER_HOST = "server.host"
    SERVER_PORT = "server.port"
    SERVER_ENV = "server.env"

    # 被弃用的
    # SERVER_FIRST_START = "server.first_start"
    
    # Log
    LOG_LEVEL = "log.level"
    LOG_DATABASE = "log.database"
    LOG_DEBUG_IGNORE = "log.debug_ignore"
    LOG_IGNORE_CLIENT_ERROR = "log.ignore_client_error"
    
    # Database
    DATABASE_PATH = "database.path"
    
    # Auth
    AUTH_AVAILABLE_TIME = "auth.available_time"


    
    
CONFIG_ITEMS = [
    FieldDefinition(CONFIG.SERVER_HOST, str, "0.0.0.0", NotEmpty()),
    FieldDefinition(CONFIG.SERVER_PORT, int, 5000, Interval(1, 65535)),
    FieldDefinition(CONFIG.LOG_LEVEL, str, "info", Choices("debug", "info", "warning", "error", "critical")),
    FieldDefinition(CONFIG.LOG_DATABASE, str, "data/log.db", NotEmpty()),

    FieldDefinition(CONFIG.LOG_DEBUG_IGNORE, list, []),
    FieldDefinition(CONFIG.LOG_IGNORE_CLIENT_ERROR, bool, False),

    FieldDefinition(CONFIG.DATABASE_PATH, str, "data/main.db", NotEmpty()),

    FieldDefinition(CONFIG.AUTH_AVAILABLE_TIME, int, 60, Interval(Open(0), None)), # 无上限

    FieldDefinition(CONFIG.SERVER_ENV, str, "dev", Choices("dev", "product")),
    # FieldDefinition(CONFIG.SERVER_FIRST_START, bool, True), # 被弃用的

]

# CONFIG_PATH = "data/config.json"
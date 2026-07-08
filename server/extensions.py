# 全局对象，供所有脚本使用
from core.log.logger import Logger
from threading import Thread
from queue import Queue
from core.config import Config
from core.auth import AuthManager

logger : Logger 
db_logger_thread : Thread
db_logger_queue : Queue

auth_manager : AuthManager

server_status : int = -1
server_info: str = ""

config : Config

is_business: bool = True

local_ip: str = ""
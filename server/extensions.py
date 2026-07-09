# 全局对象，供所有脚本使用
from queue import Queue
from threading import Thread
import os

from core.auth import AuthManager
from core.config import Config
from core.log.logger import Logger

logger : Logger 
db_logger_thread : Thread
db_logger_queue : Queue

auth_manager : AuthManager

# server_status : int = -1
# server_info: str = ""

config : Config

is_business: bool = True

local_ip: str = ""

root_dir = os.path.dirname(os.path.abspath(__file__))

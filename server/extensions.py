# 全局对象，供所有脚本使用
# quanb 
from libs.log.logger import Logger
from threading import Thread
from queue import Queue
from libs.config import Config



logger : Logger 
db_logger_thread : Thread
db_logger_queue : Queue




server_status : int = -1
server_info: str = ""

config : Config
# 全局对象，供所有脚本使用
# quanb 
from libs.log.logger import Logger
from threading import Thread
from queue import Queue

logger : Logger = None # type:ignore
db_logger_thread : Thread = None   # type:ignore
db_logger_queue : Queue = None # type:ignore

server_status : int = -1
server_info: str = ""

# 全局对象，供所有脚本使用
# quanb 
from libs.log.logger import Logger
from threading import Thread
from queue import Queue
from libs.config import Config
from script.main_db import MainDatabase
from script.meta_db import MetaDatabase


logger : Logger 
db_logger_thread : Thread
db_logger_queue : Queue

meta_db : MetaDatabase 
main_db : MainDatabase


server_status : int = -1
server_info: str = ""

config : Config
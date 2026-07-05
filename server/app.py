import extensions
from libs.log.logger import setup_logger
import logging
from libs.utils import create_server_info_by_exception
from libs.config import Config
from script.models.exceptions import *
from libs.auth import AuthManager
import os
from script.init_app import setup_app

def init():
    # 加载配置文件
    extensions.config = Config("config.json")

    # 初始化日志记录器
    try:
        logger, thread, queue = setup_logger(__name__, extensions.config.get("log.database")) #type: ignore
    
    
        extensions.logger = logger
        extensions.db_logger_thread = thread
        extensions.db_logger_queue = queue

        extensions.auth_manager = AuthManager(
            extensions.config.get("auth.secret_key"),
            int(extensions.config.get("auth.available_time")),
        )

    
    except Exception as e:
        extensions.server_status = 300
        extensions.server_info = create_server_info_by_exception(e)
        print(extensions.server_info)
        return

    extensions.server_status = 101

def shutdown():
    # 关闭数据库日志记录器线程
    if extensions.db_logger_thread is None:
        return
    
    extensions.db_logger_queue.join()
    extensions.db_logger_queue.put(None)

    extensions.db_logger_thread.join()

    logging.shutdown()


if __name__ == "__main__":
    # 加载配置文件
    init()

    # 设置环境
    os.environ["ENV"] = extensions.config.get("server.env")

    # 初始化flask
    app = setup_app()
    extensions.server_status = 100

    
    # 运行服务器
    extensions.server_status = 200
    app.run(
        host=extensions.config.get("server.host"), #type: ignore
        port=extensions.config.get("server.port"), #type: ignore
    )

    # 关闭服务器
    extensions.server_status = 299

    shutdown()




    

    
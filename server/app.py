import logging
import os

import extensions
from app.init_app import setup_app
from app.models.exceptions import *
from const import *
from core.auth import AuthManager
from core.config import Config
from core.log.logger import setup_logger
from core.utils import create_server_info_by_exception, get_local_ip


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
    
    extensions.local_ip = get_local_ip()

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
    extensions.logger.debug(f"版本：{VERSION}, IP地址：{extensions.local_ip}", "MAIN", "DebugMsg")

    # 设置环境
    os.environ["ENV"] = extensions.config.get("server.env")

    # 初始化flask
    app = setup_app()
    extensions.server_status = 100

    
    # 运行服务器
    extensions.server_status = 200
    if os.environ["ENV"] == "product":
        extensions.logger.debug("生产环境运行！", "MAIN", "DebugMsg")

        from waitress import serve
        serve(app, host=extensions.config.get("server.host"), port=extensions.config.get("server.port"))
    else:
        app.run(
            host=extensions.config.get("server.host"), #type: ignore
            port=extensions.config.get("server.port"), #type: ignore
        )

    # 关闭服务器
    extensions.server_status = 299

    shutdown()




    

    
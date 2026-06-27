import extensions
from libs.log.logger import setup_logger
import logging
from flask import Flask
import threading
from script import blueprints
from libs.utils import create_server_info_by_exception

def setup_app():
    app = Flask(__name__, static_folder="static", template_folder="res")

    for bp in blueprints:
        app.register_blueprint(bp)

    return app


def init():
    # 初始化日志记录器
    try:
        logger, thread, queue = setup_logger(__name__, "log.db")
    except Exception as e:
        extensions.server_status = 300
        extensions.server_info = create_server_info_by_exception(e)
        return
    
    extensions.logger = logger
    extensions.db_logger_thread = thread
    extensions.db_logger_queue = queue
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
    # 初始化flask
    app = setup_app()
    extensions.server_status = 100

    # 初始化服务
    load_thread = threading.Thread(target=init)
    load_thread.start()

    # 运行服务器
    extensions.server_status = 200
    app.run()

    # 关闭服务器
    extensions.server_status = 299

    shutdown()

    load_thread.join()



    

    
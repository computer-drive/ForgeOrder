import extensions
from libs.log.logger import setup_logger
import logging
from flask import Flask
import threading
from script import blueprints

def setup_app():
    app = Flask(__name__, static_folder="static", template_folder="res")

    for bp in blueprints:
        app.register_blueprint(bp)

    return app


def init():
    # 初始化日志记录器
    logger, thread, queue = setup_logger(__name__, "log.db")
    extensions.logger = logger
    extensions.db_logger_thread = thread
    extensions.db_logger_queue = queue
    extensions.server_status = 101

def shutdown():
    # 关闭数据库日志记录器线程
    extensions.db_logger_queue.join()
    extensions.db_logger_queue.put(None)

    extensions.db_logger_thread.join()

    logging.shutdown()


if __name__ == "__main__":
    app = setup_app()
    extensions.server_status = 100

    load_thread = threading.Thread(target=init)
    load_thread.start()

    extensions.server_status = 200
    app.run()

    extensions.server_status = 299
    shutdown()



    

    
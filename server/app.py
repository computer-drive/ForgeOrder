import extensions
from libs.log.logger import setup_logger
import logging

def init():
    # 初始化日志记录器
    logger, thread, queue = setup_logger("ForgeOrder")
    extensions.logger = logger
    extensions.db_logger_thread = thread
    extensions.db_logger_queue = queue

def shutdown():
    # 关闭数据库日志记录器线程
    extensions.db_logger_queue.join()
    extensions.db_logger_queue.put(None)

    extensions.db_logger_thread.join()

    logging.shutdown()


if __name__ == "__main__":
    init()

    extensions.logger.info("Hello, World!", "app", "main")
    extensions.logger.warning("Hello, World!", "app", "main")
    extensions.logger.error("Hello, World!", "app", "main")
    extensions.logger.critical("Hello, World!", "app", "main")
    extensions.logger.debug("Hello, World!", "app", "main")

    shutdown()



    

    
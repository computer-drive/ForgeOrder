# 用于读取日志队列中的日志
from multiprocessing import Queue

from core.log import Logger



def readLogQueue(logQueue: Queue, logger: Logger):
    while True:
        log = logQueue.get()
        if log is None:
            break

        logger.logWithTimestamp(
            log["msg"],
            log["level"],
            log["category"],
            log["action"],
            log["timestamp"],
            log["requestId"],
        )

      

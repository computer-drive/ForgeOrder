import time
import os
import threading

from app.init import init, shutdown
from app.const import VERSION
from core.errorHandler.excepthook import installExcepthook
from core.log import getConsoleLogger, getLogContext, getLogger
from app.config import config, CONFIG
from app.bininfo import bininfo, KEYS
from app.processing.base import startWorkers
from app.processing.log.read import readLogQueue

# 安装全局异常处理器
installExcepthook() 


    

if __name__ == "__main__":

    consoleLogger= getConsoleLogger("main")

    initTime = time.time()

    init()

    ## 设置环境变量
    os.environ["ENV"] = config.get(CONFIG.SERVER_ENV)

    logger = getLogContext(getLogger(), "Main")

    
    logger.debug({
        "version": VERSION,
        "environment": os.environ["ENV"],
        "workersPort": config.get(CONFIG.SERVER_WORKER_PORT),
        "host": config.get(CONFIG.SERVER_HOST)
    }, "RuntimeInfo")

    bininfo[KEYS.IS_NORMAL_SHUTDOWN] = False # 先设置为False，等服务正常退出后再设置为True
    bininfo[KEYS.STARTUP_COUNT] += 1
    bininfo[KEYS.LAST_START_TIMESTAMP] = int(time.time())
    bininfo.save()



    consoleLogger.info("正在启动HTTP服务...")

    workers, logQueue, printerQueue, stopEvent = startWorkers(
        host=config.get(CONFIG.SERVER_HOST),
        ports=config.get(CONFIG.SERVER_WORKER_PORT),
        threads=config.get(CONFIG.SERVER_WORKER_THREADSS)
    )

    # 启动日志读取线程
    readLogThread = threading.Thread(target=readLogQueue, args=(logQueue, getLogger()), daemon=True, name="ReadLogThread")
    readLogThread.start()
    
    consoleLogger.info(f"启动了 {len(workers)} 个 Worker")

    while True:
        a = input("输入 'exit' 退出服务：")

        if a.strip().lower() == "exit":
            break

    stopEvent.set()

    # 等待日志读取线程退出
    logQueue.put(None)
    readLogThread.join()

    # 等待所有Worker退出
    for worker in workers:
        consoleLogger.info(f"等待 {worker.name} 退出...")
        worker.join()
    
    logger.info('', "Stopped")
        
    shutdown() 


    
    

    




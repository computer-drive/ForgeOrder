import time
import os
import threading
from multiprocessing import current_process

from app.init import init, shutdown
from app.const import VERSION
from core.errorHandler.excepthook import installExcepthook
from core.log import getConsoleLogger, getLogContext, getLogger
from app.config import config, CONFIG
from app.bininfo import bininfo, KEYS
from app.wsgi.manager import HTTPWorkerManager
from app.processing.log.read import readLogQueue
from app.ws.startup import startWorker as startWebSocketWorker
# 安装全局异常处理器
installExcepthook() 

current_process().name = "Master"

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


    consoleLogger.info("正在启动应用程序...")

    # 启动HTTP服务
    # workers, logQueue, printerQueue, stopEvent = startWorkers(
    #     host=config.get(CONFIG.SERVER_HOST),
    #     ports=config.get(CONFIG.SERVER_WORKER_PORT),
    #     threads=config.get(CONFIG.SERVER_WORKER_THREADSS),
    #     config=config
    # )

    manager, logQueue, printerQueue = HTTPWorkerManager(
        config.get(CONFIG.SERVER_HOST),
        config.get(CONFIG.SERVER_WORKER_PORT),
        config.get(CONFIG.SERVER_WORKER_THREADSS),
    )()


    consoleLogger.info(f"HTTP服务：启动了 {len(manager._workers)} 个 Worker")
    
    # # 启动WebSocket服务
    # parentPipe, workerProcess = startWebSocketWorker(logQueue, config)
    # consoleLogger.info(f"WebSocket服务：启动了 Websocket Worker")


    # 启动日志读取线程
    readLogThread = threading.Thread(target=readLogQueue, args=(logQueue, getLogger()), daemon=True, name="ReadLogThread")
    readLogThread.start()
    
    
    consoleLogger.info(f"用时 {(time.time() - initTime) * 1000:.2f}  ms")
    consoleLogger.info("按下Ctrl-C退出")

    try:
        while True:
            input()
    except KeyboardInterrupt:
        pass

    manager.stop()


    # 等待所有Worker退出
    try:
        consoleLogger.info("正在等待所有Worker退出，按下Ctrl-C强制退出...")
        for worker in manager._workers:
            consoleLogger.info(f"等待 {worker.name} 退出...")
            worker.join()
    except KeyboardInterrupt:
        manager.forceStop()
        

    # 等待日志读取线程退出
    logQueue.put(None)
    readLogThread.join()
    
    logger.info('', "Stopped")
        
    shutdown() 


    
    

    




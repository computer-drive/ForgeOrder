import time
import os
from multiprocessing import current_process
import multiprocessing

from app.init import init, shutdown
from app.const import VERSION
from core.errorHandler.excepthook import installExcepthook
from core.log import getConsoleLogger, getLogContext, getLogger, getQueue
from app.config import config, CONFIG
from app.bininfo import bininfo
from app.wsgi.manager import HTTPWorkerManager

from app.ws.startup import WebsocketWorker

# 安装全局异常处理器
installExcepthook() 

current_process().name = "Master"

if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")

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

    bininfo.data.isNormalShutdown = False # 先设置为False，等服务正常退出后再设置为True
    bininfo.data.startupCount += 1
    bininfo.data.lastStartTimestamp = int(time.time())
    bininfo.save()


    consoleLogger.info("正在启动应用程序...")


    manager, logQueue, printerQueue = HTTPWorkerManager(
        config.get(CONFIG.SERVER_HOST),
        config.get(CONFIG.SERVER_WORKER_PORT),
        config.get(CONFIG.SERVER_WORKER_THREADSS),
        config.get(CONFIG.LOG_LEVEL),
        getQueue()
    )()


    consoleLogger.info(f"HTTP服务：启动了 {len(manager._workers)} 个 Worker")

    1 + ["123"]
    
    # # 启动WebSocket服务
    websocketWorker = WebsocketWorker("Worker-Websocket", config.get(CONFIG.LOG_LEVEL), logQueue, manager.stopEvent, config, False)
    websocketWorker.start()
    consoleLogger.info(f"WebSocket服务：启动了 Websocket Worker")




    # 等待所有进程启动完毕
    manager.waitProcessToStart()
    websocketWorker.waitToStart()


    consoleLogger.info(f"用时 {(time.time() - initTime) * 1000:.2f}  ms，按下Ctrl-C退出")


    try:
        while True:
            if input() == "exit": print("exit"); break
    except KeyboardInterrupt:
        pass

    manager.stop()
    websocketWorker.stop()


    # 等待所有Worker退出
    try:
        consoleLogger.info("正在等待所有Worker退出，再次按下Ctrl-C强制退出...")
        for worker in manager._workers+ [websocketWorker]:
            worker.join()
            consoleLogger.info(f"{worker.name} 已退出")


    except KeyboardInterrupt:
        manager.forceStop()

        worker._process.terminate() #type: ignore
        

    # 等待日志读取线程退出
    logQueue.put(None)
    

    shutdown() 

    


    
    

    




import time
import os
import multiprocessing
from typing import cast
import asyncio

lazy from app.init import initServer, shutdown, initBasic
from app.cli import parseArguments
lazy from app.cli import runCommand
lazy from app.const import VERSION
lazy from core.errorHandler.excepthook import installExcepthook
lazy from core.log import getConsoleLogger, getLogContext, getLogger, getQueue
lazy from app.config import config, CONFIG
lazy from app.bininfo import bininfo
lazy from app.wsgi.manager import HTTPWorkerManager
lazy from app.plugins.load import getPluginManager
lazy from app.ws.startup import WebsocketWorker
lazy from app.listen import startListen
    

# 安装全局异常处理器
installExcepthook() 

if __name__ == "__main__":
    multiprocessing.current_process().name = "Master"

    multiprocessing.set_start_method("spawn")

    ### 初始化部分

    initBasic()

    initTime = time.time()
    try:
        args, isCli = parseArguments()
    except SystemExit:
        shutdown(0, True)
        exit(0)

    if isCli:
        runCommand(args)
        shutdown(0, True)
        # 退出程序

    initServer()



    consoleLogger= getConsoleLogger("main")


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




    ## 启动worker

    # 运行插件
    getPluginManager().run()

    logQueue = cast(multiprocessing.Queue, getQueue())

    manager, _, printerQueue = HTTPWorkerManager(
        config.get(CONFIG.SERVER_HOST),
        config.get(CONFIG.SERVER_WORKER_PORT),
        config.get(CONFIG.SERVER_WORKER_THREADSS),
        config.get(CONFIG.LOG_LEVEL),
        logQueue
    )()

    
    # # 启动WebSocket服务
    websocketWorker = WebsocketWorker("Worker-Websocket", config.get(CONFIG.LOG_LEVEL), logQueue, manager.stopEvent, config, False)
    websocketWorker.start()

    


    asyncio.run(startListen(manager, websocketWorker))
    
    logger.info({}, "Stopped", "Main")

    # 等待日志读取线程退出
    logQueue.put(None)
    
    getPluginManager().shutdown()

    shutdown() 

    


    
    

    




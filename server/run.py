import time
import os

from app.init import init, shutdown
from app.const import VERSION
from core.errorHandler.excepthook import installExcepthook
from core.log import getConsoleLogger, getLogContext, getLogger
from app.config import config, CONFIG
from app.setup import setupApp
from app.bininfo import bininfo, KEYS

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
    }, "RuntimeInfo")

    

    # 初始化flask
    app = setupApp()
    
    consoleLogger.info("正在启动HTTP服务...")

    host = config.get(CONFIG.SERVER_HOST)
    port = config.get(CONFIG.SERVER_PORT)

    logger.info({
            "host": host,
            "port": port,
        },  "StartServer")

    consoleLogger.info(f"启动成功({int((time.time() - initTime) * 1000)}ms)")

    bininfo[KEYS.IS_NORMAL_SHUTDOWN] = False # 先设置为False，等服务正常退出后再设置为True
    bininfo[KEYS.STARTUP_COUNT] += 1
    bininfo[KEYS.LAST_START_TIMESTAMP] = int(time.time())
    bininfo.save()
       
    if os.environ["ENV"] == "product":

        from waitress import serve

        serve(app, host=host, port=port)

    else:
    
        app.run(
            host=host,
            port=port,
        )


    logger.info('', "ServerStopped")

    shutdown()

    




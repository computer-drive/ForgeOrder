import time
import os

from app.init import init, shutdown
from const import *
from core.error_handler.excepthook import install
from core.log import get_console_logger
import extensions
from app.init_app import setup_app




if __name__ == "__main__":

    console_logger= get_console_logger("main")
    init_time = time.time()

    install()

    init()

    ## 设置环境变量
    os.environ["ENV"] = extensions.config.get("server.env")

    logger = extensions.get_log_context(extensions.logger, "MAIN")
    logger.debug(f"ForgeOrder版本：%s" % VERSION,"DebugMsg")

    

    # 初始化flask
    app = setup_app()
    
    console_logger.info("正在启动HTTP服务...")

    host = extensions.config.get("server.host")
    port = extensions.config.get("server.port")

    
    
    if os.environ["ENV"] == "product":
        logger.debug("生产环境运行。", "DebugMsg")

        from waitress import serve

        logger.info({
            "host": host,
            "port": port,
        },  "StartServer")


        console_logger.info(f"启动成功({int((time.time() - init_time) * 1000)}ms)")


        serve(app, host=host, port=port)


    else:
        logger.debug("开发环境运行。", "DebugMsg")

        console_logger.info(f"启动成功({int((time.time() - init_time) * 1000)}ms)")
        
        app.run(
            host=host,
            port=port,
        )


    logger.info('', "ServerStopped")


    shutdown()








    

    
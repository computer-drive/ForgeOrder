import logging
from pathlib import Path
import sys
from typing import cast

from app.db.repository import RepositoryManager
from app.service import initService
from app.service.settings import SettingsService
from core.database.database import Database

from app.printer.service import PrintManager
from app.config import config, CONFIG
from core.log import getConsoleLogger
from core.log import initLogger, getLogger, shutdownLogger
from app.bininfo import bininfo, KEYS

from app.cli import createParser, executeCommand
from app.exceptions import UserError

consoleLogger= getConsoleLogger("startup")

def initRootUser(reset = False):

    import random
    from app.service import initService, UserService


    password = "".join(random.choices("abcdefghijklmnopqrstuvwxyz1234567890", k=8))


    db, _, service = cast(tuple[Database, None, UserService], initService(config.get(CONFIG.DATABASE_PATH), UserService))
    
    try:
        if reset:
            status, rootUser = service.get(username="root")

            

            if status is service.USER.SUCCESS:
                rootUser = cast(dict, rootUser)
                
                rootUserId = rootUser['id']

                service.forceChangePassword(rootUserId, password)

                consoleLogger.info("重置root用户密码：%s" % password)
                return

            else:
                consoleLogger.warning("root用户不存在，无法重置密码")

        service.create("root", password, True, True)


        consoleLogger.info("创建root用户，密码：%s" % password)

        
        bininfo[KEYS.IS_FIRST_START] = False
        bininfo.save()

    finally:
        db.close()

def initLog():


    initLogger(__name__, config.get(CONFIG.LOG_DATABASE), config.get(CONFIG.LOG_LEVEL))

    getLogger()

def initConfig(configPath: str):
    path = Path(configPath)

    path.parent.mkdir(parents=True, exist_ok=True)

    config.initConfig(configPath)
    
def initArguments():
    parser = createParser()

    args = parser.parse_args()

    if len(sys.argv) > 1:
        consoleLogger.info(f"命令行参数：{' '.join(sys.argv[1:])}")

    return executeCommand(args)

def validateAppSettings():
    # 验证配置项
    try:

        db, _, service = initService(config.get(CONFIG.DATABASE_PATH), SettingsService)

        try:
            service  = cast(SettingsService, service)

            service._init()
        finally:
            db.close()

    except UserError as e:
            consoleLogger.error(f"启动失败：{e} \n {e.hint}")
            sys.exit(1)

def initDatabase():
    # 初始化数据库的表结构
    db = Database(config.get(CONFIG.DATABASE_PATH))
    db.connect()
    
    repos = RepositoryManager(db)
    repos.init()

    # 关闭数据库连接
    db.close()

def init():

    consoleLogger.info("正在初始化...")

    # 加载bininfo
    bininfo.load()

    consoleLogger.debug(f"上次启动是否正常退出：{bininfo[KEYS.IS_NORMAL_SHUTDOWN]}")
    consoleLogger.debug(f"启动次数：{bininfo[KEYS.STARTUP_COUNT]}")


    # 初始化设置
    consoleLogger.info(f"正在加载从 {bininfo[KEYS.CONFIG]} 加载配置...")
    initConfig(bininfo[KEYS.CONFIG])

    # 初始化日志记录器
    initLog()

    # 初始化数据库
    initDatabase()

    # 判断是否为第一次启动，如果是则创建root用户
    if bininfo[KEYS.IS_FIRST_START]:
        initRootUser()

    # 初始化命令行参数
    shouldExit = initArguments()
    if shouldExit:
        shutdown()
        sys.exit(0)

    # 验证应用项
    validateAppSettings()

    # 初始化打印服务
    printManager = PrintManager()


def shutdown(exitCode: int = 0):
    # 关闭数据库日志记录器线程
    shutdownLogger()


    # 关闭打印服务
    PrintManager.getInstance().shutdown()

    # 关闭日志记录器
    logging.shutdown()

    bininfo[KEYS.IS_NORMAL_SHUTDOWN] = True

    # 保存bininfo
    bininfo.save()


    sys.exit(exitCode)

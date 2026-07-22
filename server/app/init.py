import logging
import os
import sys
from venv import logger

from core.utils import get_local_ip
import extensions
from app.models.exceptions import *
from const import *
from core.auth import AuthManager
from app.config import setup_config
from core.log.logger import setup_logger
from core.route_manager import RouteManager
from app.init_app.schema import CLIENT_ERROR
from app.db.main_db import MainDatabase
from core.log import get_console_logger
from app.app_settings.manager import SettingsManager
from app.cli import create_parser, execute_command
from app.config.verify import verify_config
from app.exceptions import UserError

console_logger= get_console_logger("startup")

def init_root_user(reset = False):

    import random
    from werkzeug.security import generate_password_hash
    from app.db.main_db import MainDatabase


    password = "".join(random.choices("abcdefghijklmnopqrstuvwxyz1234567890", k=8))
    password_hash = generate_password_hash(password)

    database = MainDatabase(extensions.config.get("database.path"))

    if reset:
        root_user = database.users.get_from_username("root")
        if root_user:
            root_user_id = root_user['id']

            database.users.change_pasword(root_user_id, password_hash)

            console_logger.info("重置root用户密码：%s" % password)
            return

        else:
            console_logger.warning("root用户不存在，无法重置密码")

    database.users.new_s("root", password_hash, True, True)
    console_logger.info("创建root用户，密码：%s" % password)
    database.close()

    
    
    extensions.config.set("server.first_start", False)

def init_log():
    logger, thread, queue = setup_logger(__name__,
                extensions.config.get("log.database"), # type: ignore
                extensions.config.get("log.level")) #type: ignore

    extensions.logger = logger
    extensions.db_logger_thread = thread
    extensions.db_logger_queue = queue


    # 处理log.ignore_client_error
    if extensions.config.get("log.ignore_client_error"):
        for error in CLIENT_ERROR:
            extensions.logger.setIgnoreAction(error)


def init():

    console_logger.info("正在初始化...")

    # 创建data目录
    if not os.path.exists("data"):
        os.makedirs("data")
    # 加载配置文件
    extensions.config = setup_config()


    
    # 初始化日志记录器
    init_log()


    # 初始化认证管理器
    extensions.auth_manager = AuthManager(
            extensions.config.get("auth.secret_key"),
            int(extensions.config.get("auth.available_time")),
        )

    # 取本地ip
    extensions.local_ip = get_local_ip()


    # 初始化ArgumentsManager
    extensions.route_manager = RouteManager()

    # print(extensions.config.get("server.first_start"))
    if extensions.config.get("server.first_start"):
        init_root_user()

    stop_running = init_args()

    if stop_running:
        shutdown()
        sys.exit(0)

    # 验证配置项
    try:
        verify_config()


        # 验证数据库的settings
        db = MainDatabase(extensions.config.get("database.path"))
        manager = SettingsManager(db)


        manager._init()

    except UserError as e:
            console_logger.error(f"启动失败：{e} \n {e.hint}")
            sys.exit(1)

    
    

def init_args():
    parser = create_parser()

    args = parser.parse_args()

    if len(sys.argv) > 1:
        console_logger.info(f"命令行参数：{' '.join(sys.argv[1:])}")

    return execute_command(args)

    
    

def shutdown():
    # 关闭数据库日志记录器线程
    if extensions.db_logger_thread is None:
        return
    
    extensions.db_logger_queue.join()
    extensions.db_logger_queue.put(None)

    extensions.db_logger_thread.join()

    logging.shutdown()

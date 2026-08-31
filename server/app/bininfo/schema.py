from core.binpack import *

class KEYS:
    IS_FIRST_START = "isFirstStart"
    IS_NORMAL_SHUTDOWN = "isNormalShutdown"
    LAST_START_TIMESTAMP = "lastStartTimestamp"
    STARTUP_COUNT = "StartupCount"
    CONFIG = "config"

SCHEMA = [
    Field(KEYS.IS_FIRST_START, Boolean(), False),     # 是否是第一次启动
    Field(KEYS.IS_NORMAL_SHUTDOWN, Boolean(), False), # 是否正常关闭

    Field(KEYS.LAST_START_TIMESTAMP, Integer(64), 0), # 上次启动时间戳
    Field(KEYS.STARTUP_COUNT, Integer(32), 0),       # 启动次数

    Field(KEYS.CONFIG, String(128), "data/config.json"),            # 配置文件路径
    
]

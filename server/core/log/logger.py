import datetime
import logging
import queue
import json
import multiprocessing

from .schema import *

from .worker import createWorker


class Logger(logging.Logger):
    def __init__(self, name: str, formatJson: bool = True):
        super().__init__(name)

        self.ignoreCategory = []
        self.ignoreActions = []
        self.ignoreDebug = []
        self.formatJson = formatJson

    def setLevel(self, level: int | str) -> None:
        return super().setLevel(level)
    
    def setIgnoreCategory(self, category: str) -> None:
        self.ignoreCategory.append(category)
    
    def setIgnoreAction(self, action: str) -> None:
        self.ignoreActions.append(action)

    def logWithTimestamp(self, msg: str | dict | list, level: int, category: str, action: str, timestamp: float, requestId: str = None, processName: str = ""): # type:ignore
        extra : dict = {"category": category, "action": action, "requestId": requestId}
                
        extra["originMsg"] = msg

        extra["forceTimestamp"] = timestamp

        extra["process_"] = processName if processName != "" else multiprocessing.current_process().name

        if isinstance(msg, (dict, list)):
            if self.formatJson:
                msg = json.dumps(msg, ensure_ascii=False, indent=2)
            else:
                msg = json.dumps(msg, ensure_ascii=False)
        elif msg is None:
            msg = ''
        else:
            msg = str(msg)

    
        if category in self.ignoreCategory or action in self.ignoreActions:
            return
        
        super().log(level, msg, extra=extra)


    def log(self, msg: str | dict | list , level: int, category: str, action: str, requestId: str = None, processName: str = ""): # type:ignore
        extra: dict = {"category": category, "action": action, "requestId": requestId}
        
        extra["originMsg"] = msg

        extra["forceTimestamp"] = None

        extra["process_"] = processName
        
        if isinstance(msg, (dict, list)):
            if self.formatJson:
                msg = json.dumps(msg, ensure_ascii=False, indent=2)
            else:
                msg = str(msg)
        elif msg is None:
            msg = ''
        else:
            msg = str(msg)

    
        if category in self.ignoreCategory or action in self.ignoreActions:
            return
        
        super().log(level, msg, extra=extra)

    def info(self, msg: str | dict | list , category: str, action: str, requestId: str = None, processName: str = ""):  # type:ignore
        self.log(msg, logging.INFO, category, action, requestId, processName)

    def warning(self, msg: str | dict | list , category: str, action: str, requestId: str = None, processName: str = ""):  # type:ignore
        self.log(msg, logging.WARNING, category, action, requestId)

    def error(self, msg: str | dict | list , category: str, action: str, requestId: str = None, processName: str = ""):  # type:ignore
        self.log(msg, logging.ERROR, category, action, requestId, processName)

    def critical(self, msg: str | dict | list , category: str, action: str, requestId: str = None, processName: str = ""):  # type:ignore
        self.log(msg, logging.CRITICAL, category, action, requestId, processName)

    def debug(self, msg: str | dict | list , category: str, action: str, requestId: str = None, processName: str = ""):  # type:ignore
        # print(category, self.debug_ignore)
        if category in self.ignoreDebug:
            return
        else:
            self.log(msg, logging.DEBUG, category, action, requestId, processName)

class DatabaseHandler(logging.Handler):
    def __init__(self, queue: queue.Queue):
        super().__init__()

        self.q = queue

    def emit(self, record: logging.LogRecord):

        if record.forceTimestamp is not None:
            record.created = record.forceTimestamp
        
        time = datetime.datetime.fromtimestamp(record.created)

        # record.process_ = record.process_ if record.process_ != "" else multiprocessing.current_process().name

        level = 0

        match record.levelname:
            case "DEBUG":
                level = logging.DEBUG
            case "INFO":
                level = logging.INFO
            case "WARNING":
                level = logging.WARNING
            case "ERROR":
                level = logging.ERROR
            case "CRITICAL":
                level = logging.CRITICAL
            case _:
                level = logging.INFO

        if not record.originMsg:
            # 原始数据为空
            msg = None
        elif isinstance(record.originMsg, str):
            msg = {"message": record.originMsg}
        else:
            msg = record.originMsg

            
            
        self.q.put((time, level, record.category, record.action, msg, record.requestId, record.process_))
        
        

class Formatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        
        record.color = ""
        record.reset = "\033[0m"

        if record.forceTimestamp is not None:
            record.created = record.forceTimestamp

        record.process_ = record.process_ if record.process_ != "" else multiprocessing.current_process().name
      
        
        match record.levelname:
            case "DEBUG":
                record.levelname = "\033[94mDEBUG\033[0m"
            case "INFO":
                record.levelname = "\033[92mINFO\033[0m"
            case "WARNING":
                record.color = "\033[93m"
            case "ERROR":
                record.color = "\033[91m"
            case "CRITICAL":
                record.color = "\033[95m"

        if record.requestId:
            record.msg = f": [{record.requestId[:8]}...] {record.msg} "
        else:
            record.msg = f": {record.msg}"

        return super().format(record)



def setupLogger(name: str, databaseName: str, level: str = "info", formatJson: bool = True):
    logger = Logger(name, formatJson)

    formatter = Formatter(FORMAT)

    levelInt = logging.INFO
    match level:
        case "debug":
            levelInt = logging.DEBUG
        case "info":
            levelInt = logging.INFO
        case "warning":
            levelInt = logging.WARNING
        case "error":
            levelInt = logging.ERROR
        case "critical":
            levelInt = logging.CRITICAL
        case _:
            levelInt = logging.INFO
    
    logger.setLevel(levelInt)

    # 控制台日志记录器

    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    streamHandler.setLevel(levelInt)
    logger.addHandler(streamHandler)

    # 数据库日志记录器
    
    if databaseName:
        queue, thread = createWorker(databaseName)

        databaseHandler = DatabaseHandler(queue)

        databaseHandler.setLevel(levelInt)
        logger.addHandler(databaseHandler)
    else:
        queue = None
        thread = None
        logger.warning('', "LOGGER", "NotSetupDatabaseHandler")

    return logger, thread, queue



    


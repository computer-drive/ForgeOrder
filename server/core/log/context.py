from .logger import Logger
from .schema import INFO, DEBUG, WARNING, ERROR, NOTICE, LogLevel
from .schema import  Formatter

class LogContext:
    def __init__(self, logger: Logger, category: str) -> None:
        self.logger = logger
        self.category = category

    def log(self, msg: str | Formatter, data: dict, level: LogLevel, action: str, requestId: str | None = None):
        self.logger.log(msg, data, level, self.category, action, requestId)

    def info(self, msg: str | Formatter, data: dict, action: str, requestId: str | None = None):
        self.log(msg, data, INFO, action, requestId)

    def debug(self, msg: str | Formatter, data: dict, action: str, requestId: str  | None = None):
        self.log(msg, data, DEBUG, action, requestId)

    def warning(self, msg: str | Formatter, data: dict, action: str, requestId: str | None = None):
        self.log(msg, data, WARNING,  action, requestId)
    
    def error(self, msg: str | Formatter, data: dict, action: str, requestId: str | None = None):
        self.log(msg, data, ERROR, action, requestId)

    def notice(self, msg: str | Formatter, data: dict, action: str, requestId: str | None = None):
        self.log(msg, data, NOTICE, action, requestId)


class RequestLogContext(LogContext):
    def __init__(self, logger: Logger, category: str, requestId: str):
        super().__init__(logger, category)
        self.requestId = requestId

            
    def setCategory(self, category: str):
        self.category = category


    def log(self, msg: str | Formatter, data: dict, level: LogLevel, action: str, requestId: str | None = None): 
        return super().log(msg, data, level, action, self.requestId) 

    def getLogContext(self, category: str):
        return RequestLogContext(self.logger, category, self.requestId)

def getLogContext(logger: Logger, category: str):
    return LogContext(logger, category)
        
    




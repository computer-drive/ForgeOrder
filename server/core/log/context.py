from .logger import Logger
from .schema import INFO, DEBUG, WARNING, ERROR


class LogContext:
    def __init__(self, logger: Logger, category: str) -> None:
        self.logger = logger
        self.category = category

    def log(self, msg: dict , level: int, action: str, requestId: str | None = None):
        self.logger.log(msg, level, self.category, action, requestId)

    def info(self, msg: dict , action: str, requestId: str | None = None):
        self.log(msg, INFO, action, requestId)

    def debug(self, msg: dict , action: str, requestId: str  | None = None):
        self.log(msg, DEBUG, action, requestId)

    def warning(self, msg: dict , action: str, requestId: str | None = None):
        self.log(msg, WARNING,  action, requestId)
    
    def error(self, msg: dict , action: str, requestId: str | None = None):
        self.log(msg, ERROR, action, requestId)





class RequestLogContext(LogContext):
    def __init__(self, logger: Logger, category: str, requestId: str):
        super().__init__(logger, category)
        self.requestId = requestId

            
    def setCategory(self, category: str):
        self.category = category


    def log(self, msg: dict , level: int, action: str, requestId: str | None = None): 

        return super().log(msg, level, action, self.requestId) 

    def getLogContext(self, category: str):
        return RequestLogContext(self.logger, category, self.requestId)

def getLogContext(logger: Logger, category: str):
    return LogContext(logger, category)
        
    




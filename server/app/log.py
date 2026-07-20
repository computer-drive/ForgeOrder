
from flask import request, g 

from core.log.context import LogContext
from core.log.logger import Logger

class LogContextWithRequestId(LogContext):
    def __init__(self, logger: Logger, category: str = "", request_id: str = None, before_log = None):
        super().__init__(logger, category)

        self.request_id = request_id
        self.before_log = before_log

    def log(self, msg: str | dict | list , level: int, action: str, request_id: str = None):
        self.before_log()

        super().log(msg, level, action, self.request_id)

class RequestLogContext(LogContext):
    def __init__(self, logger: Logger, category: str = ""):
        super().__init__(logger, category)

        if hasattr(g, 'args'):
            args = g.args
        else:
            args = {}
            
        self.request_info = {
            "request_id": g.request_id,
            "ip": request.remote_addr,
            "path": request.path,
            "method": request.method,
            "args": args,
        }

        self.logged_request_info = False

    def set_category(self, category: str):
        self.category = category

    def _before_log(self):
        if not self.logged_request_info:
            self.logger.info(self.request_info, "REQUEST","RequestInfo", g.request_id)
            self.logged_request_info = True

    def log(self, msg: str | dict | list , level: int, action: str, request_id: str = None):
        self._before_log()


        # if isinstance(msg, dict):
        #     msg["request_id"] = g.request_id
            
        # else:
        #     msg = {
        #         "request_id": g.request_id,
        #         "msg": msg
        #     }



        return super().log(msg, level, action, g.request_id)
        
    def get_log_handler(self, category: str):
        return LogContextWithRequestId(self.logger, category, g.request_id, self._before_log)





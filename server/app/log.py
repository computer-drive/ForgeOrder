
from flask import request, g 

from core.log.manager import LogHandler
from core.log.logger import Logger

class LogHandlerWithRequestId(LogHandler):
    def __init__(self, logger: Logger, class_name: str = "", request_id: str = None, before_log = None):
        super().__init__(logger, class_name)

        self.request_id = request_id
        self.before_log = before_log

    def log(self, msg: str | dict | list , level: int, method: str, request_id: str = None):
        self.before_log()

        super().log(msg, level, method, self.request_id)

class RequestLogHandler(LogHandler):
    def __init__(self, logger: Logger, class_name: str = ""):
        super().__init__(logger, class_name)

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

    def set_class_name(self, class_name: str):
        self.class_name = class_name

    def _before_log(self):
        if not self.logged_request_info:
            self.logger.info(self.request_info, "REQUEST","RequestInfo", g.request_id)
            self.logged_request_info = True

    def log(self, msg: str | dict | list , level: int, method: str, request_id: str = None):
        self._before_log()


        # if isinstance(msg, dict):
        #     msg["request_id"] = g.request_id
            
        # else:
        #     msg = {
        #         "request_id": g.request_id,
        #         "msg": msg
        #     }



        return super().log(msg, level, method, g.request_id)
        
    def get_log_handler(self, class_name: str):
        return LogHandlerWithRequestId(self.logger, class_name, g.request_id, self._before_log)





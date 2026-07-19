
from flask import request, g 

from core.log.manager import LogHandler
from core.log.logger import Logger

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
            self.logger.info(self.request_info, self.class_name, "RequestInfo")
            self.logged_request_info = True

    def log(self, msg: str | dict | list , level: int, method: str):
        if isinstance(msg, dict):
            msg["request_id"] = g.request_id
            
        else:
            msg = {
                "request_id": g.request_id,
                "msg": msg
            }
        return super().log(msg, level, method)
        
    





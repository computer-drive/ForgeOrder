from .schema import ArgRule, ARGUMENTS
from .exceptions import *


class RouteManager:
    def __init__(self):

        self.routes = {}

    def register(self, path: str,
                 auth: bool= False,
                 is_admin: bool = False,
                 args: list[ArgRule] | None= None):
        
        if path in self.routes:
            raise RouteAlreadyRegisteredError(path)
        
        args_ = {}

        if args is None:
            args = []
            
        for arg in args:
            args_[arg['name']] = arg

        self.routes[path] = args_

        
        self.routes[path] = {
            "auth": auth,
            "is_admin": is_admin,
            "args": args_
        }

    def has_args(self, path: str):
        if path in self.routes and self.routes[path]["args"]:
            return True
        else:
            return False

    def verify_args(self, path: str, args: dict):
        if path not in self.routes:
            return ARGUMENTS.RESULT.NO_ARGS, {}
        
        args_rule = self.routes[path]["args"]
        
        args_final = {}
    
        error_info = []
        
        for arg_rule in args_rule.values():
            arg_name = arg_rule["name"]

            if arg_name in args:
                # 参数存在
                value = args[arg_name]
            
            elif arg_rule["required"]:
                # 必填参数缺失
                error_info.append({
                    ARGUMENTS.ERROR.NOT_FOUND: arg_name
                })
                continue
            
            else:
                # 参数不存在，使用默认值
                value = arg_rule["default"]

            # 类型检查（不考虑默认值情况，相信调用者会正确传递类型）
            if not isinstance(value, arg_rule["type"]):
                error_info.append({
                    ARGUMENTS.ERROR.TYPING_ERROR: arg_name
                })
                continue

            # 添加到最终的
            args_final[arg_name] = value
            

        if error_info:
            return ARGUMENTS.RESULT.FAIL, error_info
        else:
            return ARGUMENTS.RESULT.PASS, args_final
       

    def verify_auth(self, path: str):
        if path not in self.routes:
            return False, None
        
        else:
            return True, {
                "auth": self.routes[path]["auth"],
                "is_admin": self.routes[path]["is_admin"]
            }
        
        
        
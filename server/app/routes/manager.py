from .schema import RoutesInfo
from .exceptions import *
from .field import RequestField

class RouteManager:
    def __init__(self):

        self.routes: dict[str, RoutesInfo] = {}

    def register(self, path: str,
                 auth: bool= False,
                 is_admin: bool = False,
                 args: list[RequestField] | None = None):

        if args is None:
            args = []

        if path in self.routes:
            raise RouteAlreadyRegisteredError(path)
        
        args_ = {}

        for arg in args:
            args_[arg.key] = arg

        self.routes[path] = {
            "is_admin": is_admin,
            "auth": auth,
            "args": args_
        }

        

    def has_args(self, path: str):
        if path in self.routes and len(self.routes[path]["args"]) > 0:  
            return True
        else:
            return False

    def validate_args(self, path: str, args: dict):
        if path not in self.routes:
            return {}
        
        routes_info = self.routes[path] # 所有args的字段定义

        args_final = {}

        for key, field in routes_info["args"].items():
            if key in args.keys():
                # key本身存在，验证类型
                if not isinstance(args[key], field.value_type):
                    raise InvalidArgumentTypeError(key, field.value_type, type(args[key]))


                # 执行Validator
                if not field.validator:
                    args_final[key] = args[key]
                    continue

                result = field.validator.validate(args[key])

                if result.success:
                    args_final[key] = args[key]
                    continue
                else:
                    raise ArgumentValidationError(key, result.error) #type: ignore
                

                
            elif field.required:
                # key不存在，必填项。
                raise MissingRequiredArgumentError(field.key)
            else:
                # key不存在，非必填项。
                args_final[key] = field.default

        return args_final


    

    def verify_auth(self, path: str):
        if path not in self.routes:
            return False, None
        
        else:
            return True, {
                "auth": self.routes[path]["auth"],
                "is_admin": self.routes[path]["is_admin"]
            }
        
        
        
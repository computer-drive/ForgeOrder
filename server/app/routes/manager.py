from typing import Any

from .schema import Route
from .responseGenerator import ResponseGenerator, ResponseInfo
from .exceptions import *
from .field import BodyField, PathField, RequestParameterField


class RouteManager:
    def __init__(self):

        self.routes: dict[str, dict[str, Any]] = {}

    def register(self, route: Route):

        if route.paramaters is None:
            route.paramaters = []

        if route.endpoint in self.routes:
            raise RouteAlreadyRegisteredError(route.endpoint)
        
        bodyParams_ = {}
        pathParams_ = {}

        for field in route.paramaters:
            if isinstance(field, BodyField):
                bodyParams_[field.key] = field
            elif isinstance(field, PathField):
                pathParams_[field.key] = field
            else:
                raise ValueError(f"Invalid parameter type: {type(field)}")

        self.routes[route.endpoint] = { # type: ignore
            "isAdmin": route.requiresAdmin,
            "requiresAuth": route.requiresAuth,
            "bodyParams": bodyParams_,
            "pathParams": pathParams_,
            "responses": route.responses,
        }


    def hasParameters(self, endpoint: str):
        hasBodyParams = False
        hasPathParams = False

        bodyParams = {}
        pathParams = {}

        if endpoint in self.routes:
            if len(self.routes[endpoint]["bodyParams"]) > 0:
                hasBodyParams = True
                bodyParams = self.routes[endpoint]["bodyParams"]

            if len(self.routes[endpoint]["pathParams"]) > 0:
                hasPathParams = True
                pathParams = self.routes[endpoint]["pathParams"]

        return (hasBodyParams, bodyParams), (hasPathParams, pathParams)


    def validateBodyParameters(self, paramatersInfo: dict[str, BodyField], params: dict):
        errors = {}

        finalParameters = {}

        for key, field in paramatersInfo.items():
            if key in params.keys():
                # key本身存在，验证类型
                if not isinstance(params[key], field.valueType):
                    errors[key] = ParameterTypeError(key, field.valueType, type(params[key]))

                # 执行Validator
                if not field.validator:
                    finalParameters[key] = params[key]
                    continue

                result = field.validator.validate(params[key])

                if result.success:
                    finalParameters[key] = params[key]
                    continue
                else:
                    errors[key] = ParameterValidationError(key, result.error) #type: ignore
            elif field.required:
                # key不存在，必填项。
                errors[key] = MissingRequiredParameterError(field.key)
            else:
                # key不存在，非必填项。
                finalParameters[key] = field.default

        return errors, finalParameters

    def validatePathParameters(self, path: str, paramatersInfo: dict[str, PathField], params: dict):
        errors = {}

        finalParameters = {}

        for key, field in paramatersInfo.items():
            # 判断参数是否存在
            if key in params.keys():
                # 参数存在

                # 验证类型
                if not isinstance(params[key], field.valueType):
                    errors[key] = ParameterTypeError(key, field.valueType, type(params[key]))

                # 执行Validator
                if not field.validator:
                    finalParameters[key] = params[key]
                    continue

                result = field.validator.validate(params[key])

                if result.success:
                    finalParameters[key] = params[key]
                    continue
                else:
                    errors[key] = PathParameterValidationError(path, key, params[key], result.error) #type: ignore
                
            else:
                # 参数不存在
                errors[key] = MissingRequiredParameterError(key)

        return errors, finalParameters



    def getAuthConfig(self, endpoint: str):
        if endpoint not in self.routes:
            return False, None
        
        else:
            return True, {
                "requiresAuth": self.routes[endpoint]["requiresAuth"],
                "isAdmin": self.routes[endpoint]["isAdmin"]
            }
        
        
    def getResponseInfo(self, endpoint: str | None):
        if endpoint is None:
            return []
        
        result = self.routes.get(endpoint, None)

        if result:
            return result["responses"]
        else:
            return []
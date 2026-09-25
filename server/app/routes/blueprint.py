from functools import wraps

from flask import Blueprint, Flask

from .manager import RouteManager
from .schema import ResponseInfo, Route
from .field import RequestParameterField


class AppBlueprint(Blueprint):
    def __init__(self, name: str, import_name: str):
        super().__init__(name, import_name)

        self.routes_: list[Route] = []

        self.endpoints_ = []

    def registerForApp(self, app: Flask, routeManager: RouteManager):
        app.register_blueprint(self)

        for route in self.routes_:
            routeManager.register(route)
        

    def route(self, rule: str,
              paramaters: list[RequestParameterField] | None = None,
              requiresAuth: bool = False,
              requiresAdmin: bool = False,
              responses: list[ResponseInfo] | None = None,
              cached: bool = False,
              **options
              ):
        
        flask_route = super().route(rule, **options)

        def wrapper(f):
            self.routes_.append(Route(
                rule, paramaters, requiresAuth, requiresAdmin, responses, cached, f, f"{self.name}.{f.__name__}",
            ))


            @wraps(f)
            def wrapped_view(**kwargs):
                return f()

            return flask_route(wrapped_view)

        return wrapper
    
    def get(self, rule: str,
            requiresAuth: bool = False,
            requiresAdmin: bool = False,
            paramaters: list[RequestParameterField] | None = None,
            responses: list[ResponseInfo] | None = None,
            **options
            ):
        
        options.setdefault("methods", ["GET"])
        return self.route(rule, paramaters, requiresAuth, requiresAdmin, responses, **options)
    
    def post(self, rule: str,
            requiresAuth: bool = False,
            isAdmin: bool = False,
            arguments: list[RequestParameterField] | None = None,
            responses: list[ResponseInfo] | None = None,
            noRouteInfo: bool = False,
            **options
            ):
        
        options.setdefault("methods", ["POST"])
        return self.route(rule, arguments, requiresAuth, isAdmin, responses, **options)
    
    
        
    

        

        


from flask import Blueprint, Flask

from .manager import RouteManager
from .schema import RequestField

class AppBlueprint(Blueprint):
    def __init__(self, name: str, import_name: str):
        super().__init__(name, import_name)

        self.routes_ = []

    def register_for_app(self, app: Flask, route_manager: RouteManager):
        app.register_blueprint(self)

        for route in self.routes_:
            route_manager.register(route["path"],
                                    route["auth"],
                                    route["is_admin"],
                                    route["arguments"])
        

    def route(self, rule: str,
            arguments: list[RequestField] | None = None,
            auth: bool = False,
            is_admin: bool = False,
            **options
            ):
        
        flask_route = super().route(rule, **options)
        
        def wrapper(f):
            self.routes_.append({
                "path": rule,
                "auth": auth,
                "is_admin": is_admin,
                "arguments": arguments
            })

            return flask_route(f)
        return wrapper
    
    def get(self, rule: str,
            auth: bool = False,
            is_admin: bool = False,
            **options
            ):
        
        options.setdefault("methods", ["GET"])
        return self.route(rule, None, auth, is_admin, **options)
    
    def post(self, rule: str,
            arguments: list[RequestField] | None = None,
            auth: bool = False,
            is_admin: bool = False,
            **options
            ):
        
        options.setdefault("methods", ["POST"])
        return self.route(rule, arguments, auth, is_admin, **options)
    
    
        
    

        

        


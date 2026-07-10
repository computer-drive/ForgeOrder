from flask import Blueprint
from .route_manager import RouteManager
from .route_manager.schema import ArgRule

class AppBlueprint(Blueprint):
    def __init__(self, name: str, import_name: str, route_manager: RouteManager):
        super().__init__(name, import_name)

        self.route_manager = route_manager

    def route(self, rule: str,
            arguments: list[ArgRule] | None = None,
            auth: bool = False,
            is_admin: bool = False,
            **options
            ):
        
        flask_route = super().route(rule, **options)
        
        def wrapper(f):
            self.route_manager.register(rule, auth, is_admin, arguments)
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
            arguments: list[ArgRule] | None = None,
            auth: bool = False,
            is_admin: bool = False,
            **options
            ):
        
        options.setdefault("methods", ["POST"])
        return self.route(rule, arguments, auth, is_admin, **options)
    
    
        
    

        

        




class RouterManagerError(Exception):
    pass

class RouteAlreadyRegisteredError(RouterManagerError):
    def __init__(self, path: str):
        self.path = path

        super().__init__(f"Route '{self.path}' is Already Registered.")





        


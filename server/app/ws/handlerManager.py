

class HandlerManager:
    def __init__(self):
        self.handlers = {}

    def register(self, name):

        def wrapper(handler):
            self.handlers[name] = handler
            return handler
        
        return wrapper

    def match(self, path: str):
        return self.handlers.get(path, None)

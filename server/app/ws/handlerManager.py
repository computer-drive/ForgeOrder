from typing import Any
import json


from core.validation.validators import DictOf, TypeOf, NotEmpty
from .schema import MESSAGEES
lazy from .context import Client

class HandlerManager:
    def __init__(self):
        self.handlers = {}

        self.messageTypeValidator = DictOf(True).\
            Field("name", str, True, NotEmpty()).\
            Field("data", dict, True)
        

    def register(self, name):

        def wrapper(handler):
            self.handlers[name] = handler
            return handler
        
        return wrapper

    def match(self, path: str):
        return self.handlers.get(path, None)

    def extend(self, handlerManager: HandlerManager):
        self.handlers.update(handlerManager.handlers)

    async def handle(self, client: 'Client', message: Any):
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            await client.send(MESSAGEES.MESSAGE_INVALID)
            return
        
        if not self.messageTypeValidator.validate(data):
            await client.send(MESSAGEES.MESSAGE_INVALID)
            return

        handler = self.match(data["name"])
        if handler is None:
            print(self.handlers)
            await client.send(MESSAGEES.NAME_NOT_FOUND)
            return

        await handler(client, data)

{"name": "console", "data": {}}
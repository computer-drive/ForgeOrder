from dataclasses import dataclass, field
from multiprocessing.connection import Connection
from typing import Callable

from websockets.asyncio.server import ServerConnection
from websockets.protocol import State

from ..processing.log import WorkerLogger
from ..config import ConfigManager
from .message import makeMessage
from .handlerManager import HandlerManager


@dataclass
class Client:
    ws: ServerConnection
    address: tuple
    connectedAt: float

    whenClosed: Callable | None = None

    @property
    def isConnected(self) -> bool:
        return self.ws.state == State.OPEN

    async def close(self):
        if self.isConnected:
            await self.ws.close()
            
            if self.whenClosed is not None:
                self.whenClosed(self)

    async def send(self, name: str, data: dict | None= None):
        await self.ws.send(makeMessage(name, data))

            
            
    
@dataclass
class WebsocketServerContext:
    pipe: Connection
    logger: WorkerLogger
    config: ConfigManager

    handlerManager: HandlerManager

    clients: list[Client] = field(default_factory=list)

    

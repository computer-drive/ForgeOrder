from multiprocessing.synchronize import Event as MPEvent
from multiprocessing import Queue
import asyncio

from .server import websocketServer
from core.log import Logger
from ..processing.base import ProcessWorker
from ..config import ConfigManager
from core.log.schema import INFO, WARNING, ERROR, DEBUG

class WebsocketWorker(ProcessWorker):
    def __init__(self,
                name: str,
                logLevel: str,
                logQueue: Queue,
                stopEvent: MPEvent,
                config: ConfigManager,
                daemon: bool = True
                ):
        logLevel_ = 0
        
        match logLevel.lower():
            case "info":
                logLevel_ = INFO
            case "warning":
                logLevel_ = WARNING
            case "error":
                logLevel_ = ERROR
            case "debug":
                logLevel_ = DEBUG
            case _:
                logLevel_ = INFO

        super().__init__(name, logLevel_.value, logQueue, stopEvent, daemon)

        self.config = config

    def run(self):
        try:
            asyncio.run(websocketServer(self.pipe,
                                        self.getLogger(),
                                        self.config))
        except KeyboardInterrupt:
            pass

    def stop(self):
        super().stop()

        self.parentPipe.send("stop")

    def waitToStart(self):
        # 等待接受数据
        try:
            self.parentPipe.recv()
        except EOFError:
            return False
        else:
            return True
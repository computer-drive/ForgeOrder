from multiprocessing import  Pipe, Queue, current_process
from multiprocessing.connection import Connection
from multiprocessing.synchronize import Event as MPEvent
import asyncio

from .server import websocketServer
from ..processing.log import WorkerLogger
from ..processing.base import ProcessWorker
from ..config import ConfigManager


class WebsocketWorker(ProcessWorker):
    def __init__(self,
                name: str,
                logQueue: Queue,
                stopEvent: MPEvent,
                config: ConfigManager,
                daemon: bool = True
                ):

        super().__init__(name, logQueue, stopEvent, daemon)

        self.config = config

    def run(self):
        asyncio.run(websocketServer(self.pipe,
                                    self.getWorkerLogger(),
                                    self.config))

    def waitToStart(self):
        # 等待接受数据
        self.parentPipe.recv()


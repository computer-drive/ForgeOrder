from multiprocessing.synchronize import Event as MPEvent
from multiprocessing import Queue
from threading import Thread

from ..processing.base import ProcessWorker
from ..config import ConfigManager
from .setup import setupApp
from .server import AppServer
lazy from .app import MyFlaskApp
from core.log.schema import INFO, WARNING, ERROR, DEBUG

class HTTPWorker(ProcessWorker):
    def __init__(self, name: str,
                 logLevel: str,
                 logQueue: Queue,
                 stopEvent: MPEvent,
                 config: ConfigManager,
                 printerQueue: Queue,
                 host: str,
                 port: int,
                 threads: int,
                 daemon: bool = False,
                 ):

        logLevelInteger = 0
        match logLevel.lower():
            case "info":
                logLevelInteger = INFO
            case "warning":
                logLevelInteger = WARNING
            case "error":
                logLevelInteger = ERROR
            case _:
                logLevelInteger = INFO
        
        super().__init__(name, logLevelInteger, logQueue,  stopEvent, daemon)

        self.config = config
        self.printerQueue = printerQueue

        self.host = host
        self.port = port
        self.threads = threads

        self._app: MyFlaskApp = None #type: ignore
        self._server: AppServer = None #type: ignore 

    def run(self):
        workerLogger = self.getLogger()

        self._app = setupApp(workerLogger, self.config, self.stopEvent)

        workerLogger.info({
                "host": self.host,
                "port": self.port,
            }, "Worker", "Started")
        
            
        self._server = AppServer(self._app, host=self.host, port=self.port, threads=self.threads)

        # 启动一个线程监听关闭事件
        watcherThread = Thread(target=self._shutdownWatcher, daemon=True)
        watcherThread.start()


        self.pipe.send("started")

        self._server.run()

        watcherThread.join()  # 等待关闭线程结束

        workerLogger.info(None, "Worker", "Stopped")

        self.pipe.send("stop")

    def _shutdownWatcher(self):
        self.stopEvent.wait()

        self._server.trigger.pull_trigger(self._server.gracefulShutdown)  # 触发waitress的关闭事件 #type: ignore


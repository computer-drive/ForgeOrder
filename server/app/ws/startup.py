from multiprocessing import  Pipe, Queue, current_process
from multiprocessing.connection import Connection
import asyncio

from .server import websocketServer
from ..processing.log import WorkerLogger
from ..processing.excepthook import installProcessExcepthook
from ..config import ConfigManager
from ..processing.base import MyProcess

def workerMain(childPipe: Connection, logQueue: Queue, config: ConfigManager):
    logger = WorkerLogger(logQueue)

    installProcessExcepthook(logger)

    current_process().workerLogger = logger

    asyncio.run(websocketServer(childPipe, logger, config))


def startWorker(logQueue: Queue, config: ConfigManager):

    parentPipe, childPipe = Pipe()

    workerProcess = MyProcess(target=workerMain,
                            args=(childPipe, logQueue, config),
                            daemon=True, 
                            name='Worker-Websocket')

    

    workerProcess.start()

    return parentPipe, workerProcess

from multiprocessing import Process, Pipe, Queue
from multiprocessing.connection import Connection
import asyncio

from .server import websocketServer
from ..processing.log import WorkerLogger
from ..processing.excepthook import installProcessExcepthook
from ..config import ConfigManager

def workerMain(childPipe: Connection, logQueue: Queue, config: ConfigManager):
    logger = WorkerLogger(logQueue)

    installProcessExcepthook(logger)

    asyncio.run(websocketServer(childPipe, logger, config))


def startWorker(logQueue: Queue, config: ConfigManager):

    parentPipe, childPipe = Pipe()

    workerProcess = Process(target=workerMain,
                            args=(childPipe, logQueue, config),
                            daemon=True, 
                            name='Worker-Websocket')

    workerProcess.start()

    return parentPipe, workerProcess

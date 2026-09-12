from multiprocessing import Process, Queue
import sys
from typing import  cast
from multiprocessing.synchronize import Event as MPEvent
from multiprocessing import Pipe
from multiprocessing.connection import Connection

from .log.record import WorkerLogger

from .excepthook import  installProcessExcepthook, processExcepthook




class ProcessWorker:
    def __init__(self, name: str, logQueue: Queue, stopEvent: MPEvent, daemon: bool = True):
        self.name = name
        self.daemon = daemon
        self.logQueue = logQueue
        self.stopEvent = stopEvent

        # 子进程创建的变量
        self.workerLogger = None
        self.pipe: Connection = None #type: ignore

        self.parentPipe: Connection = None #type: ignore

        self._process = None


    def getWorkerLogger(self) -> WorkerLogger:
        '''注意，本方法应在子进程执行'''
        if self.workerLogger is  None:
            self.workerLogger = WorkerLogger(self.logQueue)

        return cast(WorkerLogger, self.workerLogger)

    def run(self):
        '''子进程的主函数'''
        raise NotImplementedError

    def _worker(self, pipe: Connection):

        try:
            installProcessExcepthook(self.getWorkerLogger())

            self.pipe = pipe

            self.run()
        except Exception as e:
            processExcepthook(*sys.exc_info(), self.getWorkerLogger())

    def start(self):

        parent, children = Pipe()

        self.parentPipe = parent

        self._process = Process(target=self._worker, name=self.name, args=(children,), daemon=self.daemon)

        self._process.start()


    def stop(self):
        self.stopEvent.set()


    def join(self):
        self._process.join()

    def forceStop(self):
        self._process.terminate()


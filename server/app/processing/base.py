import asyncio
from multiprocessing import Process, Queue
import sys
from typing import  cast, Any
from multiprocessing.synchronize import Event as MPEvent
from multiprocessing import Pipe
from multiprocessing.connection import Connection
from dataclasses import dataclass
import traceback

from core.log import Logger



from .excepthook import  installProcessExcepthook, processExcepthook

@dataclass
class PipeInfo:
    type: str
    data: Any

        
    
class WorkerPipe:
    def __init__(self, pipe: Connection):
        self.pipe = pipe

        self.pipe.readable

    def send(self, type: str, data: Any = None):
        self.pipe.send(PipeInfo(type, data))

    def poll(self):
        return self.pipe.poll()

    def recv(self) -> PipeInfo:
        return self.pipe.recv()

    async def recvAsync(self):
        loop = asyncio.get_running_loop()

        if sys.platform == "win32":
            # run_in_executor 轮询
            while True:
                hasData = await loop.run_in_executor(None, self.pipe.poll, 0.5)

                if not hasData:
                    continue

                return self.recv()

        else:
            # 用 add_reader 监听

            fd = self.pipe.fileno() # 获取文件描述符
            dataReady = asyncio.Event() # 数据就绪事件

            loop.add_reader(fd, dataReady.set)

            try:
                while True:
                    if not self.pipe.poll():
                        await dataReady.wait()
                        dataReady.clear()
                        continue

                    return self.recv()
            finally:
                loop.remove_reader(fd)


    

    @classmethod
    def make(cls,parent: Connection, child: Connection):
        return cls(parent), cls(child) 


class ProcessWorker:
    def __init__(self,
                name: str,
                logLevel: int,
                logQueue: Queue,
                stopEvent: MPEvent,
                daemon: bool = True):
        self.name = name
        self.daemon = daemon
        self.logLevel = logLevel

        # 父子共有的
        self.logQueue = logQueue
        self.stopEvent = stopEvent

        # 子进程创建的变量
        self.workerLogger = None
        self.pipe: WorkerPipe = None #type: ignore

        # 这是给父进程用的
        self.parentPipe: WorkerPipe = None #type: ignore


        self._process = None


    def getLogger(self) -> Logger:
        '''注意，本方法应在子进程执行'''
        if self.workerLogger is  None:
            self.workerLogger = Logger(self.logLevel,self.logQueue)

        return cast(Logger, self.workerLogger)

    def run(self):
        '''子进程的主函数'''
        raise NotImplementedError

    def _worker(self, pipe: WorkerPipe):

        try:
            installProcessExcepthook(self.getLogger(), pipe)

            self.pipe = pipe

            self.run()
        except Exception as e:
            processExcepthook(*sys.exc_info(), self.getLogger(), pipe)

    def start(self):

        parent, children = WorkerPipe.make(*Pipe())

        self.parentPipe = parent


        self._process = Process(target=self._worker, name=self.name, args=(children,), daemon=self.daemon)

        self._process.start()


    def stop(self):
        self.stopEvent.set()


    def join(self):
        if self._process is None:
            raise ValueError(f"{self.name} not started")
        self._process.join()

    def terminate(self):
        if self._process is None:
            raise ValueError(f"{self.name} not started")
        
        self._process.terminate()


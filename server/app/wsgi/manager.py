from multiprocessing import Queue, Event

from .worker import HTTPWorker
from ..config import config

class HTTPWorkerManager:

    def __init__(self, host: str, ports: list[int], threads:int, daemon: bool = False):
        self.logQueue = Queue()
        self.printerQueue = Queue()

        self.stopEvent = Event()

        self._workers: list[HTTPWorker] = []

        i = 0
        for port in ports:
            self._workers.append(HTTPWorker(f"Worker-{i}",
                        self.logQueue,
                        self.stopEvent,
                        config,
                        self.printerQueue,
                        host,
                        port,
                        threads,
                        daemon
                        ))

            i += 1

    def __call__(self):

        self.start()
        return self, self.logQueue, self.printerQueue



    def start(self):
        for worker in self._workers:
            worker.start()


    def stop(self):
        self.stopEvent.set()

    def forceStop(self):
        for worker in self._workers:
            worker.terminate()

    def waitProcessToStart(self):

        for worker in self._workers:
            # 等待worker发送一条消
            data = worker.parentPipe.recv()


            


    
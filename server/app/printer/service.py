from queue import Queue
from threading import Thread

from ..service.printTask import PrintTaskService

from .receipt import Receipt
from .worker import createPrintWorker
from core.log import getLogger




class PrintManager:

    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self):

        if hasattr(self, '_initialized'):
            return
        
        self.queue: Queue
        self.workerThread : Thread

        self._init()

    def _init(self):

        logger = getLogger()

        self.queue, self.workerThread = createPrintWorker(logger)

    def new(self, content: Receipt, service: PrintTaskService, context: dict = {}, ):

            
        result = service.create(content, context)

        taskId = result.data

        if taskId is not None:
            self.queue.put(taskId)


        getLogger().info({
            "id": taskId,
        }, "PRINTER", "PrintTaskCreated")

        return taskId


    def shutdown(self):
        self.queue.put(None)

        self.workerThread.join()

    @classmethod
    def isAvailable(cls):
        return cls._instance is not None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            raise ValueError("PrintManager not initialized")
        
        return cls._instance





    



from typing import TYPE_CHECKING
from multiprocessing import Process, Queue
from threading import Thread

from .wsgi import AppServer
from .log.record import WorkerLogger
from ..utils import g
from .excepthook import installProcessExcepthook
lazy from ..setup import setupApp
from ..config import ConfigManager

if TYPE_CHECKING:
    from multiprocessing.synchronize import Event
else:
    from multiprocessing import Event

# 监听关闭事件的一个线程
def _shutdownWatcher(server: AppServer, stopEvent: Event):
    stopEvent.wait()  # 等待关闭事件

    server.trigger.pull_trigger(server.gracefulShutdown)  # 触发waitress的关闭事件 #type: ignore


# 注意这是进程worker，不是线程worker
def _worker(host: str, # 监听的host
            port: int, # 监听的port
            threads: int, # 每个worker的线程数
            logQueue: Queue, # 日志队列
            printerQueue: Queue, # 打印队列
            stopEvent: Event,
            config: ConfigManager,
            ):

    # 初始化日志记录器
    workerLogger = WorkerLogger(logQueue)

    # 安装进程异常处理器
    installProcessExcepthook(workerLogger)

    # 初始化flask app
    app = setupApp()

    app.workerLogger = workerLogger
    app.configManager = config
    app.stopEvent = stopEvent

    workerLogger.info({
        "host": host,
        "port": port,
    }, "Worker", "Started")

    
    server = AppServer(app, host=host, port=port, threads=threads)

    # 启动一个线程监听关闭事件
    watcherThread = Thread(target=_shutdownWatcher, args=(server, stopEvent), daemon=True)
    watcherThread.start()

    server.run()

    watcherThread.join()  # 等待关闭线程结束

    workerLogger.info("", "Worker", "Stopped")


def startWorkers(host: str, ports: list[int], threads: int, config: ConfigManager, ):
    workers : list[Process]= []

    logQueue = Queue()  # 日志队列
    printerQueue = Queue()  # 打印队列

    stopEvent = Event()  # 关闭事件 #type: ignore

    i = 0
    for port in ports:
        workerProcess = (
            Process(target=_worker, args=(host, port, threads, logQueue, printerQueue, stopEvent, config), daemon=True, name=f"Worker-{i}")
        )

        workerProcess.start()

        workers.append(workerProcess)

        i += 1

    return workers, logQueue, printerQueue, stopEvent


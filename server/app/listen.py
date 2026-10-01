import asyncio

from aioconsole import ainput, aprint

from .processing.base import WorkerPipe, ProcessWorker
from .wsgi.manager import HTTPWorkerManager
from .ws.startup import WebsocketWorker
from core.log import getLogger

async def listenWorker(worker: ProcessWorker, availableProcesses: dict[str, bool]):
    logger = getLogger()

    while True:
        try:
            data = await worker.parentPipe.recvAsync()
        except EOFError:
            break

        if data.type == "uncaughtException":
            # 退出进程
            logger.error(
                "{name} 进程异常退出",
                {
                    "name": worker.name,
                }, "WorkerListener", "AbnormalExit"
            )

            worker.stop()
            availableProcesses[worker.name] = False
            break

        elif data.type == "start":
            logger.debug(
                "{name} 进程已启动",
                {
                    "name": worker.name,
                }, "WorkerListener", "Started"
            )

        elif data.type == "stop":
            logger.debug(
                "{name} 进程已退出",
                {
                    "name": worker.name,
                }, "WorkerListener", "Stopped"
            )
            availableProcesses[worker.name] = False

            break

async def startListen(manager: HTTPWorkerManager, ws: WebsocketWorker):

    workers = manager._workers + [ws]

    availableProcesses: dict[str, bool] = {
        worker.name: False for worker in workers
    }

    async def commandInput():
        while True:
            command = await ainput()
            if command == "exit":
                manager.stop()
                ws.stop()
                break
            else:
                await aprint("Unknown command")

    async def listener():
        pass


    await asyncio.gather(*[listenWorker(worker, availableProcesses) for worker in workers], commandInput())

    

    


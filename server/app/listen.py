import asyncio

from aioconsole import ainput, aprint

from .processing.base import WorkerPipe, ProcessWorker
from .wsgi.manager import HTTPWorkerManager
from .ws.startup import WebsocketWorker
from core.log import getLogger

async def listenWorker(worker: ProcessWorker):
    logger = getLogger()

    while True:
        try:
            data = await worker.parentPipe.recvAsync()
        except EOFError:
            break

        if data.type == "uncaughtException":
            # 退出进程
            logger.error({
                "name": worker.name,
            }, "WorkerListener", "AbnormalExit",)

            worker.stop()
            break

        elif data.type == "start":
            logger.debug({
                "name": worker.name,
            }, "WorkerListener", "Started")

        elif data.type == "stop":
            logger.debug({
                "name": worker.name,
            }, "WorkerListener", "Stopped")

            break

async def startListen(manager: HTTPWorkerManager, ws: WebsocketWorker):

    workers = manager._workers + [ws]

    async def commandInput():
        while True:
            command = await ainput()
            if command == "exit":
                manager.stop()
                ws.stop()
                break
            else:
                await aprint("Unknown command")

    await asyncio.gather(*[listenWorker(worker) for worker in workers], commandInput())

    

    


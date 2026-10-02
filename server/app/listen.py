import asyncio
from enum import Enum, auto
import time

from aioconsole import ainput, aprint

from .processing.base import WorkerPipe, ProcessWorker
from .wsgi.manager import HTTPWorkerManager
from .ws.startup import WebsocketWorker
from core.log import getLogger

class STATE(Enum):
    STARTING = auto()
    STARTED = auto()

    STOPPED = auto()

async def listenWorker(worker: ProcessWorker, processState: dict[str, STATE], stateChanged: asyncio.Event):
    logger = getLogger()

    try:
        while True:
            try:
                data = await worker.parentPipe.recvAsync()
            except (EOFError, BrokenPipeError, ConnectionResetError,
                    OSError, asyncio.IncompleteReadError):
                logger.notice("{name} 进程的管道被关闭", {
                    "name": worker.name,
                }, "WorkerListener", "PipeClosed")
                break
            

            # print(f"received! {data.type}: {data.data}")

            if data.type == "uncaughtException":
                # 退出进程
                logger.error(
                    "{name} 进程异常退出",
                    {
                        "name": worker.name,
                    }, "WorkerListener", "AbnormalExit"
                )
                break

            elif data.type == "start":
                logger.debug(
                    "{name} 进程已启动",
                    {
                        "name": worker.name,
                    }, "WorkerListener", "Started"
                )
                processState[worker.name] = STATE.STARTED
                stateChanged.set()

            elif data.type == "stop":
                logger.debug(
                    "{name} 进程已退出",
                    {
                        "name": worker.name,
                    }, "WorkerListener", "Stopped"
                )
                break
    finally:
        processState[worker.name] = STATE.STOPPED
        stateChanged.set()

async def listenState(processState: dict, stateChanged: asyncio.Event, startTime: float):
    logger = getLogger()

    isAllStarted = False

    while True:
        await stateChanged.wait()

        stateChanged.clear()

        # print("Changed!", processState)

        if len(processState) == 0:
            continue

        if all(state == STATE.STARTED for state in processState.values()):
            if not isAllStarted:
                logger.info("启动成功（{time}秒，{workers}个进程）", {
                    "time": round(time.time() - startTime, 2),
                    "workers": len(processState),
                }, "WorkerListener", "AllStarted"
                )
                isAllStarted = True

        if all(state == STATE.STOPPED for state in processState.values()):
            logger.notice("所有进程已退出，正在关闭程序", {}, "WorkerListener", "AllStopped")
            return 
        

async def startListen(manager: HTTPWorkerManager, ws: WebsocketWorker, startTime: float):

    workers = manager._workers + [ws]

    processState: dict[str, STATE] = {
        worker.name: STATE.STARTING for worker in workers
    }

    stateChanged = asyncio.Event()

    async def commandInput():
        while True:
            command = await ainput()
            if command == "exit":
                manager.stop()
                ws.stop()
                break
            else:
                await aprint("Unknown command")

    stateTask = asyncio.create_task(listenState(processState, stateChanged, startTime))

    otherTasks: list = [
        asyncio.create_task(listenWorker(worker, processState, stateChanged))
        for worker in workers
    ]

    otherTasks.append(asyncio.create_task(commandInput()))

    try:
        await stateTask
    finally:
        for t in otherTasks:
            t.cancel()

        await asyncio.gather(*otherTasks, return_exceptions=True)



    

    


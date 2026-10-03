import psutil
import os
from dataclasses import dataclass, field
import time
from threading import Event, Thread
import gc

from core.log import getLogger, Logger

@dataclass
class MemoryInfo:
    total: int
    children: dict[int, int] = field(default_factory=dict)


def getTotalMemoryUsage(logger: Logger):
    currentProcess = psutil.Process(os.getpid())

    memory = MemoryInfo(currentProcess.memory_info().rss)

    # 获取子进程并叠加
    children = currentProcess.children(recursive=True)
    for child in children:
        try:
            memory.children[child.pid] = child.memory_info().rss
            memory.total += child.memory_info().rss

        except (psutil.NoSuchProcess):
            logger.debug("无法获取进程{pid}：进程不存在", {
                "pid": child.pid
            }, "Monitor", "GetMemoryUsage.Error")

        except (psutil.AccessDenied):

            logger.debug("无法获取进程{pid}：访问被拒绝", {
                "pid": child.pid
            }, "Monitor", "GetMemoryUsage.Error")

    return memory

def monitor(logger: Logger, maxMemory: int, stopEvent: Event):
    while True:
        startTime = time.time()

        memory = getTotalMemoryUsage(logger)


        
        
        if memory.total > maxMemory:
            logger.warning("内存使用超过最大限制：{current} / {maxMemory}MB", {
                "current": memory.total / 1024 / 1024,
                "maxMemory": maxMemory / 1024 / 1024
            }, "Monitor", "MemoryUsage.Warning")
        else:
            logger.debug("当前内存使用：{total} / {maxMemory}MB", {
                    "total": memory.total / 1024 / 1024,
                    "maxMemory": maxMemory / 1024 / 1024 
                }, "Monitor", "MemoryUsage")



        # 等待1秒
        if time.time() - startTime < 1:
            stopEvent.wait(1)

        if stopEvent.is_set():
            break

def startMonitor(maxMemory: int):
    stopEvent = Event()

    logger = getLogger()

    monitorThread = Thread(target=monitor, args=(logger, maxMemory, stopEvent))
    monitorThread.start()

    return stopEvent

            


        


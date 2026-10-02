import threading
from queue import Queue, Empty
from typing import cast
import traceback
import datetime

from escpos.printer import Usb, Network, Win32Raw
from escpos.escpos import Escpos


from app.db.repository import RepositoryManager
from app.service import SettingsService
from core.log.context import getLogContext
from core.log.logger import Logger
from app.db.connections import getDatabase_
from app.service import initService
from app.service.printTask import PrintTaskService
from app.service.settings import SettingsService
from .renderer import Renderer


def connectPrinter(connectInfo: dict) -> Escpos: #type: ignore
    if connectInfo["type"] == "Network":
        return Network(connectInfo["ip"], connectInfo["port"], connectInfo["timeout"], profile=connectInfo["profile"], encoding=connectInfo["encoding"])
    elif connectInfo["type"] == "Usb":
        return Usb(connectInfo["vid"], connectInfo["pid"], encoding=connectInfo["encoding"], profile=connectInfo["profile"])
    elif connectInfo["type"] == "Win32Raw":
        return Win32Raw(connectInfo["name"], profile=connectInfo["profile"], encoding=connectInfo["encoding"])


def printTask(commands: list, printer: Escpos, qrInfo: dict, dots: int):
    renderer = Renderer(printer, qrInfo)

    renderer.render(commands, dots)

    printer.cut()


def printWorker(q: Queue, logger: Logger):

    logContext = getLogContext(logger, "PrinterWorker")

    database = getDatabase_()
    repos = RepositoryManager(database)

    settingsService = SettingsService(repos)
    printTaskService = PrintTaskService(repos)


    # 初始化连接信息
    connectInfo = {}

    connectInfo["type"] = settingsService.get("printer.connection.type")
    if connectInfo["type"] == "Network":
        connectInfo["ip"] = settingsService.get("printer.connection.network.ip")
        connectInfo["port"] = settingsService.get("printer.connection.network.port")
        connectInfo["timeout"] = settingsService.get("printer.connection.network.timeout")
    elif connectInfo["type"] == "Usb":

        connectInfo["vid"] = settingsService.get("printer.connection.usb.vid")
        connectInfo["pid"] = settingsService.get("printer.connection.usb.pid")

    elif connectInfo["type"] == "Win32Raw":
        connectInfo["name"] = settingsService.get("printer.connection.win32.name")

    connectInfo["encoding"] = settingsService.get("printer.encoding")
    connectInfo["profile"] = settingsService.get("printer.profile")


    qrInfo = {}
    qrInfo["model"] = settingsService.get("printer.QRCode.model")
    qrInfo["native"] = settingsService.get("printer.QRCode.native")
    qrInfo["correction"] = settingsService.get("printer.QRCode.correction")

    dots = settingsService.get("printer.dotsPerLine")

    printer: Escpos | None = None
    retryConnectCount = 0

    logContext.info("启动成功", {
        "connectInfo": connectInfo,
        "qrInfo": qrInfo,
    }, "WorkerStarted")

    while True:
        # 从队列中获取任务
        try:
            entry = q.get(timeout=5)
        except Empty:
            # 五秒内没有其他任务

            if printer is not None:
                logContext.debug({"message":
                               "Printer connection closed because no print task was received within 5s."}, "ClosePrinterConnection")
                printer.close()
                printer = None

            continue

        if entry is None:
            break

        startTime = datetime.datetime.now()

        


        # 连接打印机
        if printer is None:
            try:
                printer = connectPrinter(connectInfo)

                logContext.debug({
                    "message": "Connected printer"
                }, "ConnectPrinter")
            except Exception as e:

                # 重试次数加1
                retryConnectCount += 1

                # 记录本次的连接错误信息
                logContext.warning({
                    "id": entry,
                    "error": {
                        "name": e.__class__.__name__,
                        "msg": str(e),
                        "traceback": traceback.format_exception(e)
                    }
                }, "ConnectError")

                now = datetime.datetime.now()
                printTaskService.update(entry, 3, "PrinterConnectError")

                # 重试次数超过5词，跳出本次循环
                if retryConnectCount >= 5:
                    logContext.error("", "RetryConnectExhausted")
                    break

    
                # 重试连接打印机
                continue

            retryConnectCount = 0

        # 读取设置

        status, printInfo = printTaskService.get(entry)

        if status == printTaskService.GET.TASK_NOT_FOUND:
        
            logContext.warning({
                "id": entry,
            }, "NotFoundTask")

        
            continue

        printInfo = cast(dict, printInfo)

        # 打印任务
        try:
            printTask(printInfo["commands"], printer, qrInfo, dots)
        except Exception as e:
            logContext.warning({
                "id": entry,
                "error": {
                    "name": e.__class__.__name__,
                    "msg": str(e),
                    "traceback": traceback.format_exception(e)
                }
            }, "PrintTaskError")

            now = datetime.datetime.now()

            printTaskService.update(entry, 3, "PrintTaskError")

            printer.close()
            printer = None

            continue

        printTaskService.update(entry, 2, None)


        # logContext.info({
        #     "id": entry,
        # }, "PrintTaskFinished")

    database.close()      

    # logContext.info("", "WorkerStopped")

    


def createPrintWorker(logger: Logger):
    q = Queue()

    thread = threading.Thread(target=printWorker, args=( q, logger), name="PrintWorker")
    thread.daemon = True
    thread.start()

    return q, thread

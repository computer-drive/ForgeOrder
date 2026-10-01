import threading
import os
from multiprocessing import Queue

from peewee import SqliteDatabase, IntegrityError, OperationalError

from .service import LogService
from ..schema import LogRecord, BUFFER_SIZE, NOTICE
from ...errors.exceptions import CrashException


def printConsole(record: LogRecord):
    time = record.time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    message = record.format()
    if message != '':
        message = ': ' + message

    return f'[{time}/{record.process}] \033[{record.level.color}m{record.level.name}m\033[0m] {record.category}.{record.action}{message}'

def worker(q: Queue, databaseName: str):
    # 初始化基本变量
    buffer = 0

    database = SqliteDatabase(databaseName)
    service = LogService(database)

    # 手动开启事务
    database.begin()

    while True:
        try:
            # 获取日志消息
            record: LogRecord = q.get()

            # 判断是否为终止信号
            if record is None:
                database.commit()
                break

            # 处理日志消息
            print(printConsole(record))

            if record.level != NOTICE:
                service.insertLog(record)

            buffer += 1
            if buffer >= BUFFER_SIZE:
                database.commit()

                buffer = 0

                database.begin()

        except OperationalError as e:
            raise CrashException(f"无法将日志写入数据库，可能有其他实例正在运行。错误信息：{e}")

    database.close()


def createWorker(databaseName: str, queue: Queue):
    thread = threading.Thread(target=worker, args=(queue, databaseName), daemon=False)
    thread.start()

    return thread



            



        

    
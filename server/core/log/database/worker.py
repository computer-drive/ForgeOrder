import threading
import os
import sys
import traceback
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

    return f'[{time}/{record.process}] \033[{record.level.color}m{record.level.name}\033[0m {record.category}.{record.action}{message}'

def worker(q: Queue, databaseName: str):
    # 初始化基本变量
    buffer = 0

    database = SqliteDatabase(databaseName)
    service = LogService(database)

    # 先开启事务
    txn = database.atomic()
    txn.__enter__()

    while True:
        try:
            # 获取日志消息
            record: LogRecord = q.get()

            # 判断是否为终止信号
            if record is None:
                txn.__exit__(None, None, None)
                break

            # 处理日志消息
            print(printConsole(record))

            if record.level != NOTICE:
                service.insertLog(record)

            buffer += 1
            if buffer >= BUFFER_SIZE:
                txn.__exit__(None, None, None)

                buffer = 0

                database.__enter__()

        except OperationalError as e:
            raise CrashException(f"无法将日志写入数据库，可能有其他实例正在运行。错误信息：{e}")

        except Exception as e:
            print(f"输出日志时出错：{e}")
            traceback.print_exception(*sys.exc_info())
            txn.__exit__(*sys.exc_info())

            buffer = 0

            txn.__enter__()


    database.close()


def createWorker(databaseName: str, queue: Queue):
    thread = threading.Thread(target=worker, args=(queue, databaseName), daemon=True)
    thread.start()

    return thread



            



        

    
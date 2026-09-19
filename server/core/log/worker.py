
import threading
from multiprocessing import Queue

from .schema import BUFFER_SIZE
from .service import initService
from ..database.database.exceptions import DatabaseError
from ..database.repository.exceptions import RepositoryError
from .console import getConsoleLogger
from .schema import LogRecord
from . import schema

from .formatter import Formatter


def writeTextLog(record: LogRecord):
    with open("log.txt", "a") as f:
        f.write(formatConsole(record)[0])

def formatJSONMessage(message: dict | None) -> dict | None:
    jsonifyMessage = {}

    if message is None:
        return None

    for key, value in message.items():
        if isinstance(value, Formatter):
            jsonifyMessage[key] = value.formatJSON()
        else:
            jsonifyMessage[key] = value

    
    return jsonifyMessage

def formatConsoleMessage(message: dict) -> dict[str, str]:
    newMessage = {}

    for key, value in message.items():
        if isinstance(value, Formatter):
            newMessage[key] = value.format()
        else:
            newMessage[key] = str(value)

    return newMessage

def formatConsole(record: LogRecord):
    levelname = ""
    match record.level:
        case schema.INFO:
            levelname = "\033[92mINFO\033[0m"
        case schema.WARNING:
            levelname = "\033[93mWARNING\033[0m"
        case schema.ERROR:
            levelname = "\033[91mERROR\033[0m"
        case schema.DEBUG:
            levelname = "\033[94mDEBUG\033[0m"
        case _:
            levelname = "unknown"


    text = f"[{record.time.strftime('%Y-%m-%d %H:%M:%S.%f')}/{record.process}] " 

    indent = len(text)

    text += f"{levelname} {record.category}.{record.action}"

    if record.message is not None :
        if not isinstance(record.message, dict):
            print(f"WARNING: {record}")

        if len(record.message) == 0:
            return text
        else:
            text += "\n"

        # 取key的最大值对齐
        maxKeyLength = max(len(key) for key in record.message.keys())

        textList = []

        for key, value in formatConsoleMessage(record.message).items():
            formatResult = value.replace("\n", f"\n{indent * ' '}")

            textList.append(f"{indent * ' '}{key.ljust(maxKeyLength)}: {formatResult}")


        text += "\n".join(textList)

    return text



def worker(q: Queue, databaseName: str):
    bufferCount = 0

    # 连接数据库
    database, service = initService(databaseName)
    logger = getConsoleLogger(__name__)

    while True:
        try:
            # 获取日志消息
            record: LogRecord = q.get()

            if record is None:
                break

            print(formatConsole(record))

            service.insertLog(record, formatJSONMessage(record.message))

            bufferCount += 1
            if bufferCount >= BUFFER_SIZE:
                service.commit()
                bufferCount = 0


        except (DatabaseError, RepositoryError) as e:
            logger.warning(f"数据库错误：{e}")
            try:
                writeTextLog(record) #type: ignore
            except NameError:
                pass
            
        except (KeyboardInterrupt, EOFError):
            break

        except Exception as e:
            try:
                print(record)
            except:
                pass
            logger.error(f"日志写入错误：{e}")

    service.commit()

    database.close()

def createWorker(databaseName: str, queue: Queue):

    thread = threading.Thread(target=worker, args=(queue, databaseName), name="LogWorker")
    thread.start()

    return thread


        
        
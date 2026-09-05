from typing import TypedDict
import datetime
from multiprocessing import current_process

from ..database.database import Database
from ..database.repository import Repository, Column
from ..database.repository.schema import Integer, String, JSON, DateTime
from ..database.service import ServiceBase
class _Row(TypedDict):
    id: int
    time: datetime.datetime
    level: int
    category: str
    action: str
    message: dict
    requestId: str | None

class LogRepository(Repository[_Row]):
    columns = [
        Column("id", Integer(), primaryKey=True, autoIncrement=True),
        Column("time", DateTime(), notNull=True),
        Column("process", String(), notNull=True),
        Column("level", Integer(), notNull=True),
        Column("category", String(), notNull=True),
        Column("action", String(), notNull=True),
        Column("message", JSON()),
        Column("requestId", String(36)),
        
    ]

    def __init__(self, db: Database, tableName: str):
        super().__init__(db)

        self.tableName = tableName


class LogService:

    def __init__(self, db: Database):
        self.db = db

        self.repo: LogRepository = None # type: ignore

        self._initRepository()

    def _initRepository(self):
        # !: 表名总由日期构成无需注意SQL注入问题
        now = datetime.datetime.now().strftime("%Y%m%d")

        if self.repo is None or self.repo.tableName != f"log_{now}":
            # 若仓库对象不存在，或与当前时间不同，则创建新的仓库对象
            self.repo = LogRepository(self.db, f"log_{now}")

            # 初始化新仓库对象的表结构
            self.repo._init()
        

    def insertLog(self, 
                time: datetime.datetime,
                level: int,
                category: str,
                action: str,
                message: dict,
                requestId: str | None = None,
                process: str  = "",
                ):

        self._initRepository()

        processName = process if process != ""  else current_process().name

        print(current_process().name)

        self.repo.insert(
            time=time,
            level=level,
            category=category,
            action=action,
            message=message,
            requestId=requestId,
            process=processName,
        )

    def commit(self):
        self.repo.commit()

def initService(logDatabaseName: str):

    database = Database(logDatabaseName)

    database.connect()

    return database, LogService(database)





    

    




        
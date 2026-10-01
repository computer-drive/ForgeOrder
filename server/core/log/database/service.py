from typing import cast

from peewee import Database, IntegrityError

from ..schema import LogRecord
from .model import Logs, LogIndex, BaseModel

class LogService:
    def __init__(self, database: Database):
        self.database = database

        self.currentLogTable: tuple[str, type[Logs]] | None = None

        # 连接数据库
        self.database.connect()

        # 绑定model
        self.database.bind(BaseModel)

        # 创建LogIndex表
        self.database.create_tables([LogIndex])

    @staticmethod
    def getLogTable(date: str) -> type[Logs]:
        tableName = f'logs_{date}'

        Meta = type('Meta', (), {'table_name': tableName})

        return type(f'Logs_{date}', (Logs, ), {'Meta': Meta})


    def insertLog(self, logRecord: LogRecord):
        
        currentDate = logRecord.time.strftime("%Y%m%d")

        # 获取相应的日志表模型
        if self.currentLogTable is None or self.currentLogTable[0] != currentDate:
            self.currentLogTable = (currentDate, self.getLogTable(currentDate))

        # 创建表
        self.database.create_tables([self.currentLogTable[1]], safe=True)
        
        
        currentTime = int(logRecord.time.timestamp() * 1000) * 1000 

        for _ in range(10000):
            try:
                logs = self.currentLogTable[1].create(
                    time = currentTime,
                    process=logRecord.process,
                    level=logRecord.level,
                    category=logRecord.category,
                    action=logRecord.action,
                    data=logRecord.data,
                    message=logRecord.message,
                    requestId=logRecord.requestId
                )
            except IntegrityError:
                currentTime += 1
                continue

            # 写入logIndex
            index, created = LogIndex.get_or_create(
                date=currentDate,
                defaults={
                    'date': currentDate,
                    'name': f'logs_{currentDate}',
                    'first': logs,
                    'last': logs,
                    'count': 1,
                }
            )

        
            if not created:
                index = cast(LogIndex, index)

                index.last = logs
                index.count += 1
                index.save()

            return True


        return False


        
        

            
        
        
        
    
        
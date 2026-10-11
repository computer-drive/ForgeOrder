from dataclasses import dataclass

from peewee import MySQLDatabase
from playhouse.pool import PooledMySQLDatabase
from ..service.models import MODELS

@dataclass
class DatabaseManager:
    host: str | None = None
    port: int | None = None

    user: str | None = None
    password: str | None = None

        

    def getDatabase(self):
        if self.host is None or self.port is None or self.user is None or self.password is None:
            raise ValueError("Database information is incomplete")
        
        db = MySQLDatabase("forgeorder", host=self.host, port=self.port, user=self.user, password=self.password)

        self.initalize(db)
        
        return db
    
    def getDatabasePool(self):
        if self.host is None or self.port is None or self.user is None or self.password is None:
            raise ValueError("Database information is incomplete")

        db = PooledMySQLDatabase("forgeorder",
                                host=self.host,
                                port=self.port,
                                user=self.user,
                                password=self.password)

        self.initalize(db)

        return db
    
    @staticmethod
    def initalize(database: MySQLDatabase):
        database.connect(reuse_if_open=True)

        database.bind(MODELS)

        database.create_tables(MODELS)

    
    
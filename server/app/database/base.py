from dataclasses import dataclass

from peewee import MySQLDatabase
from playhouse.pool import PooledMySQLDatabase
from core.serialization.serializers.custom import ProxySerializer
from .model import TABLES

@dataclass
class Database:
    host: str | None = None
    port: int | None = None

    user: str | None = None
    password: str | None = None

        

    def getDatabase(self):
        if self.host is None or self.port is None or self.user is None or self.password is None:
            raise ValueError("Database information is incomplete")
        
        return MySQLDatabase("forgeorder", host=self.host, port=self.port, user=self.user, password=self.password)

    def getDatabasePool(self):
        if self.host is None or self.port is None or self.user is None or self.password is None:
            raise ValueError("Database information is incomplete")

        return PooledMySQLDatabase("forgeorder",
                                host=self.host,
                                port=self.port,
                                user=self.user,
                                password=self.password)
    
    @staticmethod
    def initalize(database: MySQLDatabase):
        database.connect(reuse_if_open=True)

        database.bind(TABLES)

        database.create_tables(TABLES)

    
    
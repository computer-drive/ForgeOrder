import datetime
import sqlite3

from .schema import SQL
from .exceptions import ExecuteError

def adapt_datetime(dt: datetime.datetime) -> str:
    return dt.isoformat()

def convert_datetime(dt: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(dt)

sqlite3.register_adapter(datetime.datetime, adapt_datetime)
sqlite3.register_converter("datetime", convert_datetime) #type: ignore


class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name

        self.conn : sqlite3.Connection = None #type: ignore


    def connect(self):
        self.conn = sqlite3.connect(self.db_name)

        self.conn.row_factory = sqlite3.Row #type: ignore

    def close(self):
        self.commit()

        self.conn.close()

        self.conn = None #type: ignore

    def execute(self, sql: str, params: tuple = None): # type: ignore
        try:
            self.conn.execute(sql, params or ())
        except sqlite3.OperationalError as e:
            raise ExecuteError(sql, e)


    def executescript(self, sql: str):
        try:
            self.conn.executescript(sql)
        except sqlite3.OperationalError as e:
            raise ExecuteError(sql, e)

    def commit(self):
        self.conn.commit()

    def fetchall(self):
        return self.conn.cursor().fetchall()
    
    def fetchone(self):
        return self.conn.cursor().fetchone()
    
    def get_all_columns(self, table_name: str):
        cursor =  self.conn.execute(
            SQL.GET_ALL_COLUMNS.format(table_name=table_name)).fetchall()
        
        result = []

        for row in cursor:
            result.append(row["name"])
        
        return result

    
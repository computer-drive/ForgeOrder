import sqlite3

from libs.db.database import Database
from libs.db.sql_parse import SqlParse
import os

class _DishedCategory:
    def __init__(self, conn: sqlite3.Connection, sql_parse: SqlParse):
        self.conn = conn
        self.sql_parse = sql_parse

    def get_all(self):
        cursor = self.conn.execute(self.sql_parse.get("category.get_all"))
        return cursor.fetchall()
    
    def new(self, name: str):
        cursor = self.conn.execute(self.sql_parse.get("category.new"), (name,))
        self.conn.commit()
        
        return cursor.lastrowid
    
    def get_from_id(self, id: int):
        cursor = self.conn.execute(self.sql_parse.get("category.get_from_id"), (id,))
        return cursor.fetchone()
    
    def get_from_name(self, name: str):
        cursor = self.conn.execute(self.sql_parse.get("category.get_from_name"), (name,))
        return cursor.fetchone()
    
    def update(self, id: int, name: str):
        cursor = self.conn.execute(self.sql_parse.get("category.update"), (name, id))
        self.conn.commit()
        
  

class MetaDatabase(Database):
    def __init__(self, db_name: str):
        super().__init__(db_name)

        self.connect()


        self._init()

        self.category = _DishedCategory(self.conn, self.sql_parse)

    def _init(self):
        ## 获取meta.sql
        current_path = os.path.abspath(os.path.dirname(__file__)) # script目录
        res_path = os.path.join(
            os.path.dirname(current_path), # server 目录
            "res",
        ) 

        # 初始化加载器
        self.sql_parse = SqlParse(os.path.join(res_path, "meta.sql"))

        # 执行init命令
        self.executescript(self.sql_parse.get("init"))
        self.commit()
        
        self.conn.row_factory = sqlite3.Row # !: 无需注意SQL注入问题

if __name__ == "__main__":
    meta_db = MetaDatabase("test.db")
    
    # meta_db.category.new("test")

    print(dict(meta_db.category.get_from_id(1)))

    




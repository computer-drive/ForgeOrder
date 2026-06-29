import sqlite3
from libs.db.database import Database
from libs.db.sql_parse import SqlParse

import os

class MainDatabse(Database):
    def __init__(self, db_name: str) -> None:
        super().__init__(db_name)
        self.connect()

        self._init()

    def _init(self):
        # 获取res
        current_path = os.path.abspath(os.path.dirname(__file__)) # script目录
        res_path = os.path.join(
            os.path.dirname(current_path), # server 目录
            "res",
        )

        # 执行sql_parse
        self.sql_parse = SqlParse(res_path)

        # 执行初始化命令
        self.conn.executescript(self.sql_parse.get("init"))
        self.conn.commit()

        # 设置row_factory为sqlite3.Row
        self.conn.row_factory = sqlite3.Row



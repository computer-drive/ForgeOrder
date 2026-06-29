import sqlite3
from libs.db.database import Database
from libs.db.sql_parse import SqlParse
import os
import datetime


class _Users:
    def __init__(self, conn: sqlite3.Connection, sql_parse: SqlParse):
        self.conn = conn
        self.sql_parse = sql_parse

    def new(self,
            username: str,
            password: str,
            is_admin: bool = False,
            is_available: bool = True,
            created_at: datetime.datetime = None):
        '''
        创建一个新用户。返回新用户的id。

        注意：password参数应传递哈希值而不是明文密码。
        当created_at为None时，默认使用当前时间。
        若已存在相同用户名的用户，则会抛出ValueError，不抛出异常的方法为new_s
        '''
        # 生成创建时间
        if created_at is None:
            created_at = datetime.datetime.now()

        try:
            # 执行new命令以在users表中创建新用户
            cursor = self.conn.execute(
                self.sql_parse.get("users.new"),
                (username, password, is_admin, is_available, created_at)
                )
            self.conn.commit()

            return cursor.lastrowid
        
        except sqlite3.IntegrityError:
            raise ValueError(f"Username {username} already exists")
    
    def new_s(self, 
            username: str,
            password: str,
            is_admin: bool = False,
            is_available: bool = True,
            created_at: datetime.datetime = None):
        '''
        创建一个新用户。返回新用户的id。本方法的效果与new方法相同，只是在创建用户时不会抛出异常。

        注意：password参数应传递哈希值而不是明文密码。
        当created_at为None时，默认使用当前时间。
        若已存在相同用户名的用户，则会返回None。
        '''
        cursor = self.conn.execute(
            self.sql_parse.get("users.get_from_username"),
            (username,)
            )
        
        user = cursor.fetchone()
        if user:
            return None
        
        return self.new(username, password, is_admin, is_available, created_at)
        

class MainDatabse(Database):
    def __init__(self, db_name: str) -> None:
        super().__init__(db_name)
        self.connect()

        self._init()

        self.users = _Users(self.conn, self.sql_parse)

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



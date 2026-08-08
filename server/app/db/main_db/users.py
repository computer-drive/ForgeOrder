import sqlite3

from core.db.sql_parse import SqlParse
import datetime
from core.db.exceptions import NotFoundError

class Users:
    def __init__(self, conn: sqlite3.Connection, sql_parse: SqlParse):
        self.conn = conn
        self.sql_parse = sql_parse

        self.conn.execute(self.sql_parse.get("users.create"))
        self.conn.commit()
        

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
    
    def get_from_id(self, user_id: int):
        '''
        根据用户id获取用户信息。用户不存在将返回None。

        注意：数据库使用了Row factory，返回的用户信息为Row对象。
        '''
        cursor = self.conn.execute(
            self.sql_parse.get("users.get_from_id"),
            (user_id,)
            )
        user = cursor.fetchone()
        if user:
            return user
        return None

    def get_from_username(self, username: str):
        '''
        根据用户名获取用户信息。用户不存在将返回None。

        注意：数据库使用了Row factory，返回的用户信息为Row对象。
        '''
        cursor = self.conn.execute(
            self.sql_parse.get("users.get_from_username"),
            (username,)
            )
        user = cursor.fetchone()
        if user:
            return user
        return None
    
    def verify(self, username: str, password: str):
        '''
        验证用户名和密码是否匹配。元组(int, sqlite3.Row)。

        返回的元组第一个表示验证状态（0=成功，1=用户不存在，2=密码错误，3=用户已被禁用）

        注意：password参数应传递哈希值而不是明文密码。
        若用户不存在，则会返回None。
        '''

        # 获取用户
        cursor = self.conn.execute(
            self.sql_parse.get("users.get_from_username"),
            (username,)
            )
        user = cursor.fetchone()

        if not user:
            # 用户不存在
            return 1, None

        if user["password"] != password:
            # 密码错误
            return 2, None

        if user["is_available"] == 0:
            # 用户已被禁用
            return 3, None

        return 0, user

    def change_password(self, user_id: int, new_password: str):

        cursor = self.conn.execute(self.sql_parse.get("users.change_password"),
                                   (new_password, user_id, ))
        
        if cursor.rowcount == 0:
            raise NotFoundError(str(user_id))

        self.conn.commit()

        return

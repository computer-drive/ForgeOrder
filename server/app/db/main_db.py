import datetime
import os
import sqlite3

from core.db.database import Database
from core.db.sql_parse import SqlParse
from core.utils import pad_string
from app.db.schema import *
import extensions

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
    
class _Tables:
    def __init__(self, conn: sqlite3.Connection, sql_parse: SqlParse):
        self.conn = conn
        self.sql_parse = sql_parse
        
    def new(self, name: str, is_available: bool = True):
        '''
        创建一个新桌。返回新桌的id。
        
        注意：若已存在相同桌名的桌，则会抛出ValueError，不抛出异常的方法为new_s。
        '''
        try:
            # 执行new命令以在tables表中创建新表
            cursor = self.conn.execute(
                self.sql_parse.get("tables.new"),
                (name, is_available)
                )
            
            self.conn.commit()

            return cursor.lastrowid
        
        except sqlite3.IntegrityError:
            raise ValueError(f"Table name {name} already exists")
    
    def new_s(self, name: str, is_available: bool = True):
        '''
        创建一个新桌。返回新桌的id。本方法的效果与new方法相同，只是在创建桌时不会抛出异常。

        注意：若已存在相同桌名的桌，则会返回None。
        '''
        cursor = self.conn.execute(
            self.sql_parse.get("tables.get_from_name"),
            (name,)
            )
        table = cursor.fetchone()
        if table:
            return None
        
        return self.new(name, is_available)
    
    def get_from_name(self, name: str):
        '''
        根据桌名获取桌信息。桌不存在将返回None。

        注意：数据库使用了Row factory，返回的桌信息为Row对象。
        '''
        cursor = self.conn.execute(
            self.sql_parse.get("tables.get_from_name"),
            (name,)
            )
        table = cursor.fetchone()
        if table:
            return table
        return None
    
    def get_all_available(self):
        '''
        获取所有可用的桌。

        注意：数据库使用了Row factory，返回的桌信息为Row对象列表。
        '''
        cursor = self.conn.execute(
            self.sql_parse.get("tables.get_all_available")
            )
        tables = cursor.fetchall()
        return tables


class _Order:
    '''
    一个订单的单类，用于处理订单的创建、获取、更新等操作。
    '''
    def __init__(self,
                 id: int,
                 display_no: int,
                 creator: int,
                 table_no: int,
                 created_at: datetime.datetime,
                 note: str,
                 order_items: list[OrderItemInput]
                 ):
        # orders表项
        self.id = id
        self.display_no = display_no
        self.creator = creator
        self.table_no = table_no
        self.note = note
        self.total_mount = 0

        # order_stats表项
        self.status: int = 0 # --0: 待处理 --1: 制作中 --2: 待结账 --3: 已结账
        
        self.updated_at : datetime.datetime | None = None
        self.created_at = created_at
        self.pay_at: datetime.datetime | None = None
        self.finish_at: datetime.datetime | None = None
        self.pay_method: int = 0 # --0: 现金 --1: 支付宝 --2: 微信

        self.discount: int = 0 #优惠金额
        self.finally_mount: int | None = None #最终金额

        self.items : list[OrderItemRecord] = [] # 订单项列表

        # 计算总价
        for item in order_items:
            self.total_mount += item["total_mount"]
        


    def update_orders(self):
        # return {
        #     "id": self.id,
        #     "creator": self.user_id,
        #     "display_no": self.display_no,
        #     "table_no": self.table_id,
        #     "total_mount": self.total_mount,
        #     "note": self.note,
        # }
        return (
            self.creator,
            self.display_no,
            self.table_no,
            self.total_mount,
            self.note,
            self.id,
        )
    
    def update_order_items(self, items: list[OrderItemRecord]):
        self.items = items
        

    def update_order_stats(self):
        # return {
        #     "id": self.id,
        #     "stats": self.stats,
        #     "updated_at": self.updated_at,
        #     "created_at": self.created_at,
        #     "pay_at": self.pay_at,
        #     "finish_at": self.finish_at,
        #     "pay_method": self.pay_method,
        #     "discount": self.discount,
        #     "finally_mount": self.finally_mount,
        # }
        return (
            self.status,
            self.updated_at,
            self.created_at,
            self.pay_at,
            self.finish_at,
            self.pay_method,
            self.discount,
            self.finally_mount,
            self.id
        )



class _Orders:
    '''
    综合处理订单操作（包括orders、order_items、order_stats）

    '''
    def __init__(self, conn: sqlite3.Connection, sql_parse: SqlParse):
        self.conn = conn
        self.sql_parse = sql_parse

    def get_latest_order(self, now_str: str):
        '''
        获取最新的订单。
        '''
        cursor = self.conn.execute(
            self.sql_parse.get("orders.get_latest_order"),
            (now_str + "%",)
            )
        order = cursor.fetchone()
        if order:
            return order
        return None
    
    def to_order(self, row: sqlite3.Row):
        pass
    
    def new(self, 
            user_id: int,
            table_id: int,
            created_at: datetime.datetime,
            order_items: list[OrderItemInput],
            note: str = "",
            ):
        # 生成订单的id 2026 06 24 35   0061
        #            年份  月  日 用户  
        
        # 获取最新的订单
        now = datetime.datetime.now()

        latest_order = self.get_latest_order(now.strftime("%Y%m%d"))
        latest_id = latest_order['id'] if latest_order else 0

        # 获取订单号后四位数字
        if latest_id != 0:
            counter = int(latest_id[-4:])
        else:
            counter = 0

        counter += 1
        
        # 生成订单号
        id_str = now.strftime("%Y%m%d") # 增加日期

        id_str += pad_string(str(user_id), 2, "0", "left") # 增加用户id

        id_str += pad_string(str(counter), 4, "0", "left") # 增加订单号
   

        id_int = int(id_str)

        # 取订单号后4位并+1
        # !: 实际上这里会有大于9999的订单号，但不常见
        if latest_id != 0:
            id_str += str(int(latest_id[-4:]) + 1)
        else:
            id_str += "0001"
        
        latest_display_no = latest_order['display_no'] if latest_order else 0 # 获取最新的订单的流水号
        display_no = latest_display_no + 1 # 增加流水号


        order = _Order(
            id_int, display_no, user_id, table_id, created_at, note, order_items
            )
        
        # !：在这里，创建了_Order对象，但为写入数据库，以下为更新订单表
        self.update_orders(order)
        self.update_order_stats(order)

        # !: 将order_items写入数据库，并传递给_Order对象
        order_items_ : list[OrderItemRecord] = [] 
        for item in order_items:
            cursor = self.conn.execute(
                self.sql_parse.get("order_items.new"),
                (order.id, item["dish_id"], item["price"], item["count"], item["total_mount"], item["choices"])
                )
            
            item_id = cursor.lastrowid
            
            item_ : OrderItemRecord = item.copy()  # 创建一个新的字典副本  # type:ignore
            item_["order_id"] = order.id  # 添加 order_id 字段 
            item_["item_id"] = item_id  # 添加 item_id 字段 # type:ignore


            order_items_.append(item_)

            
            

    def update_orders(self, order: _Order):
        self.conn.execute(
            self.sql_parse.get("orders.update_orders"),
            order.update_orders()
            )
        
        self.conn.commit()

    def update_order_stats(self, order: _Order):
        self.conn.execute(
            self.sql_parse.get("order_stats.update_order_stats"),
            order.update_order_stats()
            )
        self.conn.commit()

    

class MainDatabase(Database):
    def __init__(self, db_name: str) -> None:
        super().__init__(db_name)
        self.connect()

        self._init()

        self.users = _Users(self.conn, self.sql_parse)
        self.tables = _Tables(self.conn, self.sql_parse)
        self.orders = _Orders(self.conn, self.sql_parse)

    def _init(self):
        # 获取res
        res_path = os.path.join(extensions.root_dir, "res")
        sql_file = os.path.join(res_path, "main.sql")

        # 执行sql_parse
        self.sql_parse = SqlParse(sql_file)

        # 执行初始化命令
        self.conn.executescript(self.sql_parse.get("init"))
        self.conn.commit()

        # 设置row_factory为sqlite3.Row
        self.conn.row_factory = sqlite3.Row


if __name__ == "__main__":
    from werkzeug.security import generate_password_hash
    
    db = MainDatabase("main.db")

    db.users.new(
        "user1",
        generate_password_hash("123456"),
        True,
        True,
        datetime.datetime.now(),
    )

import sqlite3
import datetime

from core.db.sql_parse import SqlParse
from .schema import OrderItemInput, OrderItemRecord
from core.utils.common import pad_string

# TODO：此部分要大改，原有的部分将弃用

class Order:
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

class Orders:
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

        
        latest_display_no = latest_order['display_no'] if latest_order else 0 # 获取最新的订单的流水号
        display_no = latest_display_no + 1 # 增加流水号


        order = Order(
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

        self.conn.commit()

            
            

    def update_orders(self, order: Order):
        self.conn.execute(
            self.sql_parse.get("orders.update_orders"),
            order.update_orders()
            )
        
        self.conn.commit()

    def update_order_stats(self, order: Order):
        self.conn.execute(
            self.sql_parse.get("order_stats.update_order_stats"),
            order.update_order_stats()
            )
        self.conn.commit()

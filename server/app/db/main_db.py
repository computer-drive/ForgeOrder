import datetime
import os
import sqlite3
import json

from core.db.database import Database
from core.db.sql_parse import SqlParse
from core.utils import pad_string
from app.db.schema import *
import extensions
from core.db.exceptions import ColumnNotFoundError, NotFoundError
from .exceptions import CategoryNotFoundError

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

    def change_pasword(self, user_id: int, new_password: str):

        cursor = self.conn.execute(self.sql_parse.get("users.change_password"),
                                   (new_password, user_id, ))
        
        if cursor.rowcount == 0:
            raise NotFoundError(str(user_id))

        self.conn.commit()

        return

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

        self.conn.commit()

            
            

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

class _DishesCategory:
    def __init__(self, conn: sqlite3.Connection, sql_parse: SqlParse):
        self.conn = conn
        self.sql_parse = sql_parse

    def get_all(self) -> list[sqlite3.Row]:
        '''
        获取所有分类。

        注意：数据库使用了RowFactory，返回一个Row对象列表。
        '''
        cursor = self.conn.execute(self.sql_parse.get("category.get_all"))
        return cursor.fetchall()
    
    def new(self, name: str) -> int:
        '''
        创建一个新分类。返回新分类的id

        注意：在分类存在时抛出ValueError。不抛出异常的方法为new_s。
        '''
        try:
            cursor = self.conn.execute(self.sql_parse.get("category.new"), (name,))
        except sqlite3.IntegrityError:
            raise ValueError(f"Category {name} already exists")
        
        else:
            self.conn.commit()
        
            return cursor.lastrowid # type: ignore
             
    def new_s(self, name: str) -> int:
        '''
        创建一个新分类。若分类已存在，则返回这个分类的id。

        注意：本方法不抛出异常（与new相对）
        '''

        # 检查分类是否存在

        category = self.get_from_name(name)
        if category:
            return category["id"]
        else:
            return self.new(name)
        
    
    def get_from_id(self, id: int) -> sqlite3.Row | None:
        '''
        根据id获取分类。

        注意：数据库使用了RowFactory，返回一个Row对象或None。
        '''
        # print(self.sql_parse.get("category.get_from_id"))
        result = self.conn.execute(self.sql_parse.get("category.get_from_id"), (id,)).fetchone()

        if result:
            return result
        else:
            raise NotFoundError(str(id))
    
    def get_from_name(self, name: str) -> sqlite3.Row | None:
        '''
        根据名称获取分类。

        注意：数据库使用了RowFactory，返回一个Row对象或None。
        '''
        cursor = self.conn.execute(self.sql_parse.get("category.get_from_name"), (name,))
        return cursor.fetchone()
    
    def update(self, id: int, name: str) -> None:
        '''
        更新分类名称。
        '''
        cursor = self.conn.execute(self.sql_parse.get("category.update"), (name, id))
        self.conn.commit()
    
    def delete(self, id: int): 
        '''
        删除分类。

        '''

        cursor = self.conn.execute(self.sql_parse.get("category.delete"), (id,))

        if cursor.rowcount == 0:
            raise NotFoundError(str(id))
        
        self.conn.commit()

    def set_name(self, id: int, name: str) -> None:
        '''
        设置分类名称。
        '''
        cursor = self.conn.execute(self.sql_parse.get("category.set_name"), (name, id))
        if cursor.rowcount == 0:
            raise NotFoundError(str(id))
        self.conn.commit()
   
class _Dishes:
    def __init__(self, parent_database, conn: sqlite3.Connection, sql_parse: SqlParse):
        self.conn = conn
        self.sql_parse = sql_parse
        self.parent_database = parent_database

    def create(self,
               name: str,
               price: int, # 单位：分
               category_id: int,
               description: str = "",
               image: str = "",
               is_available: bool = True,
               choices: dict = {}
               ):
        '''
        创建一个新菜品。
        '''

        # 生成创建时间
        created_at = datetime.datetime.now()
        
        # 验证分类是否存在
        category = self.parent_database.category.get_from_id(category_id)
        if not category:
            raise CategoryNotFoundError(category_id)
        
        category = dict(category)

        
        
        # 执行create1和create2命令以在dishes和dish_stats表中创建新菜品
        cursor = self.conn.execute(
            self.sql_parse.get("dishes.create1"),
            (name, price, category_id, description, image, is_available, created_at)
            )
        
        dish_id = cursor.lastrowid

        cursor = self.conn.execute(
            self.sql_parse.get("dishes.create2"),
            (dish_id, created_at)
            )
        
        # 执行create3命令以在dish_choices表中创建新菜品的选择
        # 判断是否有选择
        if choices != {}:
            for name, options in choices.items():

                if not (isinstance(name, str) and isinstance(options, list)):
                    # 验证选择类型
                    raise ValueError(f"Choice type error: {name}")
                
                for option in options: #type: ignore
                    # 验证选项类型
                    if not isinstance(option, str):
                        raise ValueError(f"Option type error in {name}: {option}(type: {type(option).__name__}")
                    
                # 执行create3命令以在dish_choices表中创建新菜品的选择
                self.conn.execute(
                    self.sql_parse.get("dishes.create3"),
                    (dish_id, name, json.dumps(options))
                )
        
        # 提交事务
        self.conn.commit()

        return dish_id


    def get_all(self):
        '''
        获取所有菜品。
        '''
        # 准备返回结构
        result: dict[int, list] = {}

        # 1、获取所有分类并构建id->name映射，同时初始化每个分类的列表
        categories = self.parent_database.category.get_all()
        categories_map = {category["id"]: category["name"] for category in categories}
        for cid in categories_map.keys():
            result[cid] = []

        # 2、一次性获取所有相关表数据
        dishes_rows = self.conn.execute(self.sql_parse.get("dishes.get_all")).fetchall()
        dish_stats_rows = self.conn.execute(self.sql_parse.get("dish_stats.get_all")).fetchall()
        dish_choices_rows = self.conn.execute(self.sql_parse.get("dish_choices.get_all")).fetchall()

        # 3、构建索引以避免嵌套循环
        stats_map = {stat["id"]: dict(stat) for stat in dish_stats_rows}

        choices_map: dict[int, dict[str, list]] = {}
        for choice in dish_choices_rows:
            did = choice["dish_id"]
            if did not in choices_map:
                choices_map[did] = {}
            choices_map[did][choice["name"]] = json.loads(choice["options"])

        # 4、组装菜品并分配到分类中
        for row in dishes_rows:
            dish = dict(row)

            # 附加统计信息（如果存在）
            stat = stats_map.get(dish["id"])
            if stat is not None:
                dish["stat"] = stat

            # 附加选择（如果存在）
            ch = choices_map.get(dish["id"])
            if ch is not None:
                dish["choices"] = ch

            # 将菜品加入对应分类，若分类缺失则创建一个临时列表
            try:
                cid = int(dish["category"])
            except Exception:
                cid = None

            if cid is None or cid not in result:
                # 把未知分类也放入结果（使用id作为键）
                if cid is None:
                    continue
                result.setdefault(cid, []).append(dish)
            else:
                result[cid].append(dish)

        # 5、将result的key转换为分类名称并返回
        result_by_name: dict[str, list] = {}
        for cid, items in result.items():
            name = categories_map.get(cid, str(cid))
            result_by_name[name] = items

        return result_by_name, categories_map


    def get_from_id(self, dish_id: int):
        '''
        获取菜品信息。
        '''
        dish_data = self.conn.execute(self.sql_parse.get("dishes.get"), (dish_id,)).fetchone()

        if not dish_data:
            raise NotFoundError(str(dish_id))
        
        result = dict(dish_data)

        choices = self.conn.execute(self.sql_parse.get("dish_choices.get"), (dish_id,)).fetchall()
        
        result["choices"] = {}
        for choice in choices:
            result["choices"][choice["name"]] = json.loads(choice["options"])
        
        return result

    def gets_from_category(self, category_id: int):
        '''
        获取分类下的所有菜品。
        '''
        result = self.conn.execute(self.sql_parse.get("dishes.get_from_category"), (category_id,)).fetchall()
               
        return [dict(dish) for dish in result]
    
    def _update_dishes(self, dish_id: int, changed_items):
        '''
        更新菜品信息。
        '''
        # 获取所有列
        
        columns = list(self.parent_database.get_all_columns("dishes"))

            
        for key in changed_items.keys():
            if key not in columns:
                raise ColumnNotFoundError("dishes", key)
        
        
        query_keys = ""
        for key, value in changed_items.items():
            query_keys += f"{key} = ?,"

        query_keys = query_keys.rstrip(",")

        # query_sql_values = ("VALUES (" + "?," * (len(changed_items.values()) + 1)).rstrip(",") + ")" 
        query_sql_values = ''
        
        # print(self.sql_parse.get("dishes.update").format(settings = query_keys,
                                                    #    value = query_sql_values))
        
        cursor = self.conn.execute(
            self.sql_parse.get("dishes.update").format(settings = query_keys,
                                                       value = query_sql_values),
            list(changed_items.values()) + [dish_id])
        
        # 判断是否更新成功
        if cursor.rowcount == 0:
            raise NotFoundError(str(dish_id))
        
        # 提交事务
        self.conn.commit()

    def _update_dish_choices(self, dish_id: int, changed_choices: list[dict]):
        '''
        更新菜品选择。
        '''

        PAIR = {
        "new_option": "delete_option",
        "delete_option": "new_option",
        "new_choice": "delete_choice",
        "delete_choice": "new_choice",
    }

        remain = {}

        for item in changed_choices:
            t = item["type"]

            if t in ("new_option", "delete_option"):
                key = ("option", item["name"], item["option"])
            else:
                key = ("choice", item["name"])

            if key not in remain:
                remain[key] = item
                continue

            prev = remain[key]

            if PAIR.get(prev["type"]) == t:
                # 配对成功，删除
                del remain[key]
            else:
                remain[key] = item

        unique_choices = list(remain.values())
        

        # 执行数据库命令，更新菜品选择
        for action in unique_choices:
            if action["type"] == "new_choice":
                # 新增选择
                self.conn.execute(self.sql_parse.get("dish_choices.new"),
                                  (dish_id, action["name"], json.dumps([]), ))
            
            elif action["type"] == "delete_choice":
                # 删除选择
                self.conn.execute(self.sql_parse.get("dish_choices.delete"),
                                  (dish_id, action["name"], ))
                
                # print("删除项目：", action["name"])

            
            elif action["type"] == "new_option" or action["type"] == "delete_option":
                
                # 获取选项
                # print(type(dish_id))
                choices = self.conn.execute(self.sql_parse.get("dish_choices.get_choice"),
                                          (dish_id, action["name"], )).fetchone()
                
                if not choices:
                    raise NotFoundError(str((dish_id, action["name"], )))
                
                options = json.loads(choices["options"])

                if action["type"] == "new_option":
                    options.append(action["option"])
                else:
                    options.remove(action["option"])

                self.conn.execute(self.sql_parse.get("dish_choices.update"),
                                  (json.dumps(options), dish_id, action["name"], ))
                
                # print("删除项目：", action["option"])
                
            
        self.conn.commit()
            


    def update(self, dish_id: int, changed_items: dict, changed_choices: list):
        if changed_items:
            self._update_dishes(dish_id, changed_items)
        
        if changed_choices:
            self._update_dish_choices(dish_id, changed_choices)
        
    
    def delete(self, dish_id: int):
        cursor = self.conn.execute(self.sql_parse.get("dishes.delete1"),
                              (dish_id,))
            
        if cursor.rowcount == 0:
            raise NotFoundError(str(dish_id))
        
        self.conn.execute(self.sql_parse.get("dishes.delete2"),
                              (dish_id, ))
        
        self.conn.execute(self.sql_parse.get("dishes.delete3"),
                              (dish_id, ))

        self.conn.commit()

        return True 

    def delete_by_category(self, category_id: int):
        cursor = self.conn.execute(self.sql_parse.get("dishes.delete_by_category"),
                              (category_id,))
            
        self.conn.commit()

        return True 
    
class _Settings:
    def __init__(self, conn: sqlite3.Connection, sql_parse: SqlParse):
        self.conn = conn
        self.sql_parse = sql_parse

    def get(self, key: str):
        cursor = self.conn.execute(self.sql_parse.get("settings.get"), (key,))
        
        
        result = cursor.fetchone()
        
        if result:
            return dict(cursor.fetchone())
        else:
            return None


    
    def insert(self, key: str, value: str):
        self.conn.execute(self.sql_parse.get("settings.insert"),
                              (key, value, ))
        self.conn.commit()


class MainDatabase(Database):
    def __init__(self, db_name: str) -> None:
        super().__init__(db_name)
        self.connect()

        self._init()

        self.users = _Users(self.conn, self.sql_parse)
        
        self.tables = _Tables(self.conn, self.sql_parse)

        self.orders = _Orders(self.conn, self.sql_parse)

        self.category = _DishesCategory(self.conn, self.sql_parse)

        self.dishes = _Dishes(self, self.conn, self.sql_parse)

        self.settings = _Settings(self.conn, self.sql_parse)

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
    import random
    main_db =  MainDatabase('data/main.db')
    for i in range(10):
        category_id = main_db.category.new_s(f"分类{i}")

        # 创建一个新菜品
        for j in range(100):
            main_db.dishes.create(
            name=f"测试菜品{i}{j}",
            price=random.randint(100, 200),
            category_id=category_id,
            description="这是一个测试菜品",
            is_available=True,
            choices={            
                "大小": ["小", "中", "大"],
                "口味": ["甜", "酸", "咸"]
            }
        )

    # from werkzeug.security import generate_password_hash

    # 

    # db.users.new("admin",
    #               generate_password_hash("123456"),

    #             True,
    #               True)

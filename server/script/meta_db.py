import datetime
import sqlite3
from core.db.database import Database
from core.db.sql_parse import SqlParse
import os
from core.db.exceptions import NotFoundException
import json

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
        cursor = self.conn.execute(self.sql_parse.get("category.get_from_id"), (id,))
        return cursor.fetchone()
    
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
        
class _Dishes:
    def __init__(self, parent_database: MetaDatabase, conn: sqlite3.Connection, sql_parse: SqlParse):
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
               ) -> None:
        '''
        创建一个新菜品。
        '''

        # 生成创建时间
        created_at = datetime.datetime.now()
        
        # 验证分类是否存在
        category = self.parent_database.category.get_from_id(category_id)
        if not category:
            raise NotFoundException(str(category_id))
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


    def get_all(self):
        '''
        获取所有菜品。
        '''
        result = {}

        # 1、获取所有分类
        categories = self.parent_database.category.get_all()
        
        # 1.1、初始化分类的菜品列表为空
        for category in categories:
            result[category["id"]] = []

        # 2、从dishes表中获取菜品
        dishes = self.conn.execute(self.sql_parse.get("dishes.get_all")).fetchall()
        
        

        dishes = [dict(dish) for dish in dishes] # 2.1、转换为字典

        # 3、从dish_stats表中获取菜品统计信息
        dish_stats = self.conn.execute(self.sql_parse.get("dish_stats.get_all")).fetchall()

        # 3.1、将菜品统计信息与菜品关联
        for dish in dishes:
            for stat in dish_stats:
                if stat["id"] == dish["id"]:
                    dish["stat"] = dict(stat)
                    break

        # 4、从dish_choices表中获取菜品选择
        dish_choices = self.conn.execute(self.sql_parse.get("dish_choices.get_all")).fetchall()

        # 4.1、将菜品选择与菜品关联
        for dish in dishes:
            for choice in dish_choices:
                if choice["dish_id"] == dish["id"]:
                    if "choices" not in dish:
                        dish["choices"] = {}

                    dish["choices"][choice["name"]] = json.loads(choice["options"])

        # 5、分组
        for dish in dishes:
            result[dish["category"]].append(dict(dish))

        # 6、将result的key转换为分类名称

        # 6.1 将categories转换为字典
        categories = {category["id"]: category["name"] for category in categories}

        result_ = {} # 创建新字典因为key不可改变
        for category_id in result:
            result_[categories[category_id]] = result[category_id]

        return result_, categories


    def get(self, dish_id: int):
        '''
        获取菜品信息。
        '''
        result = self.conn.execute(self.sql_parse.get("dishes.get"), (dish_id,)).fetchone()

        if not result:
            raise NotFoundException(str(dish_id))
        
        return result
                
    

class MetaDatabase(Database):
    def __init__(self, db_name: str) -> None:
        super().__init__(db_name)

        self.connect()


        self._init()

        self.category = _DishesCategory(self.conn, self.sql_parse)

        self.dishes = _Dishes(self, self.conn, self.sql_parse)

    def _init(self) -> None:
        '''
        初始化数据库。
        '''
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
        
        # 设置RowFactory
        self.conn.row_factory = sqlite3.Row # !: 无需注意SQL注入问题

if __name__ == "__main__":
    import random
    meta_db = MetaDatabase("meta.db")

    # 创建一个新分类
    for i in range(4):
        category_id = meta_db.category.new_s(f"分类{i}")

        # 创建一个新菜品
        for j in range(10):
            meta_db.dishes.create(
            name=f"测试菜品{i}_{j}",
            price=random.randint(100, 200),
            category_id=category_id,
            description="这是一个测试菜品",
            is_available=True,
            choices={            
                "大小": ["小", "中", "大"],
                "口味": ["甜", "酸", "咸"]
            }
        )
    # meta_db = MetaDatabase("meta.db")
    # dishes, categories = meta_db.dishes.get_all()
    # print(categories)
    # with open("dishes.json", "w", encoding="utf-8") as f:
    #     json.dump(dishes, f, ensure_ascii=False, indent=2)

    




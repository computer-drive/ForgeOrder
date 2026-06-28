import datetime
import sqlite3
from libs.db.database import Database
from libs.db.sql_parse import SqlParse
import os
from libs.db.exceptions import NotFoundException

class _DishedCategory:
    def __init__(self, conn: sqlite3.Connection, sql_parse: SqlParse):
        self.conn = conn
        self.sql_parse = sql_parse

    def get_all(self):
        cursor = self.conn.execute(self.sql_parse.get("category.get_all"))
        return cursor.fetchall()
    
    def new(self, name: str):
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
        
            return cursor.lastrowid
        
    def new_s(self, name: str):
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
        
    
    def get_from_id(self, id: int):
        cursor = self.conn.execute(self.sql_parse.get("category.get_from_id"), (id,))
        return cursor.fetchone()
    
    def get_from_name(self, name: str):
        cursor = self.conn.execute(self.sql_parse.get("category.get_from_name"), (name,))
        return cursor.fetchone()
    
    def update(self, id: int, name: str):
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
               ):
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
                    (dish_id, name, options)
                )
        
        # 提交事务
        self.conn.commit()

class MetaDatabase(Database):
    def __init__(self, db_name: str):
        super().__init__(db_name)

        self.connect()


        self._init()

        self.category = _DishedCategory(self.conn, self.sql_parse)

        self.dishes = _Dishes(self, self.conn, self.sql_parse)

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
    meta_db = MetaDatabase("meta.db")

    # 创建一个新分类
    category_id = meta_db.category.new("测试分类")

    # 创建一个新菜品
    meta_db.dishes.create(
        name="测试菜品",
        price=100,
        category_id=category_id,
        description="这是一个测试菜品",
        image="https://example.com/test.jpg",
        is_available=True,
        choices={            "大小": ["小", "中", "大"],
            "口味": ["甜", "酸", "咸"]
        }
    )

    




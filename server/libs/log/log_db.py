from ..db.database import Database
from ..db.sql_parse import SqlParse
import os
import datetime

class LogDatabase(Database):
    def __init__(self, db_name: str):
        super().__init__(db_name)

        self.date_now = datetime.datetime.now().strftime("%Y%m%d")

        self.connect()

        self._init()

    def _init(self):
        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 向上推，获取res目录
        res_dir = os.path.join(os.path.dirname(
            os.path.dirname(current_dir)# libs目录
        ), # server目录 
        "res")

        # 初始化加载器
        self.parser = SqlParse(os.path.join(res_dir, "log.sql"))

        # 执行wal命令
        self.execute(self.parser.get("wal"))

        # !: 表名总是由日期构成，无需注意SQL注入问题
        self.execute(self.parser.get("check_table_exists"), (f"log_{self.date_now}",))

        # 若表不存在，则创建表
        if not self.fetchone():
            self.execute(self.parser.get("init").replace("{table_name}", f"log_{self.date_now}")) # !: 表名总是由日期构成，无需注意SQL注入问题
            self.commit()

    def insert_log(self, 
                   time: datetime.datetime,
                   level: int,
                   class_name: str,
                   method: str,
                   message: str):
        
        date_now = datetime.datetime.now().strftime("%Y%m%d")

        if date_now != self.date_now:
            self.date_now = date_now
            self._init()
        
        # !: 表名总是由日期构成，无需注意SQL注入问题
        self.execute(self.parser.get("insert_log").replace("{table_name}", f"log_{self.date_now}"), (time, level, class_name, method, message))
        self.commit()

if __name__ == "__main__":
    log_db = LogDatabase("test.db")
    
        
        

        




        
        
         

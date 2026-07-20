import datetime
import os

# import extensions

from ..db.database import Database
from ..db.sql_parse import SqlParse
# from ..utils import get_res_path


class LogDatabase(Database):
    def __init__(self, db_name: str):
        super().__init__(db_name)

        self.date_now = datetime.datetime.now().strftime("%Y%m%d")

        self.connect()

        self._init()

    def _init(self):
        # 获取当前脚本所在目录
        import extensions
        res_path = os.path.join(extensions.root_dir, "res")
        sql_file = os.path.join(res_path, "log.sql")
        self.parser = SqlParse(sql_file)

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
                   category: str,
                   action: str,
                   message: str,
                   request_id: str = None):
        
        date_now = datetime.datetime.now().strftime("%Y%m%d")

        if date_now != self.date_now:
            # print(1)
            self.date_now = date_now
            self._init()
        
        # !: 表名总是由日期构成，无需注意SQL注入问题
        self.execute(self.parser.get("insert_log").replace("{table_name}", f"log_{self.date_now}"),
                      (time, level, category, action, message, request_id))
        

if __name__ == "__main__":
    log_db = LogDatabase("test.db")
    
        
        

        




        
        
         

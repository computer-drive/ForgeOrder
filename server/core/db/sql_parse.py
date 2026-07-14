from .exceptions import *


class SqlParse:
    def __init__(self, sql_file_path: str):
        self.sql_file_path = sql_file_path
        self.queries = {}

        self._load()



    def _load(self):
        # 读取文件
        with open(self.sql_file_path, 'r', encoding="utf-8") as f:
            lines = f.readlines()

        # 判断文件是否为空
        if not lines:   
            raise EmptyFileError(self.sql_file_path)
        
        # 初始化当前命令名称与SQL语句
        current_name = ""
        current_sql = ""
        
        # 读取每一行
        for line in lines:
    
            line = line.strip()

            if not line:
                continue

            if line.startswith("-- command:"):
                # 命令定义行

                sql_name = line.replace("-- command:", "").strip()

                if not current_name:
                    current_name = sql_name


                if current_name != sql_name: # 当前命令与本行命令不同，说明开启一个新命令
                    self.queries[current_name] = current_sql 
                
                    current_name = sql_name
                    current_sql = ""
    
            
            elif line.startswith("--") or line == "": # 排除普通注释与空白行
                continue

            else:
                current_sql += line + "\n"

        
        self.queries[current_name] = current_sql

    def get(self, name: str):
        if name not in self.queries:
            raise CommandNotFoundError(name)
        
        return self.queries[name]


if __name__ == "__main__":
    sql_parse = SqlParse("test.sql")

    print(sql_parse.queries)




                



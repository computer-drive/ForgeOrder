import sqlite3

class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name

        self.conn : sqlite3.Connection = None #type: ignore

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)

    def close(self):
        self.commit()

        self.conn.close()

        self.conn = None #type: ignore

    def execute(self, sql: str, params: tuple = None): # type: ignore
        self.conn.execute(sql, params or ())

    def executescript(self, sql: str):
        self.conn.executescript(sql)

    def commit(self):
        self.conn.commit()

    def fetchall(self):
        return self.conn.cursor().fetchall()
    
    def fetchone(self):
        return self.conn.cursor().fetchone()

    
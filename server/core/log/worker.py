import datetime
import queue
import threading
import sqlite3
import os

from .schema import BUFFER_SIZE

from .log_db import LogDatabase


def write_text_log(entry):
    now = datetime.datetime.now()

    file_path = f"data/{now.strftime('%Y-%m-%d')}.log"
    
    try:
        with open(file_path, "r") as f:
            content = f.read()
    except FileNotFoundError:
        content = ""

    
    with open(file_path, "a") as f:
        if content != "":
            f.write('''
服务器无法将日志写入数据库。
{entry}
''')
        else:
            f.write(entry)
        

def worker(q: queue.Queue, db_name: str):
    buffer_count = 0

    # 连接数据库
    log_db = LogDatabase(db_name)
    
    try:
        
        while True:
            entry = q.get()

            if entry is None:
                q.task_done()
                break


            log_db.insert_log(*entry)

            buffer_count += 1

            if buffer_count >= BUFFER_SIZE:
                log_db.commit()
                buffer_count = 0

            q.task_done()
    except sqlite3.OperationalError as e:
        write_text_log(f"数据库操作错误：{e}")
        try:
            write_text_log(entry)
        except:
            pass


    log_db.commit()

    log_db.close()

def create_worker(db_name: str):
    q = queue.Queue()

    thread = threading.Thread(target=worker, args=(q, db_name), name="LogWorker")
    thread.daemon = True
    thread.start()

    return q, thread


        
        
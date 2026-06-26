import threading
import queue
from .log_db import LogDatabase
from const import *

def worker(q: queue.Queue, db_name: str):
    buffer_count = 0

    # 连接数据库
    log_db = LogDatabase(db_name)

    while True:
        
        entry = q.get()

        if entry is None:
            q.task_done()
            break

        log_db.insert_log(*entry)

        buffer_count += 1

        if buffer_count >= LOG.BUFFER_SIZE:
            log_db.commit()
            buffer_count = 0

        q.task_done()


    log_db.commit()

    log_db.close()

def create_worker(db_name: str):
    q = queue.Queue()

    thread = threading.Thread(target=worker, args=(q, db_name))
    thread.daemon = True
    thread.start()

    return q, thread


        
        
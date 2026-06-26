-- command: wal
PRAGMA journal_mode = WAL

-- command: init
CREATE TABLE IF NOT EXISTS {table_name} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    level INTEGER NOT NULL,
    class_name TEXT NOT NULL,
    method TEXT NOT NULL,
    message TEXT
)

-- command: check_table_exists
SELECT * FROM sqlite_master WHERE type = 'table' AND name = ?

-- command: insert_log
INSERT INTO {table_name} (timestamp, level, class_name, method, message)
VALUES (?, ?, ?, ?, ?)
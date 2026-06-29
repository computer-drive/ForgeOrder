-- command: init
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    is_admin INTEGER NOT NULL DEFAULT 0,
    is_available INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL,
    last_login_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    creator INTEGER NOT NULL,
    
    display_no INTEGER NOT NULL,
    table_no INTEGER NOT NULL,
    total_mount INTEGER NOT NULL,
    note TEXT,

    FOREIGN KEY (creator) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS order_items (

    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    order_id INTEGER NOT NULL,
    dish_id INTEGER NOT NULL,
    price INTEGER NOT NULL,
    count INTEGER NOT NULL,
    total_mount INTEGER NOT NULL,
    choices JSON,
 
    FOREIGN KEY (order_id) REFERENCES orders (id)
);

CREATE TABLE IF NOT EXISTS order_stats (
    id INTEGER PRIMARY KEY,

    status INTEGER NOT NULL DEFAULT 0, --0: 待处理 --1: 制作中 --2: 待结账 --3: 已结账
    updated_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL,

    pay_at TIMESTAMP,
    finish_at TIMESTAMP,

    pay_method INTEGER, --0: 现金 --1: 支付宝 --2: 微信
    
    discount INTEGER, --优惠金额
    finally_mount INTEGER, --最终金额

    FOREIGN KEY (id) REFERENCES orders (id),
);

CREATE TABLE IF NOT EXISTS tables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    is_available INTEGER NOT NULL DEFAULT 1
);


-- command: users.new
INSERT INTO users (username, password, is_admin, is_available, created_at, last_login_at)
VALUES (?, ?, ?, ?, ?);

-- command: users.get_from_username
SELECT * FROM users WHERE username = ?

-- command: users.get_from_id
SELECT * FROM users WHERE id = ?


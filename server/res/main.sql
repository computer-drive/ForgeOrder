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

CREATE TABLE IF NOT EXISTS tables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    is_available INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    creator INTEGER NOT NULL,
    
    display_no INTEGER NOT NULL,
    table_no INTEGER NOT NULL,
    total_mount INTEGER NOT NULL,
    note TEXT,
    
    FOREIGN KEY (table_no) REFERENCES tables (id),
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

    FOREIGN KEY (id) REFERENCES orders (id)
);

CREATE TABLE IF NOT EXISTS dishes_category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    is_deleted INTEGER NOT NULL DEFAULT 0
);   

CREATE TABLE IF NOT EXISTS dishes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    description TEXT,
    image TEXT,
    category INTEGER NOT NULL,
    is_available INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL,
    is_deleted INTEGER NOT NULL DEFAULT 0,

    FOREIGN KEY (category) REFERENCES dishes_category (id)
);

CREATE TABLE IF NOT EXISTS dish_stats (
    id INTEGER PRIMARY KEY,
    total_sales INTEGER NOT NULL DEFAULT 0,
    monthly_sales INTEGER NOT NULL DEFAULT 0,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (id) REFERENCES dishes (id)
);

CREATE TABLE IF NOT EXISTS dish_choices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dish_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    options JSON NOT NULL,
    FOREIGN KEY (dish_id) REFERENCES dishes (id)
);


-- command: users.new
INSERT INTO users (username, password, is_admin, is_available, created_at)
VALUES (?, ?, ?, ?, ?);

-- command: users.get_from_username
SELECT * FROM users WHERE username = ?

-- command: users.get_from_id
SELECT * FROM users WHERE id = ?

-- command: tables.new
INSERT INTO tables (name, is_available)
VALUES (?, ?);

-- command: tables.get_from_name
SELECT * FROM tables WHERE name = ?

-- command: tables.get_all_available
SELECT * FROM tables WHERE is_available = 1

-- command: orders.get_latest_order
SELECT * FROM orders WHERE id LIKE ? ORDER BY id DESC LIMIT 1

-- command: order_items.new
INSERT INTO order_items (order_id, dish_id, price, count, total_mount, choices)
VALUES (?, ?, ?, ?, ?, ?);

-- command: orders.update_orders
UPDATE orders SET creator = ?, display_no = ?, table_no = ?, total_mount = ?, note = ? WHERE id = ?

-- command: order_stats.update_order_stats
UPDATE order_stats SET status = ?, updated_at = ?, pay_at = ?, finish_at = ?, pay_method = ?, discount = ?, finally_mount = ? WHERE id = ?



-- Category 表操作

-- command: category.get_all
SELECT * FROM dishes_category WHERE is_deleted = 0

-- command: category.new
INSERT INTO dishes_category (name) VALUES (?)

-- command: category.get_from_id
SELECT * FROM dishes_category WHERE id = ? AND is_deleted = 0

-- command: category.get_from_name
SELECT * FROM dishes_category WHERE name = ? AND is_deleted = 0

-- command: category.update
UPDATE dishes_category SET name = ? WHERE id = ?

-- command: category.delete
UPDATE dishes_category SET is_deleted = 1 WHERE id = ?;

-- command: category.set_name
UPDATE dishes_category SET name = ? WHERE id = ?;

-- Dish 表操作

-- command: dishes.create1
INSERT INTO dishes (name, price, category, description, image, is_available, created_at)
VALUES (?, ?, ?, ?, ?, ?, ?);

-- command: dishes.create2
INSERT INTO dish_stats (id, updated_at)
VALUES (?, ?);

-- command: dishes.create3
INSERT INTO dish_choices (dish_id, name, options)
VALUES (?, ?, ?);


-- get_all菜品

-- command: dishes.get_all
SELECT * FROM dishes WHERE is_deleted = 0
ORDER BY id ASC

-- command: dish_stats.get_all
SELECT * FROM dish_stats
ORDER BY id DESC

-- command: dish_choices.get_all
SELECT * FROM dish_choices 
ORDER BY id DESC

-- command: dishes.get_from_category
SELECT * FROM dishes WHERE is_deleted = 0 AND category = ?


-- get菜品

-- command: dishes.get
SELECT * FROM dishes WHERE id = ?

-- command: dish_choices.get
SELECT * FROM dish_choices WHERE dish_id = ?

-- 更新菜品

-- command: dishes.update
UPDATE dishes SET {settings} WHERE id = ? {value}

-- command: dish_choices.new
INSERT INTO dish_choices (dish_id, name, options)
VALUES (?, ?, ?)

-- command: dish_choices.delete
DELETE FROM dish_choices WHERE dish_id = ? AND name = ?


-- command: dish_choices.get_choice
SELECT * FROM dish_choices WHERE dish_id = ? AND name = ?


-- command: dish_choices.update
UPDATE dish_choices SET options = ? WHERE dish_id = ? AND name = ?

-- command: dishes.delete1
UPDATE dishes SET is_deleted = 1 WHERE id = ?; -- 将dishes表的内容更新为is_deleted

-- command: dishes.delete2
DELETE FROM dish_stats WHERE id = ?; -- 删除dish_stats表的项

-- command: dishes.delete3
DELETE FROM dish_choices WHERE dish_id = ?; -- 删除dish_choices表的项

-- command: dishes.delete_by_category
UPDATE dishes SET is_deleted = 1 WHERE category = ?;







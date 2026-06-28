

-- command: init
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS dishes_category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
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

    FOREIGN KEY (category) REFERENCES dishs_category (id)
);

CREATE TABLE IF NOT EXISTS dish_stats (
    id INTEGER PRIMARY KEY,
    total_sales INTEGER NOT NULL DEFAULT 0,
    monthly_sales INTEGER NOT NULL DEFAULT 0,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (id) REFERENCES dishs (id)
)

-- Category 表操作

-- command: category.get_all
SELECT * FROM dishes_category

-- command: category.new
INSERT INTO dishes_category (name) VALUES (?)

-- command: category.get_from_id
SELECT * FROM dishes_category WHERE id = ?

-- command: category.get_from_name
SELECT * FROM dishes_category WHERE name = ?

-- command: category.update
UPDATE dishes_category SET name = ? WHERE id = ?

-- Dish 表操作

-- command: dishes.create
INSERT INTO dishes (name, price, category, description, image, is_available, created_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)



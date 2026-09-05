# 数据库与 Repository

[返回文档首页](../index.md)

ForgeOrder 当前使用项目内封装的数据库访问层。业务代码通过 `RepositoryManager` 获取具体 Repository，由 Repository 负责 SQL、类型转换和事务操作。

## 1. 数据库文件

默认数据库路径为 `data/main.db`，配置项为 `database.path`。日志数据库默认位于 `data/log.db`，配置项为 `log.database`。

首次启动时，应用会创建数据库连接并调用 `RepositoryManager.init()` 初始化业务表。

## 2. RepositoryManager

`app.db.repository.RepositoryManager` 当前注册了以下 Repository：

| Repository | 表 / 用途 |
| --- | --- |
| `users` | 用户 |
| `tokens` | 登录 Token |
| `tables` | 桌台 |
| `settings` | 应用设置 |
| `printTask` | 打印任务 |
| `dishesCategory` | 菜品分类 |
| `dishes` | 菜品 |
| `dishStats` | 菜品统计 |
| `dishChoices` | 菜品选项 |
| `orders` | 总订单 |
| `subOrders` | 子订单 |
| `orderStatus` | 订单状态与结算信息 |
| `orderItems` | 订单菜品 |

这些 Repository 在启动阶段依次初始化。

## 3. 通用 Repository API

`core.database.repository.Repository` 是业务 Repository 的基础类。

### `get(**where)`

查询单条记录：

```python
user = repos.users.get(id=user_id)
```

至少需要一个查询条件；没有条件会抛出 `EmptyQueryCriteriaError`。没有匹配记录时返回 `None`。

### `getAll(**where)`

查询多条记录：

```python
rows = repos.dishes.getAll(isDeleted=False)
```

不传条件时返回整张表的数据。

### `insert(**data)`

插入一条记录，并返回数据库 `lastrowid`。

```python
dish_id = repos.dishes.insert(
    name="Coffee",
    price=15,
    category=1,
    isAvailable=True,
    createdAt=now,
)
```

### `update(where, data)`

根据 `where` 更新 `data`。如果没有任何记录匹配，会抛出 `RecordNotFoundError`。

### `delete(where)`

执行物理删除。需要注意：业务层经常自己实现“软删除”，因此看到 `delete()` 并不代表所有业务对象都会真正从数据库消失。

例如菜品和分类使用 `isDeleted` 标记，并通过修改名称等方式避免继续作为正常数据出现。

### 事务

Repository 提供：

```python
repo.commit()
repo.rollback()
```

底层 Database 由多个 Repository 共享，因此一次业务操作可能涉及多个 Repository；提交边界应由业务操作决定。

## 4. 类型转换

每个 Repository 通过 `Column` 声明字段类型。`Repository._convertTo()` 会在写入或查询前验证并转换 Python 值；`_convertFrom()` 在读取后转换为 Python 类型。未知字段会触发 `ColumnNotFoundError`。

因此不建议在 Service 中绕过 Repository 直接拼接业务 SQL。

## 5. 自定义 SQL

Repository 提供 `execute(sql, params)`，但代码明确将其定位为 Repository 标准方法无法满足需求时的低层能力。

同时可以通过 `setCustomSQL()` 设置一次性的 SQL 片段。该机制会在执行一次操作后清除，因此使用时必须特别注意 SQL 语法和调用顺序。

## 6. 批量查询

`repo.many.getAll()` 支持将条件转换为 `IN` 查询。例如一个条件可以传入 tuple / list，以便一次查询多个值。

```python
rows = repos.dishes.many.getAll(id=(1, 2, 3))
```

## 7. 订单数据模型

订单不是单表结构，而是由多张表组成：

```text
orders
  │
  ├── orderStatus
  │
  ├── subOrders
  │     │
  │     └── orderItems
  │
  └── tableId → tables
```

`orders` 保存订单身份、显示码、类型、桌台和人数；`subOrders` 保存子订单及备注；`orderStatus` 保存生命周期状态、创建人、支付信息、金额和优惠；`orderItems` 保存具体菜品、单价、数量、金额和选项。

### 订单类型

`orders.type` 当前约定：

- `0`：堂食，需要有效桌台。
- `1`：打包，不绑定桌台。

创建订单时 `OrderService.new()` 会在堂食场景检查桌台是否存在、是否可用。

### 订单状态

`orderStatus.status` 当前约定：

| 值 | 含义 |
| ---: | --- |
| `0` | 已下单 |
| `1` | 制作中 |
| `2` | 待结账 |
| `3` | 已结账 |

这些状态值直接定义在 Repository 注释和业务代码中，后续如果修改状态机，应同步更新所有相关 Service、View 和文档。

### 金额单位

代码中的 `price` / `totalAmount` / `totalPrice` 使用整数保存，具体展示单位由上层约定；新增金额相关逻辑时不要直接假设数据库字段是浮点数。订单创建会根据菜品单价和数量计算总金额并写入 `orderStatus.totalAmount`。

## 8. 今日订单查询

`OrderStatusRepository.getTodayOrders(offset, limit)` 按当前时间的当天起止时间筛选 `createdAt`，按创建时间倒序排列，并应用分页。`OrderService.getToday()` 再将订单信息和状态信息合并，并按照状态是否为 `3` 分为 `unfinished` / `finished` 两组。

## 9. 数据库变更原则

当前项目没有独立的 migration 系统；表结构由 Repository 的 `_init()` 在启动时使用 `CREATE TABLE IF NOT EXISTS` 初始化。

因此修改已有表结构时需要谨慎：仅修改 `columns` 并不会自动迁移已经存在的数据库。正式引入字段变更前，应设计兼容旧数据库的迁移方案，而不是依赖 `_init()` 自动完成。
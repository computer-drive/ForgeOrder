[返回](index.md)

# 日志
ForgeOrder的日志为结构化日志，在记录日志时，包含如下字段：
- msg: 日志消息。
- class_name：记录日志时的功能的名称。
- method：记录日志时的方法的名称。

日志记录时，`msg`字段为可选的，因为`class_name`与`method`字段已足够描述日志的来源。`msg`字段可为`dict`、`str`等类型。

`class_name`字段应使用全大写命名法。例如：`ORDER`、`USER`、`BEFORE_REQUEST`等。

`method`字段应使用大驼峰命名法。例如：`createOrder`、`getUserInfo`等。


日志同时会在数据库中被记录。

## 数据库日志记录
由于SQLite的事务机制和阻塞问题，在执行记录函数时，日志消息并不会被立即写入数据库。

程序在启动时将启动一个线程`LogWorker`，在子线程中建立数据库连接并从队列中异步写入日志消息。

程序关闭时，自动关闭数据库连接。

日志数据库采用WAL模式，以提高写入性能。

日志在数据库中分表记录，每个表对应一天的日志。例如：2026年07月01日的日志记录在`log_20260701`表中。


## Flask及Werkzeug日志记录
日志数据库中并不会记录来自Flask和Werkzeug的日志。

在开发环境中，Flask的内置服务器会将日志打印到控制台。


## 日志格式
以下的部分，介绍了不同的`class_name`、`method`下的日志格式，日志的含义等。

**所有的`class_name`下都包含`DebugMsg`方法，用于记录调试日志。在后面的章节中，不在详细介绍。**

### BEFORE_REQUEST
介绍`class_name`为`BEFORE_REQUEST`时的日志。本部分的日志均在`/server/app/init_app/before_request.py`文件中被记录。

#### AuthError
- 级别：`INFO`
- 客户端请求，未通过认证验证。
- `msg`字段包含以下内容：
    - `ip`: 该请求的IP地址。
    - `error`: 错误信息。本字段的值与说明如下表：

| 错误信息 | 说明 |
| --- | --- |
| `InvalidToken` | 无效的Token |
| `TokenExpire` | Token过期 |
| `TokenLogout` | Token的用户已退出登录 |
| `OldDevice` | 旧设备的请求 |
| `IPNotMatch` | Token的IP地址与请求IP地址不匹配 |


**对于这些错误的详细说明，请参见[Auth Design](../auth.md)。**

#### NonAdminUserAccess
- 级别：`WARNING`
- 非管理员用户尝试访问管理员接口。
- `msg`字段包含以下内容：
    - `ip`: 该请求的IP地址。
    - `user_id`: 非管理员用户的ID。
    - `path`：请求的路径。


### FLASK_APP
介绍`class_name`为`FLASK_APP`时的日志。本部分的日志均在`/server/app/init_app`模块中被记录。

#### ExecuteError
- 级别：`ERROR`
- 数据库执行SQL语句时的错误。
- `msg`字段包含以下内容：
    - `sql`: 执行的SQL语句。
    - `origin_error`: 原始异常信息。

#### SqliteError
- 级别：`ERROR`
- 数据库操作时的错误。
- `msg`字段包含以下内容：
    - `type`: 异常的类型。
    - `msg`：异常的详细信息。

#### RequestError
- 级别：`ERROR`
- 客户端请求时未被捕获的异常。
- `msg`字段包含以下内容：
    - `traceback`: 异常的详细信息。
    - `error`: 错误信息。

### ERROR_HANDLER
介绍`class_name`为`ERROR_HANDLER`时的日志。本部分的日志均在`/server/core/error_handler/excepthook.py`文件中被记录。

#### ThreadedUncaughtException
- 级别：`ERROR`
- 子线程中未被捕获的异常。
- `msg`字段包含以下内容：
    - `type`: 异常的类型。
    - `value`: 异常的详细信息及Traceback。
    - `thread`: 子线程。

#### UncaughtException
- 级别：`ERROR`
- 主线程中未被捕获的异常。
- `msg`字段包含以下内容：
    - `type`: 异常的类型。
    - `value`: 异常的详细信息及Traceback。



### ACCOUNTS
介绍`class_name`为`ACCOUNTS`时的日志。

#### UserLogin
- 级别：`INFO`
- 用户登录。
- `msg`字段包含以下内容：
    - `user_id`: 用户ID。
    - `ip`: 登录IP地址。
    - `cover`：覆盖上一次登录。（详见[Auth Design](auth_design.md)中的说明）

#### UserLogout
- 级别：`INFO`
- 用户退出登录。
- `msg`字段包含以下内容：
    - `user_id`: 用户ID。
    - `ip`: 退出登录IP地址。


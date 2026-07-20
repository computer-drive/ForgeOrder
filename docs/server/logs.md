[返回](index.md)

# 日志
ForgeOrder的日志为结构化日志，在记录日志时，包含如下字段：
- msg: 日志消息。
- category：功能分类。
- action：功能操作。

日志记录时，`msg`字段为可选的，因为`category`与`action`字段已足够描述日志的来源。`msg`字段可为`dict`、`str`等类型。

`category`字段应使用全大写命名法。例如：`ORDER`、`USER`、`BEFORE_REQUEST`等。

`action`字段应使用大驼峰命名法。例如：`createOrder`、`getUserInfo`等。


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

## 日志上下文
在大多数情况下，对于同一个功能，日志都有相同的`category`，在这个功能里，每次记录日志都需要反复输入`category`，日志上下文处理器（`LogContext`）可以解决本问题。
例如：
```python
from core.log.context import get_log_context
import extensions

logger = get_log_context(extensions.logger, "CATEGORY_NAME")

logger.info("msg", "action")
```

在同一个日志处理器中，记录日志时无需再传递`cateogory`。

**注意：`LogContext`是对`Logger`的封装，并不是`Logger`的子类。在系统中，`Logger`涉及数据库操作、异步队列，是全局唯一的；`LogContext`对其进行封装，提供与`Logger`相同的接口。**

在系统中，使用`Logger`与`LogContext`记录日志都是支持的。



### 请求日志上下文处理器
处理请求时，`before_request`会将`RequestLogContext`（`LogContext`的子类）对象添加到`g`对象，在视图函数中，推荐使用`g.logger`以记录日志。

若不设置`category`，在请求中的日志的`category`统一为`REQUEST`，使用`g.logger.set_category`可以设置`category`的内容，例如：`LOGIN_REQUEST`。

#### Request Id
`request_id`用于标识各个请求的日志，每个请求有唯一的`request_id`，UUID v4格式。在数据库查看日志、控制台查看日志时，处理请求时记录的日志都会附上`request_id`。

`request_id`在进入视图函数，`before_request`中生成。

为了记录`request_id`，在处理请求期间记录任何日志时，都应使用`g`对象的日志上下文。

在请求处理中，可能遇到更复杂的情况：
> 在登录请求中，普通的日志的`category`为`LOGIN_REQUEST`，但处理登录成功、登录失败等业务日志时的`category`为`ACCOUNTS`。

对于上面的例子，视图函数的两个日志的`category`不同，但都应记录`request_id`。解决方法是使用`g.logger.get_log_context`方法，返回一个`LogContextWithRequestId`，在使用此上下文时，会继承当前请求的`request_id`，同时可以编辑`category`。

**注意：`request_id`为`Logger.log`方法的一个参数，默认为`None`，`request_id`自动生成，通常情况下，记录日志时请勿主动提供此参数。**


#### 请求&响应基本信息的日志
在请求进入视图函数前、后，系统将自动记录两条日志：`RequestInfo`，`ResponseInfo`，具体内容详见后面日志格式部分的信息。

对于`RequestInfo`，若在本次请求中没有记录任何日志，`RequestInfo`日志也不会被记录。




## 日志格式
以下的部分，介绍了不同的`category`、`action`下的日志格式，日志的含义等。

**所有的`category`下都包含`DebugMsg`方法，用于记录调试日志。在后面的章节中，不在详细介绍。**

### BEFORE_REQUEST
介绍`category`为`BEFORE_REQUEST`时的日志。本部分的日志均在`/server/app/init_app/before_request.py`文件中被记录。

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
介绍`category`为`FLASK_APP`时的日志。本部分的日志均在`/server/app/init_app`模块中被记录。

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
介绍`category`为`ERROR_HANDLER`时的日志。本部分的日志均在`/server/core/error_handler/excepthook.py`文件中被记录。

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
介绍`category`为`ACCOUNTS`时的日志。

#### UserLogin
- 级别：`INFO`
- 用户登录。
- `msg`字段包含以下内容：
    - `user_id`: 用户ID。
    - `ip`: 登录IP地址。
    - `cover`：覆盖上一次登录。（详见[Auth](auth.md)中的说明）

#### UserLogout
- 级别：`INFO`
- 用户退出登录。
- `msg`字段包含以下内容：
    - `user_id`: 用户ID。
    - `ip`: 退出登录IP地址。


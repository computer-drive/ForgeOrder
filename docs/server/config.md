[返回](../index.md)

# 配置文件
ForgeOrder的系统配置文件位于`data`目录下的`config.json`。
配置项以键值对的形式存在，对于不存在的键，系统将使用默认值。
若需修改配置项，需要在`config.json`中手动添加需要更改的键。
键名以`.`分隔。

## `server`配置项
此处的配置项为服务器的设置。

1. `server.host`
   - 说明：服务器运行时的地址。
   - 默认值：`0.0.0.0`。

2. `server.port`
   - 说明：服务器运行时的端口号。
   - 默认值：`5000`。

3. `server.env`
   - 说明：服务器运行时的环境。
   - 默认值：`dev`。
   - 可用值：`dev`、`product`。


## `log`配置项
此处的配置项为日志的设置。

1. `log.level`：
    - 说明：记录日志时的等级。
    - 默认值：`info`。
    - 可用值：`debug`、`info`、`warn`、`error`。
2. `log.database`：
    - 说明：记录日志的数据库文件路径。
    - 默认值：`data/log.db`。
    - 相对路径和绝对路径均可，相对路径将相对于后端的工作目录。
    - 若为空，将不使用数据库日志记录器（生产环境不推荐）。

3. `log.debug_ignore`：
    - 说明：将日志等级设置为`debug`时，忽略的`class_name`的列表。在此列表中的`class_name`且等级为`debug`的日志将不被记录。
       - 默认值：`[]`。
    - 可用值：任意字符串。

4. `log.ignore_client_error`：
    - 说明：是否记录客户端请求的错误日志。
    - 默认值：`false`。
    - 开启此选项后，将不记录任何`method`包含在`CLIENT_ERROR`（`CLIENT_ERROR`在`server\app\init_app\schema.py`被定义）中的日志。

## `database`配置项
此处的配置项为数据库的设置。

1. `database.path`：
    - 说明：数据库文件路径。
    - 默认值：`data/main.db`。
    - 相对路径和绝对路径均可，相对路径将相对于后端的工作目录。

## `auth`配置项
此处的配置项为有关用户认证的设置。

1. `auth.secret_key`：
    - 说明：生成用户认证时用的Token所用的密钥
    - 默认值：`development_key`。
    - 在生产环境中，建议以足够长的随机字符串作为密钥。

2. `auth.available_time`：
    - 说明：用户认证Token的可用时间，单位为分钟。
    - 默认值：`60`。
    - 可用值：任意正整数。


    



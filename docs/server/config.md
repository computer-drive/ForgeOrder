[返回文档首页](../index.md)

# 配置文件

ForgeOrder 的默认配置文件路径为后端工作目录下的：

```text
data/config.json
```

配置由后端的 `ConfigManager` 加载并进行验证。配置项使用 `.` 分隔的键名表示；未显式配置的项目使用代码中定义的默认值。

> **注意**：配置结构以 `server/app/config/schema.py` 为准。本文只记录当前代码中已经定义的配置项。

## 配置项

### `server`

服务器运行相关配置。

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `server.host` | `string` | `0.0.0.0` | HTTP 服务监听地址 |
| `server.port` | `integer` | `5000` | HTTP 服务监听端口，范围为 `1-65535` |
| `server.env` | `string` | `dev` | 运行环境，可选 `dev` 或 `product` |
| `server.first_start` | `boolean` | `true` | 是否视为首次启动 |

### `log`

日志系统相关配置。

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `log.level` | `string` | `info` | 日志等级，可选 `debug`、`info`、`warning`、`error`、`critical` |
| `log.database` | `string` | `data/log.db` | 日志数据库路径；相对路径相对于后端工作目录 |
| `log.debug_ignore` | `array` | `[]` | Debug 日志中需要忽略的类别列表 |
| `log.ignore_client_error` | `boolean` | `false` | 是否忽略客户端错误日志 |

### `database`

数据库相关配置。

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `database.path` | `string` | `data/main.db` | 主数据库文件路径；相对路径相对于后端工作目录 |

### `auth`

用户认证相关配置。

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `auth.available_time` | `integer` | `60` | Token 可用时间，单位为分钟，必须大于 `0` |

> 当前版本的配置 Schema 中**没有 `auth.secret_key` 配置项**。旧版文档中关于 `secret_key` 的说明已经过时，请不要继续按照旧文档配置该字段。

## 示例

下面是一个最小的自定义配置示例：

```json
{
  "server.host": "0.0.0.0",
  "server.port": 5000,
  "server.env": "dev",
  "log.level": "info",
  "database.path": "data/main.db",
  "auth.available_time": 60
}
```

未写入的配置项会继续使用默认值。

## 修改配置后的建议

修改监听地址、端口或运行环境后，建议重启 ForgeOrder 服务使配置重新加载。

生产环境尤其应确认：

- `server.env` 设置为 `product`；
- `server.port` 未与其他服务冲突；
- 数据库和日志文件路径具有正确的读写权限；
- 不要把运行数据目录提交到 Git 仓库。

[返回文档首页](../index.md)

# 后端服务器

ForgeOrder 后端位于 `server/` 目录，启动入口为 `server/run.py`。

## 启动流程

服务器启动的大致流程如下：

```text
server/run.py
    ↓
初始化异常处理
    ↓
app.init.init()
    ↓
加载并验证配置
    ↓
初始化应用 / 数据库等运行环境
    ↓
setupApp()
    ↓
注册 API Blueprint
    ↓
读取 server.host / server.port
    ↓
启动 HTTP 服务
```

应用的 Blueprint 当前包含账号、店铺、系统、订单和基础接口等模块。

## 开发环境

当 `server.env` 为 `dev` 时，后端使用 Flask 内置开发服务器：

```python
app.run(host=host, port=port)
```

源码运行：

```bash
cd server
poetry run python run.py
```

## 生产环境

当 `server.env` 为 `product` 时，后端使用 Waitress：

```python
serve(app, host=host, port=port)
```

因此生产环境和开发环境使用相同的 `run.py` 入口，只由配置决定 HTTP 服务实现。

## 网络配置

默认配置：

```text
host = 0.0.0.0
port = 5000
```

配置项见：[配置文件](config.md)。

如果 `host` 使用 `0.0.0.0`，服务器会监听所有网络接口；在局域网部署时，应同时考虑操作系统防火墙和网络访问控制。

## API 路由

业务 API 通过 `AppBlueprint` 注册。当前主要模块包括：

- `accounts`：登录和退出登录
- `shop`：营业状态、菜品、分类和桌台
- `orders`：订单相关操作
- `system`：系统相关接口
- `basic`：基础接口

具体 API 见：[API 设计](../api.md)。

## 运行数据

默认情况下，配置文件、主数据库和日志数据库位于后端工作目录的 `data/` 目录：

```text
data/
├── config.json
├── main.db
└── log.db
```

实际路径可以通过配置项修改。

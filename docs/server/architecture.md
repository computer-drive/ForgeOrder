# 后端架构

[返回文档首页](../index.md)

本文从代码结构和请求生命周期两个角度介绍 ForgeOrder 后端。后端位于 `server/`，当前实现以 Flask 为 HTTP 层，并在其上增加了路由元数据、认证、参数验证、统一响应、Repository 和 Service 等基础设施。

## 1. 分层结构

```text
server/
├── run.py                 # 进程入口
├── app/
│   ├── init.py            # 启动/关闭流程
│   ├── config/            # 配置
│   ├── hooks/             # 请求前后钩子
│   ├── routes/            # 路由元数据、参数验证和响应生成
│   ├── views/             # HTTP API 控制器
│   ├── service/           # 业务逻辑
│   ├── db/                # 业务 Repository
│   ├── printer/           # 打印任务及打印机服务
│   └── cli/               # 命令行处理
└── core/
    ├── database/          # 通用数据库 / Repository 基础设施
    ├── validation/        # 通用验证器
    ├── log/               # 通用日志
    ├── errorHandler/      # 异常处理
    ├── binpack/           # Binpack 相关能力
    └── utils/              # 通用工具
```

核心依赖方向：

```text
HTTP Request
    ↓
Flask / AppBlueprint
    ↓
beforeRequest
    ├─ 请求上下文
    ├─ Authentication / Authorization
    └─ 参数验证
    ↓
views
    ↓
service
    ↓
Repository
    ↓
Database
```

业务代码原则上不应该把数据库访问、HTTP 参数解析和业务规则全部塞进 View 中。当前项目已经通过 `Service` 与 `Repository` 对这些职责进行了拆分。

## 2. 启动流程

`server/run.py` 首先安装全局异常处理，然后调用 `app.init.init()` 完成初始化；之后通过 `setupApp()` 创建 Flask 应用并读取 `server.host` / `server.port` 启动 HTTP 服务。开发环境使用 Flask 内置服务器，生产环境使用 Waitress。

初始化阶段包括：

1. 创建 `data/` 目录（如果不存在）。
2. 加载 `data/config.json`。
3. 初始化日志系统。
4. 创建数据库连接并初始化 Repository 对应的表结构。
5. 首次启动时创建 `root` 管理员。
6. 解析 CLI 参数；如果命令要求程序停止，则执行关闭流程后退出。
7. 校验应用级设置。
8. 初始化打印管理器。

## 3. Repository 层

`RepositoryManager` 集中持有用户、Token、桌台、设置、打印任务、菜品、订单等 Repository，并在启动时逐一调用 `_init()` 创建表。

通用 `Repository` 提供以下基础能力：

- `get(**where)`：按条件获取一条记录。
- `getAll(**where)`：按条件获取多条记录；无条件时获取全部记录。
- `insert(**data)`：插入记录。
- `update(where, data)`：更新记录；没有匹配记录时抛出 `RecordNotFoundError`。
- `delete(where)`：删除记录。
- `commit()` / `rollback()`：事务提交与回滚。
- `execute(sql, params)`：执行自定义 SQL，原则上只在 Repository 封装不足时使用。
- `many.getAll(...)`：对查询条件使用 `IN` 做批量查询。

Repository 同时负责 Python 类型和数据库类型之间的转换，因此业务层通常不需要直接处理 SQLite 的底层值表示。

## 4. Service 层

Service 是业务规则的主要承载层。例如：

- `UserService` 处理登录、Token、密码和用户相关业务。
- `ShopService` 组合菜品分类、菜品和桌台业务。
- `OrderService` 处理订单创建和订单查询。

Service 通常返回统一的 `Result`，由 View 根据结果码转换为 HTTP API 响应。订单创建就是典型例子：View 调用 `OrderService.new()`，根据 `ResultCode` 将桌台、菜品、选项等业务错误映射成对应响应。

## 5. View 与路由元数据

API View 使用 `AppBlueprint`。它除了注册 Flask 路由，还会保存 `requiresAuth`、`isAdmin`、参数定义和响应定义，并在注册到 Flask 应用时交给 `RouteManager`。

因此一个 API 的定义实际上同时描述了：

- HTTP 方法和路径。
- 是否需要登录。
- 是否需要管理员权限。
- Body / Path 参数。
- 可能返回的业务响应。

`RouteManager` 将这些信息保存为路由元数据，供请求钩子使用。

## 6. 请求生命周期

请求进入 Flask 后，`beforeRequest()` 按以下顺序处理：

```text
_handleRequestInfo
      ↓
_handleAuth
      ↓
_handleArguments
      ↓
View function
      ↓
afterRequest / error handling
```

### `_handleRequestInfo`

创建 `requestId`、日志上下文和请求开始时间，初始化 `ResponseGenerator`，并获取数据库连接。

### `_handleAuth`

对于 `/api/` 请求，先从 `RouteManager` 查询路由认证元数据。需要认证的接口要求：

```http
Authorization: Bearer <token>
```

随后验证 Token、过期时间、退出状态和 Token 所绑定的 IP；管理员接口还会检查用户的 `isAdmin`。认证成功后，当前用户信息写入 `g.userInfo`。

### `_handleArguments`

根据路由元数据读取 JSON Body 和 URL Path 参数，然后执行类型检查及 Validator。失败时统一返回 `ArgumentError`，HTTP 状态码为 `400`。

## 7. 统一响应

API 使用统一结构：

```json
{
  "status": 0,
  "data": {},
  "message": "OK"
}
```

实际生成由 `ResponseInfo` → `ResponseGenerator` → `makeResponse()` 完成。每个路由声明允许返回的 `ResponseInfo`，View 通过 `g.res.<ResponseName>(data)` 生成响应。

全局错误码集中在 `GLOBAL` 中，例如参数错误 `1001`、方法错误 `1002`、资源不存在 `1003`、权限错误 `2002`、Token 无效 `2003`、Token 过期 `2004`，以及服务端/数据库相关错误 `9010`、`9020`、`9021`。

## 8. 开发建议

新增 API 时建议遵循现有模式：

1. 在 `app/views/` 中使用 `AppBlueprint` 声明路由。
2. 在 `arguments` 中声明 Body / Path 参数及 Validator。
3. 在 `responses` 中声明业务响应。
4. View 只负责请求参数和 HTTP 响应的适配。
5. 将业务规则放到 `Service`。
6. 将数据库读写放到 `Repository`。
7. 新增错误状态时同时更新对应的 ResultCode / ResponseInfo / 文档。
8. 对影响数据一致性的多步操作明确 `commit()` / `rollback()` 边界。

## 9. 当前实现中的注意事项

文档描述的是当前代码行为，而不是理想化架构。当前代码仍存在一些值得后续整理的地方，例如部分 Service / View 中存在兼容旧 API 的代码和较强的隐式约定；因此修改底层框架时应同时检查对应的路由元数据和文档。
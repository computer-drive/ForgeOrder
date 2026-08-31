# Route Manager

[返回文档首页](../index.md)

`RouteManager` 是 ForgeOrder HTTP 层的路由元数据中心。它不是 Flask 自身的路由表，而是在 Flask 注册路由之外，额外保存每个 API 的认证、权限、参数和响应定义，供请求钩子使用。

## 1. 路由元数据

每个已注册 Endpoint 对应一份 `RoutesInfo`：

```text
endpoint
├── requiresAuth
├── isAdmin
├── bodyParams
├── pathParams
└── responses
```

其中：

- `requiresAuth`：是否需要 Token 认证。
- `isAdmin`：是否需要管理员权限。
- `bodyParams`：JSON Body 参数定义。
- `pathParams`：URL Path 参数定义。
- `responses`：该接口声明的业务响应。

这些字段的结构定义在 `app.routes.schema.RoutesInfo`。

## 2. AppBlueprint 如何注册

API 通常通过 `AppBlueprint` 的 `get()` / `post()` 注册。例如：

```python
shopBlueprint.post(
    "/api/shop/setBusinessState",
    requiresAuth=True,
    isAdmin=True,
    arguments=[
        BodyField("isBusiness", bool, True)
    ],
    responses=[
        ResponseInfo(0, "OK", None)
    ]
)
```

`AppBlueprint` 会把这些信息保存到自己的 `routes_` 中；调用 `registerForApp()` 时，一方面注册 Flask Blueprint，另一方面把路由元数据交给 `RouteManager.register()`。

## 3. 注册过程

`RouteManager.register()` 会：

1. 检查 Endpoint 是否重复。
2. 将 `BodyField` 分类到 `bodyParams`。
3. 将 `PathField` 分类到 `pathParams`。
4. 保存认证、权限和响应定义。

重复 Endpoint 会抛出 `RouteAlreadyRegisteredError`；传入既不是 `BodyField` 也不是 `PathField` 的参数定义会抛出 `ValueError`。

## 4. 参数验证

请求进入 `_handleArguments()` 后，通过 `RouteManager.hasParameters()` 获取当前 Endpoint 的 Body / Path 参数定义。

### Body 参数

`validateBodyParameters()` 对每个定义执行：

1. 判断参数是否存在。
2. 检查 Python 类型。
3. 如果定义了 Validator，则执行 Validator。
4. 缺少必填参数时报错。
5. 缺少非必填参数时使用默认值。

验证成功后，最终参数保存到 `g.args`。

### Path 参数

`validatePathParameters()` 对 Flask 提供的 `request.view_args` 做类似处理。Path 参数没有可选项：定义了 PathField 就要求该参数存在并通过类型 / Validator 检查。

### 错误

验证失败时会收集：

```json
{
  "key": "字段名",
  "error": "ValidatorClassName",
  "msg": "错误消息"
}
```

最终返回全局 `ArgumentError`，HTTP 状态码为 `400`。

## 5. 认证信息

`getAuthConfig(endpoint)` 只暴露当前 Endpoint 的：

```json
{
  "requiresAuth": true,
  "isAdmin": false
}
```

`beforeRequest._handleAuth()` 使用这些信息决定是否需要检查 Token、是否需要管理员权限。

认证本身由 `UserService.checkToken()` 完成，Route Manager 不负责 Token 的业务逻辑。

## 6. 响应信息

`getResponseInfo(endpoint)` 返回该 Endpoint 注册的 `ResponseInfo` 列表。

请求上下文会据此创建 `ResponseGenerator`，最终可以通过：

```python
g.res.OK(data)
g.res.SomeBusinessError(data)
```

生成响应。

## 7. 为什么需要 RouteManager

当前设计把 Flask 的“路由”与应用的“API 元数据”分开：

```text
Flask
└── URL → View

RouteManager
└── Endpoint →
    ├── Auth
    ├── Permission
    ├── Parameters
    └── Responses
```

这样认证和参数验证可以在 View 执行前统一处理，而 View 不需要重复编写这些基础逻辑。

## 8. 新增 API 时的推荐写法

新增接口时优先完整声明 `requiresAuth`、`isAdmin`、`arguments` 和 `responses`。不要只注册 Flask Route 而跳过元数据，否则 `/api/` 请求在认证阶段可能因为找不到路由配置而直接返回 `NotFound`。

同时，`noRouteInfo=True` 会跳过 ForgeOrder 的路由元数据登记，只适合确实不需要认证、参数验证和统一响应元数据的特殊路由。
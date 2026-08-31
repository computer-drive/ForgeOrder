[返回文档首页](./index.md)

# 用户认证

ForgeOrder 的 API 使用基于 `Authorization` 请求头的 Token 认证机制。认证由后端路由层统一处理，业务视图只需要声明接口是否需要认证以及是否要求管理员权限。

## 认证流程

1. 客户端调用 `/api/auth/login`，提交用户名和密码。
2. 登录成功后，服务端返回登录信息，其中包含后续请求所需的认证信息。
3. 客户端在需要认证的请求中携带 `Authorization` 请求头。
4. 后端在进入具体视图函数前执行认证和权限检查。
5. Token 失效、过期或用户状态不允许访问时，请求会在进入业务逻辑前被拒绝。

当前登录接口定义如下：

```text
POST /api/auth/login
```

请求参数：

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `username` | `string` | 是 | 用户名，不能为空 |
| `password` | `string` | 是 | 密码，不能为空 |
| `cover` | `boolean` | 否 | 是否覆盖已有登录状态，默认 `false` |

当前登录相关业务状态包括：

| 状态码 | 状态 | 说明 |
| --- | --- | --- |
| `0` | `OK` | 登录成功 |
| `3001` | `UsernameOrPasswordError` | 用户名或密码错误 |
| `3002` | `UserIsDisabled` | 用户已被禁用 |
| `3003` | `RepeatLogin` | 检测到重复登录 |
| `3004` | `NewDeviceLogin` | 检测到新设备登录 |

## 请求头

需要认证的接口使用：

```http
Authorization: Bearer <token>
```

后端会在路由进入视图函数之前处理认证，因此业务接口通常不需要自行解析 Token。

## 路由权限声明

ForgeOrder 使用 `AppBlueprint` 注册 API 路由，并通过路由声明控制认证和管理员权限。例如：

```python
@blueprint.post(
    "/api/example",
    requiresAuth=True,
    isAdmin=True,
)
def example():
    ...
```

其中：

- `requiresAuth=True`：要求用户已经登录。
- `isAdmin=True`：除登录外，还要求管理员权限。
- `requiresAuth=False`：接口不要求登录，例如登录接口。

## 退出登录

退出登录接口：

```text
POST /api/auth/logout
```

该接口需要认证。服务端会根据 `Authorization` 中的 Token 注销当前登录状态。

如果 Token 无效，会返回 `3001 TokenInvalid`。

## 会话有效期

Token 的有效时间由配置项 `auth.available_time` 控制，默认值为 **60 分钟**。当前配置 Schema 中没有 `auth.secret_key` 配置项，因此旧版文档中关于通过配置文件设置 `secret_key` 的说明已经废弃。

## 多设备登录

当前登录接口会区分重复登录和新设备登录：

- **重复登录（`3003`）**：服务端检测到已有登录状态，需要客户端处理重复登录场景。
- **新设备登录（`3004`）**：服务端检测到来自新设备的登录，需要客户端根据返回信息决定是否覆盖原登录状态。

具体 Token 生命周期和设备判定属于后端内部实现；如果修改认证实现，应同步更新本文档和 API 文档。

## 安全建议

- 不要在日志、Issue 或公开文档中记录真实 Token。
- 生产环境应使用受信任的局域网环境，并合理限制服务端口的访问范围。
- 客户端应妥善保存认证信息，并在退出登录后清理本地会话状态。

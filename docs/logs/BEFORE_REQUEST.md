# BEFORE_REQUEST
本文档介绍了`class_name`为`BEFORE_REQUEST`时，各`method`的日志记录。


## 1. `DebugMsg`
- 级别：`DEBUG`
- 调试日志


## 2. `RouteNotRegistered`
- 级别：`WARNING`
- 该请求访问的路由未在`RouteMangaer`注册，本身不属于错误，但开发者可能使用错误的方法注册了路由，导致该错误。`msg`包含请求的路由路径。

## 3. `AuthError`
- 级别：`INFO`
- 认证错误，该日志可通过设置的`ignore_client_error`忽略。当用户因为认证失败导致请求失败时，该日志会被记录。`msg`包含请求的ip地址，及错误原因。
 - `InvalidToken`：无效的token。
 - `TokenExpire`：token已过期。
 - `TokenLogout`：该用户已经退出登录。
 - `OldDevice`：新设备登录后，旧设备已被下线。
 - `IPNotMatch`： 请求的ip地址与token中的ip地址不匹配。

## 4. `NonAdminUserAccess`
- 级别：`WARNING`
- 非管理员用户访问管理员路由，该日志会被记录。`msg`包含请求的ip地址，路由路径，请求用户的id。






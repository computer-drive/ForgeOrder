[返回](./index.md)

# 用户认证
本文档主要介绍前端、后端的用户认证的设计与实现。

## 用户认证设计
用户的用户名、密码存储在数据库中，用户登录时校验用户名、密码是否匹配。

登录成功后，后端使用SHA512算法，用配置文件中的`secret_key`生成一个Token并返回给前端，前端将Token保存至`localStorage`中，后端将Token存储在内存中。

在前端，所有请求的请求头中都包含`Authorization`字段，值为`Bearer ${token}`。后端收到请求，进入路由的视图函数前，校验`Authorization`中的Token是否有效。


## 后端认证设计

### 设置路由认证
后端认证主要通过[AppBlueprint](server/app_blueprint.md)及[RouteManager](server/route_manager.md)实现。

在注册路由时，需要添加`auth`及`is_admin`参数，参数均为`bool`类型。
`auth`参数用于指定路由是否需要用户认证。
`is_admin`参数用于指定路由是否需要管理员权限。
例如：
```python
@bp.get("/api/auth/test", auth=True, is_admin=False)
def test():
    ...
```

Flask注册路由时，AppBlueprint将把所有路由注册到RouteManager中。


### 生成Token
在登录请求中，若校验成功，后端将生成一个Token，Token由用户名、`secret_key`、当前的时间组合哈希得到。

### 校验Token
后端收到请求，进入路由的视图函数前，校验`Authorization`中的Token是否有效，对于任何无效的情况，都会阻止进入视图函数，返回401错误。

校验失败的情况有如下几种：
#### Token无效(InvalidToken)
请求中的Token在RouteManager中不存在。

#### Token过期(TokenExpired)
请求中的Token在RouteManager中存在，但已经超出了配置文件中的`auth.token_expire`时间。

在有效期内发送请求，Token将会更新过期时间。

#### 用户退出登录(TokenLogout)
请求中的Token在RouteManager中存在，但对应的用户已退出登录。

#### 旧设备登录(OldDevice)
请求中的Token在RouteManager中存在，但对应的用户已登录在其他设备上。
在接下来的部分，将会介绍“多设备互踢”机制的实现。

#### IP地址不匹配(IPNotMatch)
请求中的Token在RouteManager中存在，但对应的用户IP地址与请求IP地址不匹配。

### 多设备互踢机制
登录校验成功后，若发现当前用户已被其他设备登录，但IP相同，则会返回“重复登录”信息。若IP不同，将会返回一个“新设备登录”的信息，在前端，用户需要确认是否踢出其他设备的登录。
在用户确认前，旧设备的Token仍然有效。
用户确认后，旧设备的Token将被踢出RouteManager，用户需要重新登录。








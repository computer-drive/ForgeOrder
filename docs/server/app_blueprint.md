[返回](../index.md)

# AppBlueprint
AppBlueprint是ForgeOrder路由注册时所使用的蓝图，本身属于`flask.Blueprint`的子类。

AppBlueprint主要实现路由的注册，以及与其他功能对接，如参数验证、用户认证。

AppBlueprint的用法与`flask.Blueprint`大致相同，下面的文档，将着重描述AppBlueprint特有的方面。

## `route`方法
`route`方法相当于注册路由，与`flask.Blueprint.route`方法大致相同。

与`flask.Blueprint.route`方法不同的是，`route`方法在注册路由时，可添加`arguments`、`auth`、`is_admin`参数，用于参数验证、用户认证。


**与参数验证有关的部分，详见[Route Manager](args_verify.md) 。**

**与用户认证有关的部分，详见[Auth](../auth.md)。**

## `get`、`post`方法
这两个方法相当于对`route`方法的封装，分别对应`GET`、`POST`请求方法。

注意这两个方法不能实现允许多个方法的路由。同时使用本方法时候不要传入`methods`参数。





[返回文档首页](./index.md)

# API 设计

ForgeOrder 的 Web API 使用 HTTP + JSON，并以 `/api/` 作为统一前缀。

> 本文档描述当前代码中已经实现的 API 约定和主要接口。随着项目开发，具体接口参数和返回值可能继续变化。

## 基本约定

### URL

所有 Web API 路径均以 `/api/` 开头，例如：

```text
/api/auth/login
/api/shop/dishes/get
/api/order/new
```

接口名称采用 RPC 风格的小驼峰命名。对于操作型接口，项目约定优先使用 `new`、`update`、`delete`、`get` 等动词。

### 请求

需要提交参数时，参数通常放在 JSON 请求体中，而不是 URL 查询参数中。

请求体中的字段名称和类型必须与后端路由声明一致。参数验证失败时，请求会在进入业务逻辑前被拒绝。

需要认证的接口必须携带：

```http
Authorization: Bearer <token>
```

### 响应

ForgeOrder 使用统一响应对象，核心字段为：

```json
{
  "status": 0,
  "data": null
}
```

其中：

- `status`：本次请求的业务状态码；`0` 表示成功。
- `data`：成功结果或错误附加信息，具体结构由接口定义。

项目倾向于使用状态码表达机器可判断的业务状态，而不是依赖自然语言 `message`。

## 状态码

状态码通常按千位区分错误类别：

| 状态码范围 | 类型 | 说明 |
| --- | --- | --- |
| `0` | 成功 | 请求成功 |
| `1xxx` | 客户端错误 | 参数、HTTP 方法或请求本身的问题 |
| `2xxx` | 认证/授权错误 | 登录状态、Token 或权限问题 |
| `3xxx` | 业务错误 | 当前接口相关的业务逻辑错误 |
| `9xxx` | 系统错误 | 服务端、数据库或文件系统等系统级错误 |

### 常见通用错误

| 状态码 | HTTP | 说明 |
| --- | --- | --- |
| `1000` | `400` | 未知的客户端错误 |
| `1001` | `400` | 参数验证失败 |
| `1002` | `405` | HTTP 方法不正确 |
| `1003` | `404` | API 不存在 |
| `1004` | `429` | 请求频率过高 |
| `2001` | `401` | 用户未登录 |
| `2002` | `401` | 用户权限不足 |
| `2003` | `401` | Token 无效 |
| `2004` | `401` | Token 过期 |
| `2005` | `401` | 旧设备登录状态 |
| `9001` | `500` | 服务器内部错误 |
| `9002` | `500` | 数据库错误 |
| `9003` | `500` | 文件系统错误 |
| `9004` | `500` | 其他系统错误 |

> `3xxx` 通常用于接口自己的业务错误。例如订单和菜品接口都可能使用 `3001`，但其具体含义由对应接口决定。

## 当前接口概览

### 认证

| 方法 | 路径 | 认证 | 管理员 | 说明 |
| --- | --- | --- | --- | --- |
| `POST` | `/api/auth/login` | 否 | 否 | 用户登录 |
| `POST` | `/api/auth/logout` | 是 | 否 | 用户退出登录 |

`/api/auth/login` 参数：

```json
{
  "username": "admin",
  "password": "password",
  "cover": false
}
```

登录状态码：`0`、`3001`、`3002`、`3003`、`3004`。

### 店铺

当前代码包含以下主要店铺接口：

| 方法 | 路径 | 认证 | 管理员 | 说明 |
| --- | --- | --- | --- | --- |
| `GET` | `/api/shop/getBusinessState` | 是 | 否 | 获取营业状态 |
| `POST` | `/api/shop/setBusinessState` | 是 | 是 | 设置营业状态 |
| `GET` | `/api/shop/dishes/getAll` | 是 | 否 | 获取全部菜品及分类 |
| `POST` | `/api/shop/dishes/get` | 是 | 否 | 获取指定菜品 |
| `POST` | `/api/shop/dishes/new` | 是 | 是 | 新建菜品 |
| `POST` | `/api/shop/dishes/update` | 是 | 是 | 更新菜品 |
| `POST` | `/api/shop/dishes/delete` | 是 | 是 | 删除菜品 |
| `GET` | `/api/shop/category/getAll` | 是 | 否 | 获取全部分类 |
| `POST` | `/api/shop/category/new` | 是 | 是 | 新建分类 |
| `POST` | `/api/shop/category/update` | 是 | 是 | 更新分类 |
| `POST` | `/api/shop/category/delete` | 是 | 是 | 删除分类 |
| `GET` | `/api/shop/tables/getAll` | 是 | 否 | 获取全部桌台 |
| `POST` | `/api/shop/tables/get` | 是 | 否 | 获取指定桌台 |
| `POST` | `/api/shop/tables/new` | 是 | 是 | 新建桌台 |
| `POST` | `/api/shop/tables/update` | 是 | 是 | 更新桌台 |
| `POST` | `/api/shop/tables/delete` | 是 | 是 | 删除桌台 |

### 订单

当前代码包含以下主要订单接口：

| 方法 | 路径 | 认证 | 管理员 | 说明 |
| --- | --- | --- | --- | --- |
| `POST` | `/api/order/new` | 是 | 是 | 创建订单 |
| `POST` | `/api/order/getToday` | 是 | 否 | 分页获取今日订单 |
| `POST` | `/api/order/get` | 是 | 否 | 获取指定订单 |

创建订单的主要参数包括：

```json
{
  "orderType": 0,
  "partySize": 2,
  "tableId": 1,
  "dishes": [
    {
      "id": 1,
      "count": 1,
      "choices": {}
    }
  ],
  "note": ""
}
```

具体字段约束以及业务错误以 `server/app/views/orders.py` 中的路由声明为准。

## 参数验证

接口参数通过后端的声明式验证系统进行校验。例如：

```python
BodyField("username", str, True, None, NotEmpty())
```

表示 `username` 必须存在、类型为字符串且不能为空。

参数验证失败时通常返回 `1001`，并在 `data` 中提供验证结果。

示例：

```json
{
  "status": 1001,
  "data": {
    "username": "NOT_FOUND"
  }
}
```

更多验证机制见：[参数验证](server/args_verify.md) 和 [声明式数据验证](server/validation.md)。

## API 文档维护原则

接口实现与文档发生冲突时，应优先检查 `server/app/views/` 下对应的路由定义，并同步修正文档。

新增或修改 API 时，建议同时更新：

1. 本文档的接口概览；
2. 请求参数及响应示例；
3. 状态码说明；
4. 认证/管理员权限要求。

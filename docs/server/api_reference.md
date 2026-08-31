# 后端 API 参考

[返回文档首页](../index.md)

本文记录当前后端 API 的实际接口约定。API 路由主要位于 `server/app/views/`，当前至少包含认证、店铺管理和订单接口。

## 1. 通用约定

API 返回 JSON：

```json
{
  "status": 0,
  "data": null,
  "message": "OK"
}
```

其中：

- `status`：应用级状态码，不等同于 HTTP 状态码。
- `data`：业务数据；没有数据时通常为 `null`。
- `message`：状态名称。

响应由 `ResponseInfo` 和 `ResponseGenerator` 管理，路由在声明时列出允许返回的响应。fileciteturn50file0turn51file0

## 2. HTTP 状态码

当前请求前置处理主要使用：

| HTTP | 场景 |
| ---: | --- |
| `200` | 请求进入 View 并正常生成业务响应 |
| `400` | Body / Path 参数验证失败 |
| `401` | Token 无效、过期、旧设备或权限不足 |
| `404` | `/api/` 路径没有对应的路由元数据 |

业务成功/失败进一步由 JSON 中的 `status` 表示。认证和参数错误是在 View 执行前由 `beforeRequest` 处理的。fileciteturn47file0

## 3. 认证

需要认证的 API 必须提供：

```http
Authorization: Bearer <token>
```

Token 由 `/api/auth/login` 返回。请求进入后端后，`beforeRequest` 会验证 Token，并检查 Token 状态、过期时间和绑定 IP；管理员接口还会检查用户的 `isAdmin`。fileciteturn47file0turn61file0

## 4. 认证 API

### `POST /api/auth/login`

登录用户。

请求 Body：

```json
{
  "username": "root",
  "password": "password",
  "cover": false
}
```

字段：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `username` | string | 是 | 用户名 |
| `password` | string | 是 | 密码 |
| `cover` | boolean | 否 | 是否覆盖其他 IP 上的有效登录；默认 `false` |

成功时返回 Token 和用户信息。密码字段会从返回的用户对象中移除。fileciteturn23file0turn61file0

主要业务状态：

- `0 OK`
- `3001 UsernameOrPasswordError`
- `3002 UserIsDisabled`
- `3003 RepeatLogin`
- `3004 NewDeviceLogin`

`NewDeviceLogin` 表示当前 Token 仍绑定在其他 IP；只有 `cover=true` 才会覆盖旧 Token。fileciteturn23file0turn61file0

### `POST /api/auth/logout`

退出当前 Token。

请求头：

```http
Authorization: Bearer <token>
```

如果 Token 不存在，返回 `3001 TokenInvalid`。fileciteturn23file0

## 5. 店铺 API

店铺接口位于 `server/app/views/shop.py`。当前包含三类资源：店铺营业状态、菜品/分类、桌台。fileciteturn24file0

### 营业状态

| 方法 | 路径 | 权限 | 说明 |
| --- | --- | --- | --- |
| GET | `/api/shop/getBusinessState` | 登录 | 获取营业状态 |
| POST | `/api/shop/setBusinessState` | 管理员 | 修改营业状态 |

`setBusinessState` Body：

```json
{
  "isBusiness": true
}
```

配置实际保存为 `shop.isBusiness`。fileciteturn24file0

### 菜品

| 方法 | 路径 | 权限 | 说明 |
| --- | --- | --- | --- |
| GET | `/api/shop/dishes/getAll` | 登录 | 获取分类和全部可见菜品 |
| POST | `/api/shop/dishes/get` | 登录 | 获取单个菜品 |
| POST | `/api/shop/dishes/new` | 管理员 | 新建菜品 |
| POST | `/api/shop/dishes/update` | 管理员 | 更新菜品 |
| POST | `/api/shop/dishes/delete` | 管理员 | 删除菜品 |

新建菜品 Body：

```json
{
  "name": "示例菜品",
  "price": 1000,
  "category": 1,
  "description": "",
  "image": "",
  "isAvailable": true,
  "choices": {}
}
```

`price` 必须大于 `0`；`choices` 用于定义菜品选项。菜品删除采用软删除策略。fileciteturn24file0turn59file0

更新菜品 Body：

```json
{
  "dishId": 1,
  "changedItems": {
    "name": "新名称"
  },
  "changedChoices": []
}
```

`changedChoices` 当前支持 `new_choice`、`delete_choice`、`new_option`、`delete_option` 四类操作；相互抵消的新增/删除操作会被消除。fileciteturn24file0turn59file0

### 分类

| 方法 | 路径 | 权限 | 说明 |
| --- | --- | --- | --- |
| GET | `/api/shop/category/getAll` | 登录 | 获取分类 |
| POST | `/api/shop/category/new` | 管理员 | 新建分类 |
| POST | `/api/shop/category/update` | 管理员 | 修改分类名称 |
| POST | `/api/shop/category/delete` | 管理员 | 删除分类及其菜品 |

### 桌台

| 方法 | 路径 | 权限 | 说明 |
| --- | --- | --- | --- |
| GET | `/api/shop/tables/getAll` | 登录 | 获取桌台 |
| POST | `/api/shop/tables/get` | 登录 | 获取单个桌台 |
| POST | `/api/shop/tables/new` | 管理员 | 新建桌台 |
| POST | `/api/shop/tables/update` | 管理员 | 修改桌台名称 |
| POST | `/api/shop/tables/delete` | 管理员 | 删除桌台 |

桌台创建后默认 `isAvailable=true`。桌台名称需要满足唯一性约束。fileciteturn24file0turn59file0

## 6. 订单 API

订单接口位于 `server/app/views/orders.py`，当前包含创建订单、获取今日订单和按 ID 获取订单。fileciteturn45file0

### `POST /api/order/new`

需要登录和管理员权限。

请求 Body：

```json
{
  "orderType": 0,
  "partySize": 2,
  "tableId": 1,
  "dishes": [
    {
      "id": 10,
      "count": 2,
      "choices": {}
    }
  ],
  "note": ""
}
```

字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `orderType` | int | `0` 堂食，`1` 打包 |
| `partySize` | int | 用餐人数，必须大于 `0` |
| `tableId` | int | 堂食桌台 ID；打包订单最终不保存桌台 |
| `dishes` | array | 至少包含一个菜品 |
| `dishes[].id` | int | 菜品 ID |
| `dishes[].count` | int | 数量，必须大于 `0` |
| `dishes[].choices` | object | 菜品选项 |
| `note` | string | 备注 |

创建时后端会重新读取菜品价格，不信任客户端传入的金额；同时验证菜品是否存在、是否可售，以及每个选项和选项值是否存在。fileciteturn46file0

成功返回的数据为：

```json
{
  "status": 0,
  "data": ["<order-id>", 1],
  "message": "OK"
}
```

当前主要错误：

| 状态码 | 名称 |
| ---: | --- |
| `3011` | `TableNotFound` |
| `3012` | `TableNotAvailable` |
| `3021` | `DishNotFound` |
| `3022` | `DishNotAvailable` |
| `3023` | `DishChoiceNotFound` |
| `3024` | `DishChoiceOptionNotFound` |
| `3031` | `OrderAlreadyExist` |
| `3999` | `UnknownError` |

注意：`OrderService` 当前还定义了 `INVALID_ORDER_TYPE`、`INVALID_PARTY_SIZE`、`CREATOR_NOT_FOUND`、`DISH_COUNT_NOT_AVAILABLE` 等结果，但 `orders.py` 的路由层没有将这些结果逐一映射成独立的 `ResponseInfo`。新增错误处理时应同步补齐这一层。fileciteturn46file0turn45file0

### `POST /api/order/getToday`

获取当天订单。

请求 Body：

```json
{
  "offset": 0,
  "limit": 10
}
```

两个参数均可省略，默认 `offset=0`、`limit=10`，且不能小于 `0`。返回结果分为：

```json
{
  "unfinished": [],
  "finished": []
}
```

当前实现将 `status != 3` 的订单放入 `unfinished`，`status == 3` 的订单放入 `finished`。fileciteturn45file0turn46file0

### `POST /api/order/get`

按订单 ID 获取指定信息。

请求 Body：

```json
{
  "id": "<order-id>",
  "queries": [
    "basicInfo",
    "tableName",
    "subOrdersCount",
    "dishesCount"
  ]
}
```

`queries` 当前允许：

- `tableName`：桌台名称。
- `subOrdersCount`：已完成 / 总子订单数。
- `dishesCount`：已完成 / 总菜品项数。
- `basicInfo`：订单基本信息和订单状态信息。

接口允许返回 `PartialError`，因为部分查询可以失败而其他查询仍成功。例如打包订单没有桌台信息时，`tableName` 会记录 `NoTableInfo`。fileciteturn45file0turn46file0

## 7. 全局状态码

当前全局状态码定义如下：

| 状态码 | 名称 | 用途 |
| ---: | --- | --- |
| `1001` | `ArgumentError` | 参数验证失败 |
| `1002` | `MethodError` | HTTP 方法错误 |
| `1003` | `NotFound` | 资源不存在 |
| `1004` | `PayloadError` | 请求体类型错误 |
| `2001` | `NotLoginError` | 未登录 |
| `2002` | `PermissionError` | 权限不足 |
| `2003` | `TokenInvalidError` | Token 无效 |
| `2004` | `TokenExpiredError` | Token 过期 |
| `2005` | `OldDeviceToken` | 旧设备 Token |
| `9010` | `ServerError` | 服务端错误 |
| `9020` | `DatabaseError` | 数据库错误 |
| `9021` | `DatabaseBusy` | 数据库繁忙 |

定义来源为 `app.routes.schema.GLOBAL`。fileciteturn66file0
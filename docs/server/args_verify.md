# 请求参数验证

[返回文档首页](../index.md)

ForgeOrder 的参数验证已经从早期的 `ArgRule` 方案演进为 `BodyField` / `PathField` + Validator。新增 API 时应以当前 `app.routes.field` 和 `core.validation` 实现为准。

## 1. BodyField

`BodyField` 用于 JSON Body 参数：

```python
BodyField(
    key="username",
    valueType=str,
    required=True,
    default=None,
    validator=NotEmpty(),
)
```

参数：

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `key` | string | 参数名 |
| `valueType` | type | 参数的 Python 类型 |
| `required` | bool | 是否必填 |
| `default` | any | 非必填参数的默认值 |
| `validator` | Validator / None | 额外校验规则 |

非必填字段必须提供默认值；否则 `BodyField` 初始化时会抛出 `ValueError`。

## 2. PathField

`PathField` 用于 URL 路径参数：

```python
PathField(
    key="id",
    valueType=int,
    validator=Interval(1, None),
)
```

Path 参数没有 `required` / `default` 选项；一旦定义，路由参数就必须存在。

## 3. 验证顺序

请求进入 `beforeRequest` 后，RouteManager 根据当前 Endpoint 的元数据执行参数验证：

```text
读取 Body / Path
      ↓
类型检查
      ↓
Validator.validate()
      ↓
生成最终参数
      ↓
g.args
```

Body 参数缺失时：

- 必填：生成 `MissingRequiredParameterError`。
- 非必填：写入声明的 `default`。

参数存在但类型不匹配时，生成 `ParameterTypeError`。

Validator 失败时，生成 `ParameterValidationError` 或对应 Path 参数错误。

## 4. Validator

项目的通用 Validator 位于 `core/validation/validators/`。当前包含多种组合式验证器，例如：

- `NotEmpty`：非空。
- `Choices`：值必须属于给定选项。
- `Interval`：数值区间。
- `Length`：长度约束。
- `ListOf`：列表元素验证。
- `DictOf`：字典结构验证。
- `ForEach`：对集合中的每个元素应用验证。
- `AllOf` / `AnyOf` / `Not`：逻辑组合。
- `TypeOf`：类型相关验证。

Validator 的设计允许在路由声明处直接表达复杂的请求结构。例如订单创建接口可以表达“数组非空，并且每个元素都必须是包含 `id`、`count`、`choices` 的字典”。

## 5. 验证失败响应

参数验证在 View 执行之前完成。失败时后端返回：

```http
HTTP/1.1 400 Bad Request
```

并使用全局 `ArgumentError` 响应。

错误数据由多个字段组成：

```json
[
  {
    "key": "username",
    "error": "NotEmptyError",
    "msg": "..."
  }
]
```

具体 `error` 名称和 `msg` 来自实际 Validator / Error 类，不应该在业务文档中假设固定文本。

## 6. 与 RouteManager 的关系

参数规则不是独立存在的，而是注册到 RouteManager 的 Endpoint 元数据中：

```text
AppBlueprint
   ↓
RouteManager.register()
   ↓
bodyParams / pathParams
   ↓
beforeRequest._handleArguments()
   ↓
g.args
```

因此新增 API 时，应优先在 `arguments` 中声明规则，而不是在 View 函数内部重复检查必填字段和类型。

## 7. 注意事项

当前实现的类型检查使用 Python 的 `isinstance()`。这意味着 API 文档中的类型应使用 Python / JSON 的实际映射来描述，例如 `int`、`str`、`bool`、`list`、`dict`。

另外，当前 `RouteManager` 在类型检查失败后仍可能继续执行后续 Validator；新增复杂 Validator 时应考虑错误聚合行为，不要假设一次请求只会产生一个错误。
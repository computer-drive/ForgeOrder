# 声明式数据验证

[返回文档首页](../index.md)

ForgeOrder 的 `core.validation` 是一个可组合的声明式验证框架，目前用于配置项、请求参数和其他业务输入的规则检查。

## 1. 核心概念

验证器实现 `Validator` 接口，通过 `validate(value)` 返回 `ValidationResult`。结果包含：

- `success`：是否通过。
- `error`：失败时的 `ValidationError`。

验证失败的信息是“错误对象”，不是必须通过异常抛出的流程。

## 2. FieldDefinition

`core.validation.field.FieldDefinition` 用于描述一个值的字段定义：

```python
FieldDefinition(
    key="server.port",
    valueType=int,
    default=5000,
    validator=Interval(1, 65535),
)
```

它负责：

1. 保存字段名。
2. 声明 Python 类型。
3. 提供默认值。
4. 可选地绑定 Validator。
5. 在调用 `validate()` 时先做类型检查，再运行 Validator。

应用配置 `CONFIG_ITEMS` 就采用了这种模式。

## 3. 请求参数验证

HTTP 层在此基础上提供：

- `BodyField`：JSON Body 参数。
- `PathField`：URL Path 参数。

它们继承自 `RequestParameterField`。BodyField 额外声明 `required` 和非必填字段的 `default`；PathField 不提供可选参数语义。

详见[请求参数验证](args_verify.md)。

## 4. 基础验证器

当前代码中常用的验证器包括：

### `NotEmpty`

拒绝空字符串、空字典、空列表和 `None`。

### `Choices`

限制值必须属于给定集合：

```python
Choices("dev", "product")
```

### `Interval`

限制数字范围，并支持开区间 / 闭区间：

```python
Interval(1, 65535)
Interval(Open(0), None)
```

### `Length`

对字符串长度进行范围限制。

### `ListOf` / `DictOf`

用于描述集合元素或字典字段的结构。

### `ForEach`

对集合中的每个元素应用验证器。

### `TypeOf`

用于类型相关的验证场景。

## 5. 组合验证器

验证器可以继续组合，从而表达复杂规则：

```python
AllOf(
    NotEmpty(),
    Length(4, 10),
)
```

常用逻辑组合：

- `AllOf`：全部规则通过。
- `AnyOf`：至少一个规则通过。
- `Not`：反转规则结果。

项目还提供基于逻辑表达式的其他组合能力；使用前应查看 `core.validation.validators` 当前实现，而不要依赖早期文档中的模块路径。

## 6. `bind`

Validator 可以通过 `bind()` 指定验证值的来源：

```python
AllOf(
    NotEmpty().bind(value_a),
    NotEmpty().bind(value_b),
)
```

这使多个字段可以在同一个验证表达式中参与判断，而不必都使用 `validate()` 的直接输入。

## 7. 验证上下文

部分验证器支持从上下文或计算函数中取得值。项目中存在 Value Provider 机制，用于表达延迟读取的值。

在需要依赖运行时数据的验证规则中，应优先使用项目已有的 Provider / `bind` 机制，而不是把数据库查询直接塞进 Validator。

## 8. 路由中的典型用法

订单创建接口使用组合 Validator 描述嵌套结构，例如：

```python
AllOf(
    NotEmpty(),
    ForEach(
        DictOf()
            .Field("id", int, True)
            .Field("count", int, True, Interval(1, None))
            .Field("choices", dict, True)
    )
)
```

这样 View 层不需要手工逐层检查 `dishes` 的类型和字段是否存在。

## 9. 新增 Validator

当现有规则不足时，可以继承 `Validator` 实现新的验证器。新验证器应：

- 明确支持的输入类型。
- 返回标准 `ValidationResult`。
- 提供稳定的错误类型 / 消息。
- 避免执行有副作用的业务操作。
- 在适当的模块中导出，使路由和配置可以直接使用。

旧版文档曾建议使用 `FunctionHandler`；当前实现中应优先使用正式 Validator 类，避免继续扩大旧 API 的依赖。

## 10. 与 HTTP 层的边界

验证框架负责“值是否满足规则”，HTTP 层负责“请求中的值从哪里来以及验证失败后如何返回 HTTP 响应”。

```text
JSON / Path
    ↓
BodyField / PathField
    ↓
FieldDefinition
    ↓
Validator
    ↓
ValidationResult
    ↓
RouteManager
    ↓
ArgumentError (HTTP 400)
```

这种边界可以让同一套 Validator 同时用于配置和 API 参数。
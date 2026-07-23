[返回](../index.md)

# 设置项验证
配置文件、AppSettings中的设置项在系统启动前都进行验证，验证的逻辑主要通过`SettingsProperty`和`VerifyHandler`实现。

## SettingsProperty
设置项都定义了一份注册表，`SettingsProperty`是一项设置的注册信息。在注册时，需要包含如下参数：
- `key`：`str`类型，设置项的键名；
- `value_type`：`type`类型，设置项的值类型；
- `default`：设置项的默认值，类型应为`value_type`；
- `verify`：`VerifyHandler`类型，验证值的逻辑。

## VerifyHandler
`VerifyHandler`是验证设置项是否有效的条件。不同的`VerifyHandler`有其可以接受的类型。

其本身实现一个`verify`方法，该方法接受一个参数，传入设置项的值，返回一个`VerifyResult`对象。（将在下面的文档中说明）

在`verify`方法内部，先判断传入的值的类型是否能被这个`VerifyHandler`处理。若可处理，将调用`_verify`函数，进行具体的验证逻辑；反之，将会抛出异常`UnsupportedTypeError`。
**`UnsupportedTypeError`并不是用户的错误，而是开发者错误使用了类型错误的`VerifyHandler`。**

`_verify`方法返回一个`VerifyResult`对象。

### VerifyResult
`VerifyResult`是验证设置项的结果，其包含三个属性：
- `success`：`bool`类型，验证是否成功；
- `error`：`VerifyError`类型或`None`，验证失败时的错误。
- `can_fix`：`bool`类型，若验证失败，是否可以修复。

### VerifyError
`VerifyError`是验证失败时的错误信息，其本身没有属性其子类可能拥有其其他属性。

`VerifyError`用于描述错误原因，并不继承于`Exception`类。


### 基础验证器
系统内部实现了多个`VerifyHandler`，接下来将对它们进行详细介绍：

#### 基本类型验证器
##### NotEmpty
- 允许的类型：`str | list | dict | None`
- 限制值不能为`None`，不能为空字符串，不能为空列表、字典。
- 错误类型：`EmptyError`d

##### Interval
- 允许的类型：`int | float`
- 限制值在一个区间内。
- 需要传递两个参数，表示最小值`min`和最大值`value`，允许`Boundary`对象。
- 建议调用`Open`和`Closed`工厂函数表示区间的端点。其中，`Open`表示开区间，`Closed`表示闭区间。
- `Interval`允许`int | float`类型的参数作为语法糖，传入的值作为开区间，`int | float`类型与`Boundary`允许混用。
- 若传入`None`则表示无限制。
- 错误类型：`IntervalError`，内部包含`Interval`对象
- 例子：
```python
Interval(1, 8)                 # 表示：(1,8)
Interval(Open(1), Open(8))     # 表示：(1,8)
Interval(Open(1), Closed(8))   # 表示：(1,8]
Interval(Closed(1), Open(8))   # 表示：[1,8)
Interval(Closed(1), Closed(8)) # 表示：[1,8]
Interval(Closed(1), None)      # 表示：[1,+∞)
Interval(None, Open(1))        # 表示:(-∞,1)
Interval(Closed(1), 8)         # 表示：[1,8)
```

##### Length
- 允许的类型：`str | list | dict`
- 限制值长度在指定范围内。
- 需要传递两个参数，表示最小长度`min`和最大长度`max`，允许`int`类型。
- 错误类型：`LengthError`，包含最小长度和最大长度的值。

##### Choices
- 允许的类型：`Any`
- 限制值只能是指定的选项。
- 传递选项的列表，支持可变长参数。
- 错误类型：`ChoicesError`，包含选项的列表。

#### 自定义验证器
##### FunctionHandler
- 允许的类型：Any
- 允许传入一个函数，用于自定义验证逻辑。
- 传入的函数需要接受一个参数，传入设置项的值，返回一个`VerifyResult`对象。
- 若返回值的类型不是`VerifyResult`，会抛出`UnsupportedVerifyHandlerError`异常，

**已有的验证器无法满足需求时，才建议使用`FunctionHandler`。**
**`FunctionHandler`没有默认的错误类型，开发者需自己继承`VerifyError`类。**
**`FunctionHandler`默认支持所有的类型的值验证，若需要对值进行类型验证，应自己继承`VerifyHandler`类重写`_verify`方法，使用`allow_type`属性进行类型验证。**


#### 逻辑组合验证器
##### AnyOf
- 允许的类型：Any
- 传入多个`VerifyHandler`，值任意通过其中一个即可。
- 错误类型：`AnyOfError`，其`children`属性包括所有验证失败的错误。

##### AllOf
- 允许的类型：Any
- 传入多个`VerifyHandler`，值必须通过所有验证。
- 错误类型：`AllOfError`，其`children`属性包括所有验证失败的错误。
- 在验证时，若一个`VerifyHandler`验证失败，不会立即返回错误，而是继续验证下一个`VerifyHandler`，直到完成验证。

### 复杂的验证逻辑
通过对以上验证器的组合，可以实现复杂的验证逻辑。例如：
> 限制值必须满足验证器A和B，或满足验证器C或D。
> 验证器的逻辑可以是：
> ```python
> AnyOf(AllOf(A, B), C, D)
> ```

在上面的例子中，`AnyOf(AllOf(A, B), AnyOf(C, D))`实际上也满足验证逻辑，但开发时应避免嵌套验证器，使错误信息更可读。




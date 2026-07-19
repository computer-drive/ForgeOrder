[返回](../index.md)

# 参数验证
参数验证是指验证每个请求的请求体中的参数是否符合要求。


## 注册参数验证

注册参数验证的方案需要在路由被注册时使用`AppBlueprint.route`方法，并传递`arguments`参数，参数的类型为`list[ArgRule]`，`ArgRule`本质是一个`TypedDict`，应包含以下字段：
 
 - `name`：参数名，`str`类型，必填项。
 - `type`：该参数允许的类型，`type`类型，必填项。
 - `required`：这个参数是否是必须的，`bool`类型，必填项。
 - `default`：参数的默认值，可选项。

## 参数验证
对于任何如下的情况，都将使验证失败：
 - 必填参数未提供。
 - 参数类型错误。

请注意，应确保`default`项的类型与`type`项的类型一致。在代码中，若已提供`default`，将不会判断类型是否与`type`一致。

`default`只应在`required`项的值为`False`时出现，当`required`为`True`时，任何情况下不会使用`default`项中的值。

# 前端文本

## 文案的存储
所有文案存储在`/src/locales/`下的`*.jsonc`文件中。

不同的文件名代表不同模块、功能所使用的文案。

目前，有以下文件：
 - `pages.jsonc`：各页面中出现的文本所用的文案。
 - `components.jsonc`：各组件中出现的文本所用的文案。
 - `utils.jsonc`：各工具函数中出现的文本所用的文案。

## `t`函数
在前端，所有出现的文本都应使用`/src/locales/index.js`中的`t`函数获取。若在模板中，可用Vue的全局对象`$t`。

在其他地方，若需获取文本，需要从`/src/locales/index.js`中导入`t`函数。

`t`函数应传递两个变量：
 - `key`：文案的键名，字符串，用`.`分隔，例如：`common.text.confirm`
 - `params`：参数对象，用于替换文案中的占位符，例如：`{name}`，`{age}`等。

对于不存在的键名，将返回键名本身，同时在控制台输出警告信息。

需要注意的是，在读取非`pages.jsonc`文件时，需在键名的第一位添加前缀。例如读取`components.jsonc`中的`bottombar.text.main`时，应使用`t('Ubottombar.text.main')`，


## 文案参数与引用
在`*.jsonc`文件中，文案的占位符以`{}`包裹，内为参数名。

若参数名以`$`开头，则被认为要引用文案。例如：`总金额：{$common.cny_char}{price}`，这将使用`common.cny_char`中的文案替换`{$common.cny_char}`。

若想让整体被引用，则可让文案只为一个带`$`的参数，例如：`{$common.cny_char}`。

## `locale`函数
`locale`函数是另一种使用`t`函数的方式。在`locale`函数中，只有当键名以`$`开头时，才会被认为是一个文案，将会调用`t`函数获取文案。否则将返回一个普通字符串。`locale`函数同样支持`params`参数。





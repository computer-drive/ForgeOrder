# LOGIN_REQUEST
本文档介绍了`class_name`为`LOGIN_REQUEST`时，各`method`的日志记录。

## 1. `DebugMsg`
- 级别：`DEBUG`
- 调试日志。

## 2. `UserLogin`
- 级别：`INFO`
- 用户登录成功，该日志会被记录。`msg`包含请求的ip地址，用户id。

## 3. `UserLogout`
- 级别：`INFO`
- 用户退出登录，该日志会被记录。`msg`包含请求的ip地址，用户id。

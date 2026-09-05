[返回 README](../../README.md) · [文档首页](../index.md)

# 使用构建版本运行

本文介绍如何在 Windows 环境下运行 ForgeOrder 的 Release 构建版本。

> 当前 Release 文档只覆盖 Windows。Linux 环境尚未经过充分验证。

## 1. 下载 Release

前往项目 GitHub Releases 页面，下载最新的 Windows 构建包。

## 2. 解压

将下载的 `.zip` 文件解压到一个目录中。

建议不要把程序放在需要管理员权限才能写入的目录中，因为 ForgeOrder 运行时需要创建和修改运行数据。

## 3. 启动服务器

进入解压后的 `server` 目录，在文件资源管理器地址栏输入 `cmd` 或 PowerShell，打开终端。

运行：

```cmd
app.exe
```

程序会根据配置启动 HTTP 服务。默认地址为：

```text
http://127.0.0.1:5000
```

如果需要让局域网内其他设备访问，请确认服务器监听地址和 Windows 防火墙规则允许相应端口的访问。

## 4. 配置

首次启动后，可以根据需要调整：

```text
server/data/config.json
```

常用配置包括：

- `server.host`：监听地址
- `server.port`：监听端口
- `server.env`：运行环境
- `database.path`：主数据库路径
- `log.level`：日志等级
- `auth.available_time`：认证 Token 有效时间

完整配置说明见：[配置文件](../server/config.md)。

## 5. 停止服务

在运行 `app.exe` 的终端中按 `Ctrl+C` 停止服务。

## 故障排查

### 端口无法访问

检查 `server.port` 是否被其他程序占用，并确认防火墙是否允许该端口。

### 程序启动后立即退出

请从终端直接运行 `app.exe`，查看控制台输出的错误信息，而不是双击后忽略窗口内容。

### 浏览器无法打开页面

确认服务已经成功启动，并检查前端资源是否包含在当前 Release 构建包中。

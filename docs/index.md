# ForgeOrder 文档

欢迎来到 ForgeOrder 文档。

ForgeOrder 是一个运行在局域网环境中的轻量级在线点单系统。本目录同时包含**使用文档**和**开发文档**；如果你只是想把项目运行起来，建议从“快速开始”开始阅读。

## 快速开始

| 文档 | 说明 |
| --- | --- |
| [源码运行](quick_start/source.md) | 从 Git 仓库安装依赖并运行项目 |
| [构建版本运行](quick_start/release.md) | Windows 用户使用 Release 构建版本 |

## 使用与运维

| 文档 | 说明 |
| --- | --- |
| [配置文件](server/config.md) | 服务地址、端口、日志、数据库和认证相关配置 |
| [日志](server/logs.md) | 日志系统及日志配置说明 |
| [用户认证](auth.md) | 登录、Token、权限和会话机制 |
| [API 设计](api.md) | HTTP API 的请求、响应和状态码约定 |

## 后端开发

| 文档 | 说明 |
| --- | --- |
| [服务器](server/server.md) | 后端启动流程及服务结构 |
| [AppBlueprint](server/app_blueprint.md) | API Blueprint 的注册方式 |
| [Route Manager](server/route_manager.md) | 路由管理机制 |
| [参数验证](server/args_verify.md) | API 请求参数验证 |
| [声明式数据验证](server/validation.md) | 后端通用验证框架 |

## 前端开发

| 文档 | 说明 |
| --- | --- |
| [Web API / 本地化](web_locales.md) | 前端本地化相关说明 |

## 设计文档

- [订单设计](order_design.md)

## 文档说明

文档会随着项目代码一起维护。对于代码与旧文档存在冲突的情况，应以当前代码为准，并优先修正文档中的过时内容。

项目目前仍处于开发阶段，接口和内部实现可能发生变化。

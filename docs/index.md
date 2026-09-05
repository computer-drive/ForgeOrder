# ForgeOrder 文档

欢迎来到 ForgeOrder 文档。

ForgeOrder 是一个运行在局域网环境中的轻量级在线点单系统。本目录同时包含使用文档和开发文档。

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
| [API 设计](api.md) | HTTP API 的总体约定 |
| [API 参考](server/api_reference.md) | 当前已实现 API 的接口、参数和错误码 |

## 后端架构

如果你准备修改后端，建议按下面的顺序阅读：

1. [后端架构](server/architecture.md) — 了解从 HTTP 请求到 Service / Repository 的整体链路。
2. [服务器](server/server.md) — 了解启动和运行模式。
3. [Route Manager](server/route_manager.md) — 了解 API 元数据、认证和参数验证如何接入路由。
4. [请求参数验证](server/args_verify.md) — 了解 BodyField / PathField。
5. [声明式数据验证](server/validation.md) — 了解 Validator 组合机制。
6. [数据库与 Repository](server/database.md) — 了解数据访问、事务和订单表结构。
7. [AppBlueprint](server/app_blueprint.md) — 了解 API 路由声明方式。

## 后端 API

- [API 参考](server/api_reference.md)
- [用户认证](auth.md)
- [订单设计](order_design.md)

## 前端开发

- [Web API / 本地化](web_locales.md) — 前端本地化相关说明。

## 文档说明

文档会随着项目代码一起维护。对于代码与旧文档存在冲突的情况，应以当前代码为准，并优先修正文档中的过时内容。

项目目前仍处于开发阶段，接口和内部实现可能发生变化。
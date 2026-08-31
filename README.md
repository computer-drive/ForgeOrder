# ForgeOrder

ForgeOrder 是一个运行在局域网环境中的轻量级在线点单系统，面向餐厅、小吃店、奶茶店等小型商户。

项目提供顾客点单、订单管理以及店铺后台管理等基础能力，并支持菜品、分类、桌台和营业状态等店铺数据的管理。项目目前仍处于开发阶段，适合学习、测试以及小规模局域网场景使用。

> **项目状态**：开发中
>
> 当前主要在 Windows 环境下开发和验证，Linux 环境尚未经过充分测试。

## 功能概览

- 顾客在线点单
- 订单创建与查询
- 菜品、菜品分类管理
- 桌台管理
- 店铺营业状态管理
- 用户登录、登出及管理员权限控制
- SQLite 数据存储
- 日志记录
- 可选的票据打印支持
- 前端与后端分离的 Web 架构

## 技术栈

### 前端

- Vue 3
- Vue Router 5
- Axios
- VueUse
- Vite
- mdui 2

### 后端

- Python 3.14+
- Flask 3
- Waitress（生产环境 HTTP 服务）
- SQLite
- Poetry
- python-escpos（打印机支持）
- Nuitka（构建）

## 环境要求

源码运行至少需要：

- Python >= 3.14
- Poetry 2.x
- Node.js / npm
- Git

具体依赖版本以 `server/pyproject.toml` 和 `web/package.json` 为准。

## 快速开始

### 从源码运行

```bash
git clone https://github.com/computer-drive/ForgeOrder.git
cd ForgeOrder
```

安装后端依赖：

```bash
cd server
poetry install
```

安装前端依赖并构建：

```bash
cd ../web
npm install
npm run build
```

启动后端：

```bash
cd ../server
poetry run python run.py
```

默认情况下服务监听 `0.0.0.0:5000`。配置项可以通过 `server/data/config.json` 调整。

> 当前仓库中的源码入口是 `server/run.py`。如果你看到旧文档或脚本仍使用 `app.py`，请以 `run.py` 为准。

更完整的说明见：[源码运行](docs/quick_start/source.md)。

### 使用 Release

Windows 用户可以直接使用 Release 中提供的构建版本，无需安装 Python 和 Node.js。

1. 从 GitHub Releases 下载最新构建包。
2. 解压到本地目录。
3. 进入 `server` 目录运行 `app.exe`。

详见：[构建版本运行](docs/quick_start/release.md)。

## 项目结构

```text
ForgeOrder/
├── docs/                  # 项目文档
├── scripts/               # 开发辅助脚本
├── server/                # Python 后端
│   ├── app/               # ForgeOrder 业务层
│   │   ├── config/        # 应用配置
│   │   ├── db/            # 数据库相关代码
│   │   ├── models/        # 数据模型
│   │   ├── routes/        # 路由及请求处理基础设施
│   │   ├── service/       # 业务服务
│   │   ├── views/         # API 接口
│   │   └── ...
│   ├── core/              # 通用基础设施
│   ├── run.py             # 后端启动入口
│   ├── pyproject.toml     # Python 项目配置
│   └── poetry.lock        # Python 依赖锁定文件
└── web/                   # Vue 前端
    ├── public/
    ├── src/
    │   ├── assets/
    │   ├── components/
    │   ├── composables/
    │   ├── locales/
    │   ├── utils/
    │   └── views/
    └── package.json
```

其中 `server` 负责 HTTP API、业务逻辑、认证、数据库和打印等功能；`web` 负责浏览器端界面。

## 文档

- [文档首页](docs/index.md)
- [快速开始](docs/quick_start/source.md)
- [配置文件](docs/server/config.md)
- [API 设计](docs/api.md)
- [用户认证](docs/auth.md)
- [后端架构说明](docs/server/server.md)
- [日志](docs/server/logs.md)
- [数据验证](docs/server/validation.md)

## 开发

Windows 环境下可以使用仓库根目录的 `debug.cmd` 同时启动开发服务。

如果只需要启动后端，可参考 `scripts/debug_server.cmd`；前端开发服务可参考 `scripts/debug_web.cmd`。

构建前端静态文件可以运行：

```cmd
build.cmd
```

## 已知限制

- 项目仍处于开发阶段，接口和数据结构可能发生变化。
- Linux 环境尚未经过充分验证。
- 部分 API 文档仍在持续完善中。
- 当前认证状态依赖服务端内存，服务重启后已有登录状态不会保留。

## Todo

- [ ] Server：完善所有接口的详细日志输出
- [ ] Server：完善配置项验证器的扩展能力
- [ ] Server：完善类型转换器的扩展支持
- [ ] Web：统一响应状态码处理
- [ ] API：补充完整的接口参数、响应及示例

## License

本项目使用 [MIT License](LICENSE)。

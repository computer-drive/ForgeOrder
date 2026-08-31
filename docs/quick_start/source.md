[返回 README](../../README.md) · [文档首页](../index.md)

# 从源码运行

本文介绍如何在开发环境中从源码运行 ForgeOrder。

## 环境要求

- Git
- Python >= 3.14
- Poetry 2.x
- Node.js / npm

后端依赖和版本范围以 `server/pyproject.toml` 为准，前端依赖以 `web/package.json` 为准。

## 1. 获取源码

```bash
git clone https://github.com/computer-drive/ForgeOrder.git
cd ForgeOrder
```

## 2. 安装后端依赖

进入 `server` 目录：

```bash
cd server
poetry install
```

Poetry 会根据项目配置和锁定文件安装后端依赖。

## 3. 安装并构建前端

进入 `web` 目录：

```bash
cd ../web
npm install
npm run build
```

构建后的前端资源会由 Vite 输出到项目配置指定的位置；请以当前 Vite 配置为准，不要手动假定输出目录。

## 4. 启动后端

进入 `server` 目录：

```bash
cd ../server
poetry run python run.py
```

后端启动入口是 `server/run.py`。开发环境下使用 Flask 自带的开发服务器；当配置中的 `server.env` 为 `product` 时，后端会使用 Waitress 提供 HTTP 服务。

默认监听：

```text
0.0.0.0:5000
```

可以通过 `data/config.json` 修改监听地址和端口。首次运行时，如果 `data` 目录或配置文件尚不存在，应用会根据当前配置初始化运行环境。

## 5. 开发模式

Windows 环境下，可以直接运行仓库根目录的：

```cmd
debug.cmd
```

该脚本会分别启动后端和前端开发服务。也可以单独使用 `scripts/debug_server.cmd` 或 `scripts/debug_web.cmd`。

## 常见问题

### 为什么旧文档写的是 `app.py`？

当前仓库的后端入口已经是 `server/run.py`。旧版文档或脚本中出现的 `app.py` 属于过时内容，运行源码时请使用 `run.py`。

### 配置文件在哪里？

默认配置路径为后端工作目录下的：

```text
data/config.json
```

配置项说明见：[配置文件](../server/config.md)。

### 如何查看 API 规范？

请参阅：[API 设计](../api.md)。

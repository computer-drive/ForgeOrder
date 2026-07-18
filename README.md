# ForgeOrder 在线点单系统
一个运行于局域网的轻量级在线点单系统。

ForgeOrder 面向餐厅、小吃店、奶茶店等小型商户，支持顾客扫码点单、订单管理以及后台管理。

本系统仍处于开发阶段，仅用于学习和测试。

开发环境主要基于Windows，Linux尚未经过充分测试。

## 项目结构
```
ForgeOrder/
├── server/
├── web/
├── scripts/
├── docs/
└── README.md
```
其中`web`目录为前端代码，`server`目录为后端代码。

## 技术架构
前端：
 - Vue3；
 - Vue Router；
 - Axios；
 - [mdui2](https://mdui.org)。

后端：
 - Python 3.14；
 - Flask；
 - SQLite3。

## 快速开始

### 1. 克隆项目
使用Git克隆项目到本地：
```bash
git clone https://github.com/computer-drive/ForgeOrder.git
```

### 2. 后端操作
在`server`目录下，使用Poetry安装依赖：
```bash
poetry install
```

### 3. 前端操作
在`web`目录下，使用npm安装依赖：
```bash
npm install
```
运行编译命令：
```bash
npm run build
```
注意：编译后的文件将自动放在`/server/static/`目录下。

### 4. 运行后端
在`server`目录下，使用Poetry运行后端：
```bash
poetry run python app.py
```

## 文档
跳转到[文档目录](docs/)。

## RoadMap
- [x] 菜品管理系统
- [ ] 订单管理系统
- [ ] ESC/POS 打印支持
- [ ] 统计系统



## 协议
[MIT License](LICENSE)









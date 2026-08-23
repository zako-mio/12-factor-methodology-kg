# 端口绑定 (Port binding)

- ID: `app-port`
- 类型: 方法原则
- 来源: App 体系
- 分组: GA · 12 Factor App 体系
- 阶段: 基础 basic

> 通过端口绑定自含导出服务，不依赖注入的 Web 服务器

## 核心主张 (what)

- 应用自含，不依赖注入 webserver
- 绑定端口导出 HTTP 服务
- webserver 库作依赖进 user space

## 为什么 (why)

- 避免依赖运行时注入的容器
- 契约即绑定端口提供服务

## 如何实践 (how)

- 依赖声明引入 Tornado/Thin/Jetty
- routing layer 路由请求
- 可成为另一 app 的 backing service

## 案例 (cases)

- Tornado、Thin、Jetty

## 反模式/易错点

- 在 webserver 容器内运行
- 依赖运行时注入 webserver

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-processes → app-port | 前置依赖 | 无状态进程通过端口导出服务 |
| app-port → t-entry | 前置依赖 | 从端口绑定理解自含入口 |
| app-port → ag-trigger | 变体 | 端口自含 ↔ 随处触发 |
| app-processes → app-port | 共现 | 进程与端口绑定共现 |

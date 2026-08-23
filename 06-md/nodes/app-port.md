# 端口绑定 (Port binding)

- ID: `app-port`
- 类型: 方法原则
- 来源: App 体系
- 分组: GA · 12 Factor App 体系
- 阶段: 基础 basic

> 通过端口绑定自含导出服务，不依赖注入的 Web 服务器

## 核心主张 (what)

- web 应用有时在 webserver 容器内执行：PHP 应用作为 Apache HTTPD 内的模块运行，Java 应用跑在 Tomcat 内。
- 十二要素应用完全自包含，不依赖运行时注入 webserver 到执行环境来创建面向 web 的服务。
- web 应用通过绑定端口把 HTTP 作为服务导出，并监听该端口上到来的请求，契约简单清晰，这正是端口绑定模型的自包含体现。
- 本地开发中开发者访问如 http://localhost:5000/ 的服务 URL 来使用应用导出的服务。
- 部署中由 routing layer 处理从公开主机名到端口绑定 web 进程的请求路由，应用无需关心。
- 典型实现：用依赖声明把 webserver 库加入应用，如 Python 的 Tornado、Ruby 的 Thin、Java/JVM 的 Jetty。
- webserver 库完全在 user space（应用代码内部）运行，与运行环境的契约就是绑定端口服务请求。
- HTTP 不是唯一可经端口绑定导出的服务：几乎任何服务器软件都能经进程绑定端口等待请求，如 ejabberd（XMPP）、Redis（Redis 协议）。
- 端口绑定还意味着一个应用可成为另一应用的 backing service：把 backing app 的 URL 作为消费方 config 中的资源句柄即可。

## 为什么 (why)

- 避免依赖运行时注入的 webserver 容器，使执行环境契约简洁统一，部署形态一致，这正是端口绑定模型的自包含体现。
- 契约即绑定端口提供服务，跨环境（本地/云平台）可移植，无需环境特化，使应用在任何执行环境都能以同一方式对外服务。
- 服务可嵌套：应用经端口绑定成为别的应用的 backing service，组合自由度高，是十二要素可移植性与环境契约简洁性的保障。

## 如何实践 (how)

- 经依赖声明引入 webserver 库（Tornado/Thin/Jetty）进 user space，随应用一起构建。
- 进程启动即绑定端口并监听请求，作为对运行环境的服务契约，无需外部注入，这正是端口绑定模型的自包含体现。
- 本地经 http://localhost:端口 访问，生产由 routing layer 从公开主机名路由到端口绑定进程。
- 把某应用的 URL 作为另一应用 config 的资源句柄，实现服务嵌套消费，使应用在任何执行环境都能以同一方式对外服务。

## 案例 (cases)

- Tornado：Python webserver 库，作为依赖加入应用自包含运行，这正是端口绑定模型的自包含体现。
- Thin：Ruby webserver 库；Jetty：Java/JVM webserver 库，均可经依赖引入。
- ejabberd：经端口绑定导出 XMPP 服务，非 HTTP 服务的端口绑定例子，使应用在任何执行环境都能以同一方式对外服务。
- Redis：经端口绑定导出 Redis 协议服务，同样遵循端口绑定模型，是十二要素可移植性与环境契约简洁性的保障。
- http://localhost:5000/：本地开发访问自含应用，无需外部 webserver，服务组合与嵌套因此变得自由而清晰。
- PHP 模块在 Apache HTTPD 内、Java 应用在 Tomcat 内——容器注入的反例。

## 反模式/易错点

- 在 webserver 容器内运行（如 Apache 模块、Tomcat），依赖环境注入，这正是端口绑定模型的自包含体现。
- 依赖运行时注入的 webserver 来提供 web 服务，破坏自包含性，使应用在任何执行环境都能以同一方式对外服务。
- 把 HTTP 当作唯一可经端口导出的服务类型，忽略端口绑定的通用性，是十二要素可移植性与环境契约简洁性的保障。

## 源码索引（实践参考）

- `08-source/app-content-en/port-binding.md` — VII. Port binding 原文：自包含/端口绑定契约/webserver 库/user space/routing layer/服务嵌套
- `08-source/app-content-en/dependencies.md` — webserver 经依赖声明引入的交叉引用
- `08-source/app-content-en/backing-services.md` — 端口绑定服务可作为 backing service 的交叉引用
- `08-source/app-deploy/Procfile` — 实例：web: ruby web.rb -p $PORT 启动即绑定 $PORT

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-processes → app-port | 前置依赖 | 无状态进程通过端口导出服务 |
| app-port → t-entry | 前置依赖 | 从端口绑定理解自含入口 |
| app-port → ag-trigger | 变体 | 端口自含 ↔ 随处触发 |
| app-processes → app-port | 共现 | 进程与端口绑定共现 |

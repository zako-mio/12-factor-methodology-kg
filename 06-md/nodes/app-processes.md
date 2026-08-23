# 进程 (Processes)

- ID: `app-processes`
- 类型: 方法原则
- 来源: App 体系
- 分组: GA · 12 Factor App 体系
- 阶段: 基础 basic

> 以一个或多个无状态进程执行应用

## 核心主张 (what)

- 进程无状态、share-nothing
- 持久数据存入有状态 backing service
- 内存/文件系统仅作单事务缓存

## 为什么 (why)

- 多进程下请求由不同进程处理
- 重启抹掉本地状态

## 如何实践 (how)

- 无状态设计，持久数据外置
- 会话数据入带过期的存储
- 资源在 build 阶段编译

## 案例 (cases)

- Memcached、Redis、asset pipeline

## 反模式/易错点

- sticky sessions
- 文件系统当缓存
- 假设缓存对后续请求可用

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-processes → app-port | 前置依赖 | 无状态进程通过端口导出服务 |
| app-processes → app-concurrency | 前置依赖 | 进程模型是并发的基座 |
| app-processes → app-disposability | 前置依赖 | 进程可处置是鲁棒性前提 |
| app-processes → t-stateless | 前置依赖 | 从无状态进程理解无状态性 |
| app-processes → ag-reducer | 变体 | 无状态进程 ↔ 无状态 reducer |
| app-processes → app-port | 共现 | 进程与端口绑定共现 |

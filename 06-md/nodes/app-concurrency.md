# 并发 (Concurrency)

- ID: `app-concurrency`
- 类型: 方法原则
- 来源: App 体系
- 分组: GA · 12 Factor App 体系
- 阶段: 进阶 intermediate

> 通过进程模型横向扩展

## 核心主张 (what)

- 进程是一等公民，借鉴 unix 模型
- 按工作类型分 process type
- formation 含类型数组与数量
- 还需跨多机横向扩展

## 为什么 (why)

- 进程模型在 scale out 时发光
- 巨型 JVM 仅能纵向扩展

## 如何实践 (how)

- 划分 web/worker 组成 formation
- 进程交系统进程管理器管理

## 案例 (cases)

- systemd、Foreman、Node.js

## 反模式/易错点

- 进程 daemonize/写 PID
- 单进程巨型模型
- 进程对开发者不可见

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-processes → app-concurrency | 前置依赖 | 进程模型是并发的基座 |
| app-concurrency → app-admin | 前置依赖 | 管理进程独立于进程编队 |
| app-concurrency → t-scaling | 前置依赖 | 从进程扩展理解规模化 |

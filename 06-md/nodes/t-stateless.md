# 无状态性 (Statelessness)

- ID: `t-stateless`
- 类型: 桥接主题
- 来源: 桥接
- 分组: GT01 · 无状态性
- 阶段: 高级 advanced

> 无状态是传统应用与 Agent 共有的可靠运行基石

## 核心主张 (what)

- 无状态是两套体系共有的可靠运行基石
- App 进程无状态、状态沉入 backing service
- Agent 把状态重构为事件归约

## 为什么 (why)

- 无状态让单元可丢弃、重启、迁移、恢复
- 是扩展与弹性运维前提

## 如何实践 (how)

- App 状态外置到数据库
- Agent 状态逻辑外置为 thread

## 三栏对比

| App 侧做法 | Agent 侧做法 | 差异根源 |
|---|---|---|
| 进程 share-nothing、会话入缓存 | thread=单一事实源，可序列化 | App 物理外置状态 |
| 持久数据入 backing service | 执行状态从上下文推断 | Agent 逻辑外置状态 |
| 内存仅单事务缓存 | reducer：事件进、状态出 | 易失状态变可重建数据 |

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-processes → t-stateless | 前置依赖 | 从无状态进程理解无状态性 |
| t-stateless → ag-reducer | 前置依赖 | 无状态性落到 Agent 的 reducer |

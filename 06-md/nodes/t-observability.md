# 可观测性与错误可见性 (Observability & Errors)

- ID: `t-observability`
- 类型: 桥接主题
- 来源: 桥接
- 分组: GT04 · 可观测性与错误可见性
- 阶段: 高级 advanced

> 运行可见性是传统日志与 Agent 错误压缩的共同目标

## 核心主张 (what)

- 运行可见性是日志与错误压缩的共同目标
- App 把日志当事件流
- Agent 把错误压缩进上下文

## 为什么 (why)

- 可见性支撑排障审计告警
- Agent 还支撑自愈与拉人决策

## 如何实践 (how)

- App 无缓冲写 stdout 交环境路由
- Agent 错误摘要回写 thread 设阈值

## 三栏对比

| App 侧做法 | Agent 侧做法 | 差异根源 |
|---|---|---|
| 事件流写 stdout | 错误压缩成事件回写 | App 观测消费者是人类（事后） |
| Logplex/Fluentd 路由归档 | 3 次阈值升级 | Agent 观测消费者是 LLM（实时） |
| 趋势绘图与主动告警 | 失败即跳出/重置/升级 | 可观测性从辅助变运行机制 |

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-logs → t-observability | 前置依赖 | 从日志事件流理解可观测性 |
| t-observability → ag-errors | 前置依赖 | 可观测性落到错误压缩 |

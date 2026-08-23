# 规模化与单元粒度 (Scaling & Granularity)

- ID: `t-scaling`
- 类型: 桥接主题
- 来源: 桥接
- 分组: GT08 · 规模化与单元粒度
- 阶段: 高级 advanced

> 进程模型扩展 / 小 Agent 组合，皆是单元化扩展

## 核心主张 (what)

- 进程模型扩展/小 Agent 组合，皆单元化扩展
- App 靠 formation 横向扩展
- Agent 靠小 Agent 编排
- 巨型单元只能纵向难维护

## 为什么 (why)

- 巨型单元难扩展难维护
- 小单元组合可靠可替换易测试

## 如何实践 (how)

- App 按工作类型分 process type
- Agent 拆小 Agent 入 DAG

## 三栏对比

| App 侧做法 | Agent 侧做法 | 差异根源 |
|---|---|---|
| 进程 share-nothing 可水平分区 | 小 Agent 聚焦单领域 | App 单元是同质副本 |
| web/worker 分型 | 确定性 DAG 编排 | Agent 单元是异质能力 |
| 交进程管理器 | 随能力扩展 | App 靠副本数、Agent 靠组合 |

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-concurrency → t-scaling | 前置依赖 | 从进程扩展理解规模化 |
| t-scaling → ag-small | 前置依赖 | 规模化落到小 Agent 组合 |

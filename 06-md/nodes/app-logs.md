# 日志 (Logs)

- ID: `app-logs`
- 类型: 方法原则
- 来源: App 体系
- 分组: GA · 12 Factor App 体系
- 阶段: 进阶 intermediate

> 将日志视为事件流，不关心存储格式

## 核心主张 (what)

- 日志是按时间排序的聚合事件流
- 应用不过问路由或存储
- 进程无缓冲写 stdout

## 为什么 (why)

- 日志提供运行可见性
- logfile 只是输出格式之一

## 如何实践 (how)

- 无缓冲写 stdout
- 路由到文件/Splunk/数据仓库
- Logplex/Fluentd 汇总

## 案例 (cases)

- Logplex、Fluentd、Splunk

## 反模式/易错点

- 应用写/管理 logfile
- 关心路由存储

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-logs → t-observability | 前置依赖 | 从日志事件流理解可观测性 |
| app-logs → ag-errors | 变体 | 日志流 ↔ 错误压缩 |

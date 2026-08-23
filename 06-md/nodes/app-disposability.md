# 可处置性 (Disposability)

- ID: `app-disposability`
- 类型: 方法原则
- 来源: App 体系
- 分组: GA · 12 Factor App 体系
- 阶段: 进阶 intermediate

> 快速启动与优雅终止，最大化鲁棒性

## 核心主张 (what)

- 进程可随时启动或停止
- 启动时间最小化，几秒就绪
- SIGTERM 优雅关闭
- 抵御意外终止

## 为什么 (why)

- 促成快速弹性扩展与部署
- 短启动便于迁移
- 隐含要求请求短暂可重连

## 如何实践 (how)

- 任务归还原队列
- 任务可重入/幂等
- 健壮队列应对突然死亡

## 案例 (cases)

- RabbitMQ NACK、Beanstalkd

## 反模式/易错点

- 启动时间长
- 不平滑退出
- 任务不可重入

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-processes → app-disposability | 前置依赖 | 进程可处置是鲁棒性前提 |
| app-disposability → t-disposable | 前置依赖 | 从可处置进程理解生命周期 |
| app-disposability → ag-pause | 变体 | 可处置性 ↔ 暂停恢复 |

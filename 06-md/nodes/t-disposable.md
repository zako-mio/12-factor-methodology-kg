# 生命周期与可处置性 (Disposability & Lifecycle)

- ID: `t-disposable`
- 类型: 桥接主题
- 来源: 桥接
- 分组: GT02 · 生命周期与可处置性
- 阶段: 高级 advanced

> 进程可快速启停，Agent 可暂停恢复，本质同源

## 核心主张 (what)

- 进程可快速启停，Agent 可暂停恢复
- 运行单元不绑定物理位置
- App 进程级启停，Agent 任务级暂停

## 为什么 (why)

- 可处置促成快速部署与弹性伸缩
- 暂停恢复把可抛弃扩展到长任务续跑

## 如何实践 (how)

- App 短启动+优雅关闭
- Agent launch/pause/resume+thread 持久化

## 三栏对比

| App 侧做法 | Agent 侧做法 | 差异根源 |
|---|---|---|
| 几秒就绪，SIGTERM 优雅关闭 | 简单 API 启动暂停恢复 | App 进程级秒级无状态自动管理 |
| 任务幂等可重试 | 关键暂停点=工具选择与执行之间 | Agent 任务级分钟级需持久化 |
| 抵御突然死亡 | 恢复即加载 thread 状态 | 粒度从进程升到工作流 |

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-disposability → t-disposable | 前置依赖 | 从可处置进程理解生命周期 |
| t-disposable → ag-pause | 前置依赖 | 生命周期落到 Agent 暂停恢复 |

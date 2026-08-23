# 启动/暂停/恢复 (Launch/Pause/Resume)

- ID: `ag-pause`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 进阶 intermediate

> 用简单 API 管理 Agent 生命周期

## 核心主张 (what)

- 用户/应用/其他 Agent 用简单 API 管理
- 长操作时可暂停
- webhook 触发恢复

## 为什么 (why)

- 满足对程序的标准预期
- 编排器多缺「选择与执行之间」暂停点

## 如何实践 (how)

- launch/pause/resume API
- 与 thread 持久化配合恢复

## 案例 (cases)

- pause-resume 动画

## 反模式/易错点

- 依赖无中间暂停的编排器

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-state → ag-pause | 前置依赖 | 统一状态支持暂停恢复 |
| t-disposable → ag-pause | 前置依赖 | 生命周期落到 Agent 暂停恢复 |
| app-disposability → ag-pause | 变体 | 可处置性 ↔ 暂停恢复 |
| ag-state → ag-pause | 共现 | 状态统一与暂停恢复共现 |

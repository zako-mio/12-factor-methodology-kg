# 管理进程 (Admin processes)

- ID: `app-admin`
- 类型: 方法原则
- 来源: App 体系
- 分组: GA · 12 Factor App 体系
- 阶段: 进阶 intermediate

> 管理/维护任务作为一次性进程运行

## 核心主张 (what)

- 一次性任务作为一次性进程运行
- 与常规进程同 codebase/config/release
- admin 代码随应用发布

## 为什么 (why)

- 一次性任务需生产同环境才能正确操作线上数据

## 如何实践 (how)

- 迁移/REPL/一次性脚本
- 依赖隔离与长进程一致
- 本地 shell、生产 ssh

## 案例 (cases)

- manage.py migrate、rake db:migrate

## 反模式/易错点

- admin 代码与应用分离
- 依赖隔离不一致

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-concurrency → app-admin | 前置依赖 | 管理进程独立于进程编队 |
| app-admin → t-human | 前置依赖 | 从管理进程理解人机边界 |

# 构建·发布·运行 (Build, release, run)

- ID: `app-build-run`
- 类型: 方法原则
- 来源: App 体系
- 分组: GA · 12 Factor App 体系
- 阶段: 进阶 intermediate

> 严格分离构建、发布、运行三阶段

## 核心主张 (what)

- build 转代码为可执行包，release=build+config，run 启动进程
- 每 release 唯一 ID
- release 只追加，创建后不可变

## 为什么 (why)

- 运行时无法把改动传播回 build
- run 阶段保持最少活动部件

## 如何实践 (how)

- 严格分离三阶段
- Capistrano releases 支持回滚
- release 打唯一 ID

## 案例 (cases)

- Capistrano

## 反模式/易错点

- 运行时修改代码
- 变更既有 release

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-deps → app-build-run | 前置依赖 | 依赖在构建阶段声明 |
| app-codebase → app-build-run | 前置依赖 | 代码库是构建的输入 |
| app-build-run → t-control | 前置依赖 | 从三阶段分离理解控制流 |
| app-build-run → ag-control | 变体 | 阶段分离 ↔ 控制流所有权 |
| tool-app-site → app-build-run | 依赖关联 | Procfile 三阶段部署实践 |

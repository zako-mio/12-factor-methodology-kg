# 代码库 (Codebase)

- ID: `app-codebase`
- 类型: 方法原则
- 来源: App 体系
- 分组: GA · 12 Factor App 体系
- 阶段: 基础 basic

> 一个代码库，多环境部署，版本控制跟踪一切

## 核心主张 (what)

- 一个 app 一个 codebase、多个 deploy
- codebase 与应用一对一，多 codebase 即分布式系统
- 共享代码抽成库而非复制

## 为什么 (why)

- 单一 codebase 使各部署可标识为同一 app 的不同版本

## 如何实践 (how)

- 版本控制跟踪一切
- 区分 codebase 与 deploy
- 共享代码经依赖管理器引入

## 案例 (cases)

- Git/Mercurial/Subversion

## 反模式/易错点

- 多 codebase 对应一 app
- 多 app 共享同一代码

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-codebase → app-build-run | 前置依赖 | 代码库是构建的输入 |
| app-codebase → ag-prompts | 依赖关联 | prompt 应像代码库一样管理 |
| tool-app-site → app-codebase | 依赖关联 | 站点是 App 原则的参考实现 |

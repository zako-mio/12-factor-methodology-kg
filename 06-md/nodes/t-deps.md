# 依赖与工具显式化 (Dependency & Tool Explicitness)

- ID: `t-deps`
- 类型: 桥接主题
- 来源: 桥接
- 分组: GT05 · 依赖与工具显式化
- 阶段: 高级 advanced

> 显式声明依赖 / 工具，不隐式依赖环境

## 核心主张 (what)

- 显式声明依赖/工具，不隐式依赖环境
- App 用 manifest 声明并隔离
- Agent 用结构化输出声明工具

## 为什么 (why)

- 隐式依赖无法保证存在与兼容
- 显式化才能隔离测试替换

## 如何实践 (how)

- App 声明+隔离双管齐下
- Agent 以 intent schema 定义工具

## 三栏对比

| App 侧做法 | Agent 侧做法 | 差异根源 |
|---|---|---|
| 清单完整声明全部依赖 | 工具=intent 结构化输出 | App 显式化对象是库与包 |
| bundle exec/venv 隔离 | 决策与执行分离 | Agent 是行为能力与副作用 |
| 禁止隐式系统级依赖 | 工具可组合可测试 | Agent 需额外关注授权安全 |

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-deps → t-deps | 前置依赖 | 从依赖声明理解显式化 |
| t-deps → ag-tools | 前置依赖 | 显式化落到工具定义 |

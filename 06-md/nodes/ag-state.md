# 统一执行/业务状态 (Unify execution & business state)

- ID: `ag-state`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 进阶 intermediate

> 将执行状态与业务状态统一为单一事实源

## 核心主张 (what)

- 统一执行状态与业务状态
- 执行状态是上下文元数据
- 不放不必要的东西进 LLM

## 为什么 (why)

- 单一事实来源：简单/可序列化/易调试/可恢复/可分叉

## 如何实践 (how)

- thread=事件流承载一切
- 执行状态从 thread 推断

## 案例 (cases)

- 7 条收益清单

## 反模式/易错点

- 两套独立系统
- 硬塞不可入上下文之物

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-state → ag-pause | 前置依赖 | 统一状态支持暂停恢复 |
| ag-state → ag-reducer | 前置依赖 | 统一状态是无状态 reducer 基础 |
| ag-state → ag-pause | 共现 | 状态统一与暂停恢复共现 |

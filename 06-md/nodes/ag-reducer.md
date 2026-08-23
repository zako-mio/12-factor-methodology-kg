# 无状态 Reducer (Stateless reducer)

- ID: `ag-reducer`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 高级 advanced

> 将 Agent 建模为无状态 reducer（state, event）→ state

## 核心主张 (what)

- Agent 建模为无状态归约器（foldl）
- 输入历史事件，产出下动作
- thread 作纯数据累积

## 为什么 (why)

- 收束统一状态为函数式视角
- 无状态化可序列化/恢复/分叉

## 如何实践 (how)

- 循环建模为 reducer 归约事件
- 状态+事件进，下状态+副作用出

## 案例 (cases)

- agent-foldl 概念图

## 反模式/易错点

- 状态藏全局可变变量

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-state → ag-reducer | 前置依赖 | 统一状态是无状态 reducer 基础 |
| ag-control → ag-reducer | 前置依赖 | 确定性控制流保障 reducer 语义 |
| ag-reducer → ag-small | 前置依赖 | 无状态 reducer 使小 Agent 可行 |
| t-stateless → ag-reducer | 前置依赖 | 无状态性落到 Agent 的 reducer |
| app-processes → ag-reducer | 变体 | 无状态进程 ↔ 无状态 reducer |
| tool-create-agent → ag-reducer | 组合 | 模板含 state.ts 无状态 reducer |

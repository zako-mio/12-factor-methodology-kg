# 掌控上下文窗口 (Own your context window)

- ID: `ag-context`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 进阶 intermediate

> 对上下文进行工程化管理（上下文工程）

## 核心主张 (what)

- 输入本质是「发生了什么，下一步是什么」
- 上下文含 prompt/检索/历史/记忆
- 可自建格式，XML 标签表达事件流

## 为什么 (why)

- 标准消息格式可优化
- 上下文是主接口，掌控构造大幅提性能

## 如何实践 (how)

- 事件驱动 Thread/Event 模型
- event_to_prompt 渲染
- 实验存什么 vs 传什么

## 案例 (cases)

- Context Engineering Cheat Sheet

## 反模式/易错点

- 无条件用标准消息
- 残留错误污染推理
- 用采样参数弥补构造不足

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-prompts → ag-context | 前置依赖 | 拥有 prompt 才能掌控上下文 |
| ag-context → ag-errors | 前置依赖 | 错误压缩是上下文工程应用 |
| ag-context → ag-errors | 组合 | 上下文 + 错误压缩 |

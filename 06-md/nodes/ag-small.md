# 小而专注的 Agent (Small, focused agents)

- ID: `ag-small`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 高级 advanced

> 用多个小 Agent 而非一个巨型 Agent 解决问题

## 核心主张 (what)

- 构建小而专注的 Agent
- 3-10 步最多 20 步
- Agent 是更大确定性系统的构件

## 为什么 (why)

- 任务越大上下文越长，LLM 越易迷失
- 有意识地控制规模是关键

## 如何实践 (how)

- 拆成单领域小 Agent 编排
- 随能力提升逐步扩展范围

## 案例 (cases)

- NotebookLM「紧贴模型能力边界」

## 反模式/易错点

- 单体 Agent 上下文爆长
- 上下文不可靠时激进扩展

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-reducer → ag-small | 前置依赖 | 无状态 reducer 使小 Agent 可行 |
| ag-small → ag-trigger | 前置依赖 | 小 Agent 便于随处触发 |
| t-scaling → ag-small | 前置依赖 | 规模化落到小 Agent 组合 |

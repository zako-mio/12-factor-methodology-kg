# 工具即结构化输出 (Tools are structured outputs)

- ID: `ag-tools`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 基础 basic

> 工具只是模型的结构化输出，可无限组合

## 核心主张 (what)

- 工具调用=LLM 输出可解析的 JSON
- 三步：输出 JSON→执行→喂回
- 决策与执行分离
- 不锁死固定函数对应

## 为什么 (why)

- 使决策执行解耦
- 为掌控控制流铺路

## 如何实践 (how)

- 数据类按 intent 输出 JSON
- switch 分发未知走 else

## 案例 (cases)

- CreateIssue/SearchIssues

## 反模式/易错点

- 工具与固定函数一一对应

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-nl2tool → ag-tools | 前置依赖 | 工具是自然语言调用的结构化输出 |
| ag-tools → ag-human | 前置依赖 | 联系人类是一类工具调用 |
| ag-tools → ag-control | 前置依赖 | 工具组合受控制流编排 |
| t-deps → ag-tools | 前置依赖 | 显式化落到工具定义 |
| app-deps → ag-tools | 变体 | 依赖清单 ↔ 工具定义 |
| ag-tools → ag-human | 组合 | 工具 + 人类批准 |
| app-backing → ag-tools | 依赖关联 | 工具是 Agent 的外部后端服务 |
| tool-create-agent → ag-tools | 组合 | 模板含 BAML 工具定义（tool_calculator） |

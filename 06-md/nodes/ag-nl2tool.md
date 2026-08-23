# 自然语言→工具调用 (NL to Tool Calls)

- ID: `ag-nl2tool`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 基础 basic

> LLM 将自然语言转换为结构化工具调用对象

## 核心主张 (what)

- 自然语言翻译为结构化工具调用对象
- 确定性代码执行 payload
- 真实 Agent 先查询 ID 构建 payload

## 为什么 (why)

- 最常见最强大的模式，既能推理又能执行
- 结构化输出让后续处理依赖确定代码

## 如何实践 (how)

- LLM 返回 nextStep 对象
- switch/if 分发，未知走 else
- 参考 mailcrew

## 案例 (cases)

- Stripe payment link、mailcrew

## 反模式/易错点

- 不回收结果循环
- ID 硬编码不进查询

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-nl2tool → ag-tools | 前置依赖 | 工具是自然语言调用的结构化输出 |
| ag-nl2tool → ag-control | 前置依赖 | 工具调用需要确定性控制流 |
| tool-create-agent → ag-nl2tool | 组合 | 脚手架内建自然语言→工具调用模板 |

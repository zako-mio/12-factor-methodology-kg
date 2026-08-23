# 掌控你的 Prompt (Own your prompts)

- ID: `ag-prompts`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 基础 basic

> 像管理代码一样版本化、测试、部署 prompt

## 核心主张 (what)

- prompt 作一等公民代码
- 用 BAML 写带类型签名的函数
- 收益：可控、可测、可迭代、透明

## 为什么 (why)

- prompt 是应用逻辑与 LLM 的主接口
- 黑盒框架难精确调优定位

## 如何实践 (how)

- 不依赖框架抽象，直接写显式 prompt
- 像代码一样建测试与 evals

## 案例 (cases)

- BAML 的 DetermineNextStep

## 反模式/易错点

- 依赖黑盒 Agent 抽象
- prompt 工程完全外包

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-prompts → ag-context | 前置依赖 | 拥有 prompt 才能掌控上下文 |
| t-config → ag-prompts | 前置依赖 | 可变性外置落到 prompt 管理 |
| t-parity → ag-prompts | 前置依赖 | 一致性落到 prompt 环境 |
| app-config → ag-prompts | 变体 | 环境配置 ↔ prompt 管理 |
| app-codebase → ag-prompts | 依赖关联 | prompt 应像代码库一样管理 |
| tool-workshops → ag-prompts | 组合 | 工作坊演练 prompt 管理与工具编排 |

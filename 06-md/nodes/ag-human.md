# 工具调用联系人类 (Contact humans with tools)

- ID: `ag-human`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 进阶 intermediate

> 把人类接入作为一类工具调用，主动寻求批准

## 核心主张 (what)

- 请求人类输入建模成工具调用
- 显式声明意图而非 token 隐式选择
- 支持外循环与多人类接入

## 为什么 (why)

- 清晰指令、内外循环、多人类、多 Agent、持久化

## 如何实践 (how)

- RequestHumanInput 保存状态跳出循环
- webhook 收回复重入循环

## 案例 (cases)

- request_human_input→human_response

## 反模式/易错点

- token 隐式决定联系人类
- 只支持 chat 流

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-tools → ag-human | 前置依赖 | 联系人类是一类工具调用 |
| t-human → ag-human | 前置依赖 | 人机边界落到人类批准 |
| ag-tools → ag-human | 组合 | 工具 + 人类批准 |
| tool-create-agent → ag-human | 组合 | 模板含 a2h.ts 人类批准机制 |

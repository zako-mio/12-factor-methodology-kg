# 压缩错误进上下文 (Compact errors)

- ID: `ag-errors`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 进阶 intermediate

> 把错误摘要压缩回上下文窗口供模型反思

## 核心主张 (what)

- 失败时格式化错误追加进上下文
- errorCounter 限重试约 3 次
- 达阈值跳出或升级人类

## 为什么 (why)

- 自愈与持久化
- 错误+阈值是拉人进循环的触发点

## 如何实践 (how)

- type='error' 事件回写继续循环
- 计数成功清零失败自增

## 案例 (cases)

- 基础版+计数进阶版

## 反模式/易错点

- 过度重试空转
- 原始错误原样回塞

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-context → ag-errors | 前置依赖 | 错误压缩是上下文工程应用 |
| t-observability → ag-errors | 前置依赖 | 可观测性落到错误压缩 |
| app-logs → ag-errors | 变体 | 日志流 ↔ 错误压缩 |
| ag-context → ag-errors | 组合 | 上下文 + 错误压缩 |

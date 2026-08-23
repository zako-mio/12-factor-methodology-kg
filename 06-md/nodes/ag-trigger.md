# 随处触发 (Trigger from anywhere)

- ID: `ag-trigger`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 高级 advanced

> 从任何触发源唤起 Agent，触达用户所在之处

## 核心主张 (what)

- 从 slack/email/sms 等渠道触发并回复
- 支持事件/cron 等非人类触发
- 可运行 5/20/90 分钟

## 为什么 (why)

- 像数字同事融入工作流
- 可审计性与执行大事的信心

## 如何实践 (how)

- 暴露多通道入口
- 关键决策点联系人类

## 案例 (cases)

- slack/email/sms、events/crons

## 反模式/易错点

- 单一入口/单一聊天界面
- 因无复核不给高价值权限

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-small → ag-trigger | 前置依赖 | 小 Agent 便于随处触发 |
| t-entry → ag-trigger | 前置依赖 | 自含入口落到随处触发 |
| app-port → ag-trigger | 变体 | 端口自含 ↔ 随处触发 |

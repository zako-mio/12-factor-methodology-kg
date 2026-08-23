# 随处触发 (Trigger from anywhere)

- ID: `ag-trigger`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 高级 advanced

> 从任何触发源唤起 Agent，触达用户所在之处

## 核心主张 (what)

- 让用户能从 slack、email、sms 或其他任何他们喜欢的渠道触发 Agent，并让 Agent 通过同样的渠道回复——在用户所在的地方遇见他们。
- 这是对 factor 6（Launch/Pause/Resume）与 factor 7（Contact Humans With Tools）的自然延伸：做好前两条，你就有资格引入这条。
- 收益一：在用户所在之处服务用户，帮助构建感觉像真人的 AI 应用，至少像一位靠谱的数字同事。，属于该因子的基础原则，应在设计中显式落实。
- 收益二：外循环 Agent（Outer Loop Agents）——允许 Agent 被非人类触发：事件、cron、宕机警报等；它们可能工作 5、20、90 分钟，到关键点联系人类请求帮助。
- 收益三：高价值工具（High Stakes Tools）——能快速拉进各种人类后，你可以给 Agent 更高风险的操作权限，比如发送外部邮件、更新生产数据等。
- 保持清晰标准能带来可审计性与对『执行更大更好事情』的 Agent 的信心，标准是信任的基石。，属于该因子的基础原则，应在设计中显式落实。
- 与 factor 7 的 RequestHumanInput/webhook 配合，多渠道触发→等待→多渠道回复形成完整闭环。
- 原文自嘲：如果你们在等 humanlayer 的推销，就是这里了——该因子正是 humanlayer 的产品动机。
- workshop 中 agent 通过 email 收审批、slack 收消息、webhook 恢复的流程都是本因子的工程落地。

## 为什么 (why)

- 在用户所在之处服务：更自然的交互体验，Agent 像数字同事而不是需要用户特意去用的独立应用。，属于该因子的基础原则，应在设计中显式落实。
- 外循环能力：被事件/cron/宕机触发而非只能由人发起，Agent 可以长时间后台工作后在关键点主动找人。
- 高价值操作解锁：能快速拉人复核，才敢让 Agent 发外部邮件、改生产数据——信任来自复核链路而非限制。
- 清晰标准与可审计性：多渠道接入加结构化记录，让高风险 Agent 有据可查、可信可用，信任可累积。，属于该因子的基础原则，应在设计中显式落实。
- 多渠道触达是『数字同事』体验与 7×24 无人值守运营的前提，规模化运营的必需能力。，属于该因子的基础原则，应在设计中显式落实。

## 如何实践 (how)

- 暴露多通道入口：slack、email、sms、webhook 各建入口，把外部消息统一转成 conversation.created 或用户消息事件。
- 回复走同一渠道：humanlayer 等工具用 contactChannel（email/slack 地址）指定回复通道，保证回程一致。
- 支持非人类触发：cron 定时、事件订阅、宕机告警都能启动 Agent（factor 11 明确列出 events/crons/outages）。
- 让 Agent 长时间工作：5/20/90 分钟级别，到关键决策点再联系人类（请求帮助/反馈/批准）。
- 给高风险工具配人类复核：发送外部邮件、更新生产数据前拉人确认，保持审计标准，授权有底线。，属于该因子的基础原则，应在设计中显式落实。
- 模板 server.ts 的 outerLoop 即多渠道入口的骨架：conversation.created 开新线程、human_contact.completed / function_call.completed 恢复线程。
- 与 factor 6 配合：webhook 触发恢复，无编排器深耦合，外部系统都能唤醒 Agent。
- 与 factor 7 配合：RequestHumanInput 加 notify_human 决定何时、用什么渠道找人。

## 案例 (cases)

- 渠道列表：slack、email、sms 以及任意用户想要的渠道，都是触发与回复的载体，入口要广。，属于该因子的基础原则，应在设计中显式落实。
- 非人类触发列表：events、crons、outages（原文明确列出三类），Agent 可被系统事件唤醒。
- 运行时长区间：『They may work for 5, 20, 90 minutes』原文原话，长时后台工作是常态。
- 高价值工具示例：sending external emails、updating production data，需要复核才能授权。
- humanlayer 产品动机（原文点明这是其销售点），多渠道触达正是其核心卖点。，属于该因子的基础原则，应在设计中显式落实。
- workshop email 审批：HUMANLAYER_EMAIL 指定邮箱，fetchHumanApproval 收批准/拒绝反馈。
- server.ts 的 V1Beta3 事件类型：conversation.created / human_contact.completed / function_call.completed 三种 webhook 事件恢复或新建线程。

## 反模式/易错点

- 只提供单一入口（如只限网页聊天界面），用户要跳出工作流去用你的应用，体验割裂、触达面窄。，属于该因子的基础原则，应在设计中显式落实。
- Agent 只能由人类发起，无法被事件/cron/宕机触发（无外循环能力），无法无人值守运行。，属于该因子的基础原则，应在设计中显式落实。
- 因没有复核链路就限制 Agent 权限，只让它做低价值调用，浪费能力，应建复核而非砍权限。，属于该因子的基础原则，应在设计中显式落实。
- 多渠道接入后不在关键决策点联系人类，导致高风险操作无审计，授权与复核必须成对。，属于该因子的基础原则，应在设计中显式落实。
- 回复渠道与触发渠道不一致，用户在 slack 问却在邮箱收到答案，体验混乱，回程要对齐。，属于该因子的基础原则，应在设计中显式落实。
- 渠道事件与线程状态脱节，webhook 回程找不到对应 thread，恢复失败，事件须携带线程引用。

## 源码索引（实践参考）

- `08-source/agent-content/factor-11-trigger-from-anywhere.md` — 原文完整内容：多渠道触发、外循环 Agent、高价值工具
- `08-source/agent-packages/create-12-factor-agent/template/src/server.ts` — 模板外循环：conversation.created / human_contact.completed / function_call.completed 事件处理
- `08-source/agent-content/factor-06-launch-pause-resume.md` — 前置依赖：webhook 恢复机制
- `08-source/agent-content/factor-07-contact-humans-with-tools.md` — 前置依赖：RequestHumanInput 与多渠道通知

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-small → ag-trigger | 前置依赖 | 小 Agent 便于随处触发 |
| t-entry → ag-trigger | 前置依赖 | 自含入口落到随处触发 |
| app-port → ag-trigger | 变体 | 端口自含 ↔ 随处触发 |

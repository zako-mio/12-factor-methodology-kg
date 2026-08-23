# 启动/暂停/恢复 (Launch/Pause/Resume)

- ID: `ag-pause`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 进阶 intermediate

> 用简单 API 管理 Agent 生命周期

## 核心主张 (what)

- Agent 只是程序，我们理应对它们如何被启动、查询、恢复、停止有明确预期——这就是 Launch/Pause/Resume 的诉求。
- 用户、应用、流水线和其他 Agent 应该能用简单的 API 轻易地启动一个 Agent，而不需要了解内部编排细节。
- Agent 及其编排的确定性代码应该在需要长时运行操作（如等人类回复、跑长任务）时能暂停它，而不是阻塞占用资源。
- 外部触发器（如 webhook）应该能让 Agent 从上次停下的地方恢复，而不需要与 Agent 编排器深度集成。
- 本因子与 factor 5（统一执行/业务状态）和 factor 8（掌控控制流）紧密相关，但可以独立实现。
- 原文特别提醒：很多 AI 编排器允许暂停/恢复，但恰恰不允许在『工具选择』与『工具执行』之间暂停，这正是审批窗口所在。
- 这个『选择与执行之间』的暂停点正是高价值操作的审批/复核窗口，缺失它就无法在工具运行前审查，风险不可控。
- 与 factor 7（用工具调用联系人类）和 factor 11（随处触发）配合，暂停/恢复才能支撑多人在线工作流。
- workshop 实现：把 /thread 端点改成异步处理并立即返回 {'status':'processing'}，联系人类后结束处理，由 webhook 恢复。

## 为什么 (why)

- Agent 也是程序，用户与系统对它有与普通程序一致的操作预期：能启动、能查状态、能暂停、能恢复、能停止。
- webhook 恢复意味着外部事件（邮件回复、Slack 消息）能无缝把 Agent 唤醒，无需深耦合编排器内部。
- 暂停点是确定性代码干预的窗口：审批、复核、长任务等待都依赖它，缺失则无法做高价值操作，价值天花板被锁死。
- 配合 factor 5 的 thread 序列化，暂停/恢复成本极低——存 thread、load thread 即完成恢复。
- 编排器普遍缺『选择与执行之间』的暂停能力，自己实现才能获得完整的控制粒度，这是本因子独立存在的价值。

## 如何实践 (how)

- 暴露简单 API：POST /thread 启动、GET /thread/:id 查询状态、/thread/:id/response 或 /webhook 提交回复。
- 长操作前让确定性代码暂停：检测 awaitingHumanResponse() 时先 save 状态再返回，不再继续循环。
- 用 webhook 接收外部结果：app.post('/webhook') 解析事件（如 V1Beta2HumanContactCompleted），从 event.spec.state.thread_id 恢复 thread。
- 恢复流程：load_state(thread_id) → 把 response_from_human 事件 push 进 thread → 重新跑 determine_next_step → 继续循环。
- 异步化端点：POST /thread 立即返回 {'status':'processing'}，处理在 Promise.resolve().then() 后台进行。
- 在 createHumanContact 时把 state.thread_id 塞进 spec，让 webhook 回程能精确定位线程。
- 模板 server.ts 的 outerLoop：根据 conversation.created / human_contact.completed / function_call.completed 三种事件新建或恢复线程。
- 与 factor 8 配合：暂停后编排器可以自由决定何时、由谁来恢复，形成自然的中断/恢复工作流，恢复时机完全自主。

## 案例 (cases)

- 原文动画 165-pause-resume-animation.gif 演示暂停/恢复过程，直观展示 API 语义。
- workshop webhook 集成：POST /thread 立即返回 processing，humanlayer 云回调 /webhook 恢复执行。
- server.ts 的 outerLoop 用 body.type 区分 conversation.created / human_contact.completed / function_call.completed。
- createHumanContact spec 携带 state: { thread_id }，webhook 回程通过 spec.state.thread_id 找回线程。
- 异步端点实现：Promise.resolve().then(async () => { const threadId = store.create(thread); … }) 后 res.json({status:'processing'})。
- handleHumanResponse：校验 thread.awaitingHumanResponse() 后 push 人类回复并继续 agentLoop 循环。
- 原文提醒的编排器缺口：『between tool selection and tool execution』没有暂停点的常见缺陷。

## 反模式/易错点

- 依赖不允许在工具选择与执行之间暂停的编排器，丧失审批与复核窗口，高价值操作无从保障，应自建控制流。，属于该因子的基础原则，应在设计中显式落实。
- 恢复逻辑与编排器深度耦合，外部 webhook 无法独立唤醒 Agent，集成面窄，应依赖公开 API 恢复。
- 暂停时把任务挂在内存里 while...sleep 空转等待，进程一断就得从头再来，可恢复性为零。，属于该因子的基础原则，应在设计中显式落实。
- 缺少查询端点（GET /thread/:id），外部系统无法知道 Agent 当前卡在哪一步，可观测性缺失。
- 恢复时从零重启整条流程，而不是加载 thread 从断点继续，浪费且易错，应直接加载持久化线程。，属于该因子的基础原则，应在设计中显式落实。
- 不把线程状态落盘，暂停后进程重启即丢失全部上下文，无法恢复，必须先持久化落盘再暂停，否则现场全丢。，属于该因子的基础原则，应在设计中显式落实。

## 源码索引（实践参考）

- `08-source/agent-content/factor-06-launch-pause-resume.md` — 原文完整内容：Launch/Pause/Resume 简单 API 与编排器缺口
- `08-source/agent-packages/create-12-factor-agent/template/src/server.ts` — 模板实现：outerLoop 按事件新建/恢复线程，webhook 恢复
- `08-source/agent-workshops/2025-05/walkthrough.md` — workshop Chapter 12 humanlayer-webhook：异步 /thread 加 /webhook 恢复

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-state → ag-pause | 前置依赖 | 统一状态支持暂停恢复 |
| t-disposable → ag-pause | 前置依赖 | 生命周期落到 Agent 暂停恢复 |
| app-disposability → ag-pause | 变体 | 可处置性 ↔ 暂停恢复 |
| ag-state → ag-pause | 共现 | 状态统一与暂停恢复共现 |

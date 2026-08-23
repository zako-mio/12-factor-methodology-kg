# 生命周期与可处置性 (Disposability & Lifecycle)

- ID: `t-disposable`
- 类型: 桥接主题
- 来源: 桥接
- 分组: GT02 · 生命周期与可处置性
- 阶段: 高级 advanced

> 进程可快速启停，Agent 可暂停恢复，本质同源

## 核心主张 (what)

- App 进程是可处置的：可随时被启动或停止，促成快速弹性伸缩与鲁棒性（disposability.md）
- Agent 是程序，需要简单的启动/暂停/恢复/停止 API 管理其生命周期（factor-06）
- App 进程应把启动时间最小化到秒级，为 release 与扩容提供敏捷性（disposability.md）
- Agent 的暂停点应落在工具选择与工具执行之间，以便审批与续跑（factor-08 关键洞见）
- 两侧运行单元都不绑定物理位置：App 可被进程管理器迁移，Agent 可由外部 webhook 恢复（disposability.md/factor-06）
- App 优雅关闭：收到 SIGTERM 停止监听、完成在途请求再退出（disposability.md）
- Agent 外部触发（webhook）可在不深度集成编排器的情况下从离开处续跑（factor-06）
- 可处置性/暂停恢复的本质同源：让运行单元可被安全地中断并重新开始
- 任务需幂等或可重试，才能支撑突然死亡后的安全重启（disposability.md reentrant）

## 为什么 (why)

- 短启动时间给 release 流程和扩容更多敏捷性，也让进程管理器更易把进程迁到新物理机（disposability.md）
- 优雅关闭避免请求中断：web 进程停收新请求、完成现有请求；worker 把作业退回队列（disposability.md）
- Agent 暂停恢复把可处置性从「可抛弃」扩展到「长任务续跑」，支撑数小时级外环工作流（factor-06/11）
- 在工具选择与执行之间插暂停点，才能实现工具执行前的人类审批（factor-08）
- 没有该暂停粒度，只能内存 sleep 重启重跑、或限制低风险、或赌高风险（factor-08 三选一）

## 如何实践 (how)

- App：进程监听 SIGTERM 后先停止接收新请求，再完成在途请求，最后退出（disposability.md）
- App：worker 收到 SIGTERM 把当前作业 NACK 回队列（RabbitMQ）或依赖队列自动返回（Beanstalkd）（disposability.md）
- App：作业包成事务或做成幂等操作，保证 reentrant（disposability.md）
- Agent：agentLoop 遇到 done_for_now/request_more_information/divide 返回 thread 表示暂停（agent.ts）
- Agent：thread 持久化到 ThreadStore，webhook 回程时 store.get(threadId) 恢复续跑（server.ts）
- Agent：CLI 模式下 askHumanCLI 暂停循环等待 Enter 审批或反馈取消（cli.ts）
- Agent：human_contact.completed / function_call.completed 事件携带 thread_id 回程（server.ts 类型）
- 两侧都按崩溃后可从已知检查点恢复来设计，而非假设进程永不死亡

## 三栏对比

| App 侧做法 | Agent 侧做法 | 差异根源 |
|---|---|---|
| 进程秒级就绪，进程管理器可随时将其迁往新物理机（disposability.md） | 简单 API 让用户/应用/流水线/其他 Agent 都能启动一个 Agent（factor-06） | App 是可处置进程：进程级、秒级、由进程管理器自动管理；Agent 是可暂停工作流：任务级、分钟级、需显式持久化 |
| SIGTERM 触发优雅关闭：停监听端口→拒绝新请求→完成现有请求→退出（disposability.md） | 关键暂停点=工具选择与执行之间，框架常缺此能力（factor-08 note） | App 恢复单位是单个进程/请求；Agent 恢复单位是整条 thread/对话工作流 |
| worker 用 NACK 把当前作业退回队列，锁系统需显式释放锁（disposability.md） | 恢复=加载 thread 状态继续循环，无需重新理解任务上下文（factor-05 recovery + server.ts） | App 生命周期由 SIGTERM 信号驱动；Agent 生命周期由 intent/事件（done_for_now/approval）驱动 |
| 依赖 Beanstalkd 等健壮排队后端，客户端断开/超时时作业自动回队（disposability.md） | webhook 外部触发恢复，无需与编排器深度集成（factor-06） | 粒度从进程升到工作流：App 丢弃进程，Agent 保留线程并在暂停点接续 |
| HTTP 请求保持短时长，或长轮询客户端无缝重连（disposability.md） | 确定性代码与 LLM 都能暂停 Agent：如 deploy 类高赌注工具 break 循环等审批（factor-08） | App 可处置面向无状态副本的弹性伸缩；Agent 暂停恢复面向有状态任务的人工介入与长程执行 |
| 作业全部 reentrant：结果包事务或操作幂等（disposability.md） | thread_id 随 human contact 的 state 持久化，保证回程定位到正确会话（server.ts createHumanContact state.thread_id） |  |
| 架构按 crash-only 设计处理非优雅终止，极端情形到 CouchDB 全崩溃设计（disposability.md） | function_call.completed 事件仅在 approved 时执行工具，否则把拒绝反馈写入 thread（server.ts） |  |

## 源码索引（实践参考）

- `08-source/app-content-en/disposability.md` — 
- `08-source/app-content-en/build-release-run.md` — 
- `08-source/app-content-en/processes.md` — 
- `08-source/agent-content/factor-06-launch-pause-resume.md` — 
- `08-source/agent-content/factor-08-own-your-control-flow.md` — 
- `08-source/agent-content/factor-05-unify-execution-state.md` — 
- `08-source/agent-packages/create-12-factor-agent/template/src/agent.ts` — 
- `08-source/agent-packages/create-12-factor-agent/template/src/server.ts` — 
- `08-source/agent-packages/create-12-factor-agent/template/src/cli.ts` — 

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-disposability → t-disposable | 前置依赖 | 从可处置进程理解生命周期 |
| t-disposable → ag-pause | 前置依赖 | 生命周期落到 Agent 暂停恢复 |

# 无状态性 (Statelessness)

- ID: `t-stateless`
- 类型: 桥接主题
- 来源: 桥接
- 分组: GT01 · 无状态性
- 阶段: 高级 advanced

> 无状态是传统应用与 Agent 共有的可靠运行基石

## 核心主张 (what)

- App 进程必须无状态且 share-nothing，任何需持久的数据都要存进有状态的 backing service（processes.md 原文）
- Agent 将执行状态与业务状态统一为单一 thread 事件流，作为唯一事实源（factor-05）
- App 进程内存或文件系统只能作短暂的单事务缓存，未来请求或重启后一律不可依赖（processes.md）
- Agent 的一切执行状态（当前步/等待/重试计数）可从上下文窗口推断，无需独立跟踪（factor-05）
- 无状态是两套体系共同认可的运行基石：支撑扩展、迁移、恢复与弹性运维（processes.md/concurrency.md）
- Agent 把状态重构为无状态 reducer：事件进、状态出，thread 只是事件序列（factor-12）
- App 粘性会话（sticky sessions）明确违反十二因子，会话状态应入带过期机制的数据存储（processes.md）
- Agent thread 可序列化/反序列化、可从任意点恢复、可 fork 子集到新上下文（factor-05 七项收益）
- LLM 本质是无状态函数，输入即输出，因此上下文（输入）工程就是状态管理（factor-03）
- 两侧都把易失状态外置：App 外置到存储，Agent 外置为可重建的事件流

## 为什么 (why)

- 无状态使运行单元可被任意丢弃、重启、迁移而数据不丢，这是快速部署与扩缩容前提（processes.md/disposability.md）
- share-nothing 架构保证多进程水平扩展时无需跨实例共享内存，扩容简单可靠（concurrency.md）
- App 状态外置到 backing service，使数据库等资源可随时挂摘而不改代码（backing-services.md）
- Agent 单一事实源带来七项收益：简单、可序列化、易调试、灵活、可恢复、可 fork、可转人读视图（factor-05）
- 无状态 reducer 使暂停/恢复、小 Agent 组合、随处触发等高级能力成为可能（factor-12/06/10/11）

## 如何实践 (how)

- App：会话状态放入 Memcached/Redis 等提供过期机制的数据存储，而非进程内存（processes.md）
- App：资产编译放进 build 阶段而非运行时文件系统，避免本地缓存依赖（processes.md 资产打包示例）
- App：大文件下载等操作仅用内存做单事务缓冲，结果入库（processes.md）
- Agent：用 Thread 事件数组承载全部历史，serializeForLLM 把事件序列化为 XML 喂给 LLM（agent.ts）
- Agent：agentLoop 每次循环重新调用 DetermineNextStep(serializeForLLM(thread))，无隐藏可变状态（agent.ts）
- Agent：执行状态从上下文推断，特殊 ID 尽量最小化（factor-05 会话ID/密码上下文例外）
- Agent：thread 持久化到 ThreadStore 接口，可按需换 redis/sqlite/postgres（state.ts 注释）
- 两侧共同原则：任何未来可能被复用的数据都不允许依赖运行单元本地的易失内存/文件

## 三栏对比

| App 侧做法 | Agent 侧做法 | 差异根源 |
|---|---|---|
| 进程 share-nothing，未来请求极可能由不同进程实例服务（processes.md） | thread 是可序列化事件数组，FileSystemThreadStore 以 JSON 落盘 .threads 目录（state.ts create/update） | App 是物理外置：状态落盘到外部存储服务（数据库/缓存）；Agent 是逻辑外置：状态编码为事件流 |
| 持久数据全部进入数据库等 stateful backing service（processes.md） | 执行状态（当前步骤/等待状态/重试计数）由 thread 推断而非独立字段（factor-05） | App 无状态单元是同质进程副本；Agent 无状态单元是带 thread 状态的具体会话实例 |
| 内存/文件系统仅作单事务缓存：下载大文件→处理→结果入库（processes.md） | 业务状态即事件历史：消息、工具调用、工具结果全部入事件流（factor-05） | 易失状态变可重建数据：App 靠重启后从存储重读，Agent 靠 reload thread 事件重放 |
| 重启（部署/配置变更/环境迁移）会清空全部本地状态，设计上不假设其留存（processes.md） | 恢复即重载 thread 状态继续 agentLoop，无需从任务起点重跑（factor-05 recovery） | App 强调运行时共享数据外置（多进程间）；Agent 强调决策上下文可回放（多轮推理间） |
| 拒绝粘性会话，改把会话状态放 Memcached/Redis（processes.md） | 可 fork：复制 thread 子集进新上下文/新状态 ID，支持探索式分叉（factor-05 forking） | 粒度差异：App 以请求/作业为单位无状态；Agent 以整条工作流/thread 为单位 |
| 多进程类型实例并存，web/worker 各自无状态化运行（concurrency.md） | serializeOneEvent 把非 intent 字段展开为 key: value，保证 LLM 看到完整历史（agent.ts） | 恢复机制不同：App 进程崩溃即放弃缓存重新拉取；Agent 保留事件序列支持断点续跑 |
| 编译型资产由构建管线产出，运行时不依赖进程本地文件缓存（processes.md） | BAML 客户端由 generators.baml 生成，线程序列化格式与工具 schema 保持同步（agent.baml） |  |

## 源码索引（实践参考）

- `08-source/app-content-en/processes.md` — 
- `08-source/app-content-en/concurrency.md` — 
- `08-source/app-content-en/backing-services.md` — 
- `08-source/agent-content/factor-05-unify-execution-state.md` — 
- `08-source/agent-content/factor-12-stateless-reducer.md` — 
- `08-source/agent-content/factor-03-own-your-context-window.md` — 
- `08-source/agent-packages/create-12-factor-agent/template/src/agent.ts` — 
- `08-source/agent-packages/create-12-factor-agent/template/src/state.ts` — 

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| app-processes → t-stateless | 前置依赖 | 从无状态进程理解无状态性 |
| t-stateless → ag-reducer | 前置依赖 | 无状态性落到 Agent 的 reducer |

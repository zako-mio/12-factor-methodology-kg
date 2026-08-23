# 统一执行/业务状态 (Unify execution & business state)

- ID: `ag-state`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 进阶 intermediate

> 将执行状态与业务状态统一为单一事实源

## 核心主张 (what)

- 在 AI 世界之外，许多基础设施系统也倾向于把『执行状态』与『业务状态』分开管理；对 AI 应用而言这可能需要跟踪当前步骤、下一步、等待状态、重试计数等。
- 这种分离会引入复杂度，有时值得，但很可能对你这个用例是过度设计——是否分开管理完全由你决定，别以为非分开不可。
- 执行状态（execution state）指：当前步骤、下一步、等待状态、重试次数等过程性的元数据。
- 业务状态（business state）指：Agent 工作流迄今为止发生的事，例如 OpenAI 消息列表、工具调用及其结果的列表。
- 核心建议：尽可能简化，把两者尽量统一成一份状态，而不是维护两套并行数据，同一 thread 事件流即承载全部状态。
- 实际上你可以这样设计应用：让所有执行状态都能从上下文窗口推断出来，很多情况下执行状态只是『发生了什么』的元数据。
- 确实有些东西放不进上下文窗口，如 session id、密码上下文等，但你的目标应该是把这类东西最小化。
- 借助 factor 3（掌控上下文窗口），你可以精确控制到底什么进 LLM、什么只留在外部状态存储里。
- 原文用动画演示统一前后：分离的两列状态（execution/business）最终合并为单一的 thread 事件流。

## 为什么 (why)

- 简单性：所有状态的唯一事实来源，不再有两套系统互相不同步，心智负担大幅下降，跨端一致性天然满足。，属于该因子的基础原则，应在设计中显式落实。
- 可序列化：thread 可以轻松地序列化/反序列化，持久化、传输、恢复都毫无负担，配合 JSON 落盘即可。
- 可调试：完整历史在一个地方可见，问题定位快，不用跨多个存储拼凑现场，复盘整条事件链即可定位根因。，属于该因子的基础原则，应在设计中显式落实。
- 灵活性：新增状态只需新增事件类型，无需改动存储 schema 或迁移数据，演进成本几乎为零且向后兼容。
- 可恢复：只要加载 thread 就能从任意断点恢复执行，暂停/恢复天然成立，无需额外重建任何上下文。
- 可分叉：复制 thread 的一部分到新的上下文/状态 ID，就能在任意点 fork 出分支试验，适合并行探索。
- 人机界面与可观测性：把 thread 转成人类可读的 markdown 或富 Web UI 极其容易，可观测性免费获得。
- 把执行状态收编进上下文元数据后，暂停/恢复（factor 6）与恢复逻辑自然成立，无需额外同步，省掉一套机制。

## 如何实践 (how)

- 用 thread（事件流）作为承载一切的单一结构：Thread.events 保存 user_input、tool_call、tool_response、error、human_response 等事件。
- 从 thread 推断执行状态：当前步骤 = 最后一个未完成事件，等待状态 = 最后事件是否为 request_more_information/done_for_now（见 awaitingHumanResponse）。
- 让所有需要决策的信息都进上下文，session id、密码等机密留在外部存储，只把脱敏引用传入，兼顾效果与安全。
- 用 factor 3 的序列化函数（serializeForLLM）决定 thread 中哪些事件、以什么格式进入 LLM。
- 实现 FileSystemThreadStore（create/get/update），thread 落盘为 JSON 与 LLM 序列化文本双份（存 .threads 目录）。
- 新增业务能力时新增 Event.type 与对应 data，而不是另起一套执行状态表来维护，保持单一事实来源。
- 持久化时机：每次工具执行或等待人类前先 save_state(thread)，恢复时 load_state(thread_id)。
- 可替换任意简单状态管理：Redis/SQLite/Postgres 皆可，接口不变，存储迁移成本低。

## 案例 (cases)

- 原文 7 条收益清单：Simplicity/Serialization/Debugging/Flexibility/Recovery/Forking/Human Interfaces & Observability。
- 执行状态与业务状态的定义对比列表（原文明确列出两类字段的归属），是理解两状态分野与统一动机的起点。，属于该因子的基础原则，应在设计中显式落实。
- 模板 src/state.ts：FileSystemThreadStore 用 crypto.randomUUID 生成 id，写 .threads/{id}.json 与 {id}.txt 双文件。
- agent.ts 的 awaitingHumanResponse()：lastEvent 意图为 request_more_information/done_for_now 时判定在等人。
- awaitingHumanApproval()：lastEvent 意图为 divide 时判定需审批（workshop 演示场景）。
- unify-state 动画/GIF（155-unify-state-animation.gif）演示两列状态合并为单线程。
- server.ts 中 create/update 线程，webhook 后 load_state 恢复并继续循环的完整链路。

## 反模式/易错点

- 为执行状态与业务状态建立两套独立系统，同步逻辑成为维护噩梦，状态极易不一致，应合并为单一事件流。，属于该因子的基础原则，应在设计中显式落实。
- 把 session id、密码等不该进上下文的东西硬塞给 LLM，引入安全与泄露风险，机密只存外部存储。
- 把执行状态藏进全局可变变量或进程内存，进程一挂全丢，无法恢复，必须落盘持久化到事件流中才能保命恢复。
- 状态没有单一序列化路径，调试时需要跨多个存储拼历史，问题定位困难，应统一走 thread 的单一序列化路径。
- 新增状态时改动存储 schema 而不是新增事件类型，破坏向后兼容性，应以追加事件类型代替改结构。，属于该因子的基础原则，应在设计中显式落实。
- 不在暂停/等待前持久化，导致恢复时丢失中间过程，恢复残缺，每次等待或暂停前都必须先 save_state 持久化落盘。

## 源码索引（实践参考）

- `08-source/agent-content/factor-05-unify-execution-state.md` — 原文完整内容：统一执行/业务状态与 7 条收益
- `08-source/agent-packages/create-12-factor-agent/template/src/state.ts` — 模板 FileSystemThreadStore：thread 持久化的 create/get/update
- `08-source/agent-packages/create-12-factor-agent/template/src/agent.ts` — 模板 Thread 类：事件流与 awaitingHumanResponse 状态推断

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-state → ag-pause | 前置依赖 | 统一状态支持暂停恢复 |
| ag-state → ag-reducer | 前置依赖 | 统一状态是无状态 reducer 基础 |
| ag-state → ag-pause | 共现 | 状态统一与暂停恢复共现 |

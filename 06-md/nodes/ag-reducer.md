# 无状态 Reducer (Stateless reducer)

- ID: `ag-reducer`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 高级 advanced

> 将 Agent 建模为无状态 reducer（state, event）→ state

## 核心主张 (what)

- 第 12 条：把 Agent 建模成无状态的归约器（stateless reducer）。原文自己承认：写到这已超 1000 行 markdown，这条主要是图个乐。
- 配图 agent-foldl（1c5-agent-foldl.png）把 Agent 循环描绘成函数式编程里的 foldl：用函数折叠事件列表。
- reducer 视角下：Agent 是一个纯函数，输入是『迄今为止的全部历史事件』，输出是『下一步动作（工具意图）』。
- 这与 factor 5（统一执行/业务状态）一脉相承并进一步收束：把 thread 当作纯粹的数据累积，Agent 只是对它的归约。
- reducer 无内部可变状态：状态+事件进，下状态+可能的副作用（工具执行）出，决策与效应分离。，属于该因子的基础原则，应在设计中显式落实。
- 体现『Agents are just programs』的最终哲学：Agent 循环 = 状态(state) 加事件(event) 归约的确定迭代，可序列化、可恢复、可分叉。
- 把 Agent 视为 reducer 让『恢复/分叉/审计』等能力在数学上变得显然：只要事件流完整，任何断点都可重建。
- 原文只有一句加两张图，本节点结合 factor 5、factor 3 与模板 state.ts/agent.ts 的工程形态合理展开。

## 为什么 (why)

- 收束统一状态：把 factor 5 的统一状态观用函数式视角彻底表达——状态即事件的归约结果。，属于该因子的基础原则，应在设计中显式落实。
- 无状态化带来确定性：同样的事件序列必然产出同样的决策，行为可预测、可复现，调试容易。，属于该因子的基础原则，应在设计中显式落实。
- 可序列化/恢复/分叉成为结构性必然：thread 是纯数据，load 即可重建任意状态，无需额外机制。
- 呼应 Agent 的本质定义：prompt + switch + accumulated context + for loop 四件套，reducer 是其最简洁抽象。
- 降低心智负担：把『Agent 是什么』收束为『一个输入历史、输出下一步的函数』，便于与确定性 DAG 一起编排。

## 如何实践 (how)

- 把循环建模为 reducer：reducer(thread_events) → next_step，即 determine_next_step 对事件流的归约。
- 状态显式化：每一步把上一步的 state 与当前 event 作为输入，产出 new_state 与副作用（工具执行）记录。
- 所有事件（user_input/tool_call/tool_response/error/human_response）进同一事件流，状态只在事件流中体现。
- 配合 factor 5 的 FileSystemThreadStore 持久化 thread，reducer 函数保持无状态，状态全在数据里。
- 恢复 = 重新把已持久化事件喂给 reducer；分叉 = 复制事件子集作为新输入，两种能力天然免费。
- 用 factor 3 的 serializeForLLM 控制 reducer 实际『看到』的上下文，实现状态压缩与过滤。
- 配合 factor 10：每个小 Agent 都是一个职责单一的小 reducer，由确定性 DAG 组合。
- 副作用隔离：工具执行（写数据库、发请求）不作为 reducer 内部逻辑，而是其外部效应，便于审计。

## 案例 (cases)

- 原文配图 1c0-stateless-reducer.png 与 1c5-agent-foldl.png（foldl 折叠示意图）。
- 原文结语：『this one is mostly just for fun』的自嘲式定位，行文风格上以轻松收尾。
- 模板 Thread 类（事件流 + serializeForLLM）作为 reducer 的数据载体。
- 模板 state.ts 的 FileSystemThreadStore：thread 序列化落盘，为无状态 reducer 提供纯数据状态。
- factor 5 的『加载 thread 从任意点恢复』在 reducer 视角下即事件重放，视角统一更清晰。
- foldl 的函数式语义：从初始状态起依次把每个事件归约进去，产出最终状态/决策序列，抽象优雅。，属于该因子的基础原则，应在设计中显式落实。

## 反模式/易错点

- 把状态藏在全局可变变量里，reducer 不再无状态，重放与恢复随之失效，纯函数性被破坏。，属于该因子的基础原则，应在设计中显式落实。
- 把副作用（真实 API 调用）写进 reducer 内部逻辑，破坏『纯函数+外部效应』的边界，审计困难。
- 事件流不完整/不持久化，reducer 无数据可归约，断点无法重建，事件完整性是前提。，属于该因子的基础原则，应在设计中显式落实。
- 让 reducer 依赖进程内存中的隐式上下文而非显式事件输入，序列化与分叉无从谈起，输入须显式。，属于该因子的基础原则，应在设计中显式落实。
- 忽略本因子『主要是图个乐』的定位，为函数式而函数式地过度设计，原文自身也承认这一点。，属于该因子的基础原则，应在设计中显式落实。

## 源码索引（实践参考）

- `08-source/agent-content/factor-12-stateless-reducer.md` — 原文：Agent 建模为无状态 reducer（foldl），一句加两图
- `08-source/agent-packages/create-12-factor-agent/template/src/state.ts` — 模板持久化：FileSystemThreadStore 承载 reducer 的纯数据状态
- `08-source/agent-packages/create-12-factor-agent/template/src/agent.ts` — 模板 Thread 类 + agentLoop：循环即对事件流的归约
- `08-source/agent-content/factor-05-unify-execution-state.md` — 理论基础：统一执行/业务状态

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-state → ag-reducer | 前置依赖 | 统一状态是无状态 reducer 基础 |
| ag-control → ag-reducer | 前置依赖 | 确定性控制流保障 reducer 语义 |
| ag-reducer → ag-small | 前置依赖 | 无状态 reducer 使小 Agent 可行 |
| t-stateless → ag-reducer | 前置依赖 | 无状态性落到 Agent 的 reducer |
| app-processes → ag-reducer | 变体 | 无状态进程 ↔ 无状态 reducer |
| tool-create-agent → ag-reducer | 组合 | 模板含 state.ts 无状态 reducer |

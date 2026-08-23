# 压缩错误进上下文 (Compact errors)

- ID: `ag-errors`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 进阶 intermediate

> 把错误摘要压缩回上下文窗口供模型反思

## 核心主张 (what)

- Agent 的一大好处是『自愈』：对短任务，LLM 调用工具失败时，好的模型相当有机会读懂错误消息或堆栈并想出在后续调用中改什么。
- 大多数框架都实现了这一点，但你可以只做这一件事而不做其他 11 条因子——它独立成立，投入产出比极高。
- 基础版实现：try handle_next_step，异常时把 {type:'error', data: format_error(e)} 追加进 thread，继续循环重试。
- 进阶版：为具体工具调用实现 errorCounter，把单工具重试限制在约 3 次，防止无限空转，给自愈加护栏。
- 计数逻辑：成功执行后 consecutive_errors 归零；异常时自增，小于 3 则把错误写入上下文再循环，否则 break。
- 达到连续错误阈值是升级到人类的好时机：可以由模型决定，也可以由确定性代码接管控制流去请求人类介入。，属于该因子的基础原则，应在设计中显式落实。
- 原文提醒：如果错误压缩做得太多，Agent 会开始空转（spin out），反复重试同一个错误，陷入死循环。
- 此时 factor 8（掌控控制流）和 factor 3（掌控上下文）登场：你不需要把原始错误原样塞回，可以重构其表示、移走先前事件，或用任何有效的确定性手段把它拉回正轨。
- 防止错误空转的头号方法是拥抱 factor 10（小而专注的 Agent），让上下文短到错误无从累积。
- 自愈依赖『把错误消息喂给 LLM 让它改错』，因此错误的格式与上下文保留策略直接决定自愈质量与成功率。

## 为什么 (why)

- 自愈：LLM 能读懂错误消息并在下一次工具调用中自行修正，无需人工介入，大幅减少运维负担。，属于该因子的基础原则，应在设计中显式落实。
- 持久化：即使一个工具调用失败，Agent 也能继续运行，整体任务不因单点失败而夭折，可用性提升。，属于该因子的基础原则，应在设计中显式落实。
- 错误+重试阈值是『拉人类进循环』的天然触发点，为升级处理提供明确信号，升级时机有据可依。，属于该因子的基础原则，应在设计中显式落实。
- 这是唯一可以脱离其他 11 条因子单独落地的一条，单独实施就能获得大量价值，投入产出比极高。，属于该因子的基础原则，应在设计中显式落实。
- 配合上下文管理（factor 3），可以主动修剪错误与失败事件，防止失败历史污染后续推理，决策更干净。

## 如何实践 (how)

- 基础循环：while True 里 determine_next_step → push intent 事件 → try handle_next_step → except 时 push {type:'error', data: format_error(e)} 并继续。
- 格式化错误：用 format_error(e) 把异常转成适合 LLM 阅读的简洁文本，而非原始堆栈噪音。
- 计数进阶：consecutive_errors 变量，成功即归零，失败自增，达到 3 则 break。
- 阈值处理：连续失败达到阈值时，选择『重置部分上下文 / 升级人类 / 其他你想做的事』，策略完全自主。
- 升级人类：在错误重试耗尽后调用 factor 7 的人类联系机制，让真人接手排障，避免无谓空转。，属于该因子的基础原则，应在设计中显式落实。
- 重构错误表示：不原样塞回原始错误，用 factor 3 的 XML 标签（如 <error> 块）结构化表达。
- 从窗口移除已解决错误：事件解决后从上下文隐藏，避免 LLM 反复看到失败史，保持决策干净。，属于该因子的基础原则，应在设计中显式落实。
- 结合 factor 10：把长任务拆成小 Agent，让每个 Agent 的上下文短到错误空转无从发生。

## 案例 (cases)

- 基础版代码：thread['events'].append({type:'error', data: format_error(e)}) 后继续循环。
- 计数进阶代码：consecutive_errors 成功归零/失败自增/达到 3 则 break 的完整片段。
- 原文句式：『Good LLMs have a fairly good chance of reading an error message or stack trace and figuring out what to change』。
- 升级人类建议：『Hitting some consecutive-error-threshold might be a great place to escalate to a human』。
- 空转警示：『if you do this TOO much, your agent will start to spin out and might repeat the same error over and over』。
- 动画 195-factor-09-errors.gif 演示错误写入上下文后模型自我修正的过程，直观展示自愈闭环。
- 与 factor 3 的结合示例：错误解决后从上下文移除、用自定义格式表示错误，双向受益。，属于该因子的基础原则，应在设计中显式落实。

## 反模式/易错点

- 无节制的无限重试（无 errorCounter），Agent 空转反复重试同一个错误，浪费资源且无收敛保证。
- 把原始堆栈/错误原文不加格式化地塞回上下文，浪费 token 且难以被模型有效解读，应格式化为事件。
- 错误解决后仍把失败事件留在上下文，模型被失败历史持续影响，应主动从窗口移除已解决错误。，属于该因子的基础原则，应在设计中显式落实。
- 达到重试阈值后不升级人类也不换策略，死循环到底，重试护栏与升级机制必须并存方可收敛。，属于该因子的基础原则，应在设计中显式落实。
- 用单体大 Agent 承载长任务，错误累积进长上下文后彻底迷失，应拆成小 Agent 缩短上下文。，属于该因子的基础原则，应在设计中显式落实。
- 把错误吞掉不写入上下文，LLM 毫不知情、自愈无从谈起，错误必须作为事件回写。，属于该因子的基础原则，应在设计中显式落实。

## 源码索引（实践参考）

- `08-source/agent-content/factor-09-compact-errors.md` — 原文完整内容：错误写回上下文自愈、errorCounter 计数
- `08-source/agent-content/factor-08-own-your-control-flow.md` — 控制流关联：错误处理是自定义控制结构的一部分
- `08-source/agent-content/factor-03-own-your-context-window.md` — 上下文管理：错误事件格式化与已解决错误隐藏策略

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-context → ag-errors | 前置依赖 | 错误压缩是上下文工程应用 |
| t-observability → ag-errors | 前置依赖 | 可观测性落到错误压缩 |
| app-logs → ag-errors | 变体 | 日志流 ↔ 错误压缩 |
| ag-context → ag-errors | 组合 | 上下文 + 错误压缩 |

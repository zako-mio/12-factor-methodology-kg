# 掌控控制流 (Own your control flow)

- ID: `ag-control`
- 类型: 方法原则
- 来源: Agent 体系
- 分组: GB · 12 Factor Agent 体系
- 阶段: 进阶 intermediate

> 控制流由代码决定，LLM 只做决策点

## 核心主张 (what)

- 如果你掌控自己的控制流，就能做很多有趣的事：为你的特定用例构建自己的控制结构，而不是被框架规定死。，属于该因子的基础原则，应在设计中显式落实。
- 某些类型的工具调用可能是跳出循环的理由——例如等待人类回复，或等待训练流水线这类长任务完成，需要中断。
- 你也可以融入自定义实现：工具结果的汇总/缓存、对结构化输出做 LLM-as-judge、上下文压缩或其他记忆管理、日志/tracing/指标、客户端限流、持久 sleep/暂停/等事件。
- 原文给出三种控制流模式示例：request_clarification（模型要求更多信息，跳出循环等人）、fetch_git_tags（取标签、追加上下文、直接交回模型）、deploy_backend（高价值，跳出循环等人批准）。
- handle_next_step 里用 while True 循环：determine_next_step → 按 intent 分支，async 步骤 break 等 webhook，sync 步骤 continue 直接再喂模型。
- 核心诉求：『我们需要能在工具选择与工具调用之间打断正在工作的 Agent 并在之后恢复』——这是作者对每个 AI 框架的头号功能请求。
- 没有这种恢复粒度，就无法在工具运行前审查/批准调用，被迫在三者中选：内存里 sleep 等长任务、只让 Agent 做低风险调用、或让 Agent 放手干高风险事赌它不搞砸。
- 该模式允许你随意中断/恢复 Agent 流程，创造更自然的多轮对话与工作流，恢复点完全由你掌控。，属于该因子的基础原则，应在设计中显式落实。
- 与 factor 5（统一状态）和 factor 6（暂停/恢复）紧密相关，但可以独立实现，不必捆绑落地。
- 掌控控制流的本质：循环 + switch 语句 + 事件累积三者全在你的代码里，而非框架黑盒，一切皆可干预。

## 为什么 (why)

- 工具选择与执行之间的中断点是审批与复核的必需窗口，缺失它就无法安全地执行高价值操作，风险失控。，属于该因子的基础原则，应在设计中显式落实。
- 自定义控制结构才能支持自然工作流：中断等人、等待长任务、再无缝恢复，体验更接近真实协作。，属于该因子的基础原则，应在设计中显式落实。
- 可以按需插入缓存、LLM-judge、限流、日志、指标等横切逻辑，框架黑盒做不到这一点，掌控力最强。
- 没有该粒度的三种被迫选项（while...sleep / 只做低风险 / yolo）全部不可接受，掌控控制流是唯一解。
- 只有自建控制流才能把『工具调用』真正当作 JSON 驱动的可编排步骤，而非不可中断的函数执行，灵活度最高。

## 如何实践 (how)

- 实现 while True 循环：determine_next_step(thread_to_prompt(thread)) 取下一步意图，形成主循环骨架。
- 按 intent 分支：request_clarification → push 事件、send_message_to_human、db.save_thread、break（async 等 webhook）；fetch_open_issues → push、调接口、push 结果、continue。
- create_issue → push 事件、request_human_approval、save_thread、break（async），等人类批准后由 webhook 恢复。
- 把中断点刻意放在『工具选择之后、工具执行之前』，让确定性代码有机会先审批再放行，掌握完整决策链。，属于该因子的基础原则，应在设计中显式落实。
- 恢复时由 webhook 或调用方 push 新事件后重新进入循环（复用 factor 6 的加载机制）。
- 融入自定义横切逻辑：工具结果缓存、LLM-as-judge 校验结构化输出、上下文压缩、客户端限流、日志/指标。
- 持久 sleep 用『保存状态 + 等事件』实现，而非内存 sleep，保证可恢复性，进程重启也不丢状态。
- 模板 handleNextStep（switch 分发工具）加外层 while true（agentLoop）即最小化掌控控制流的骨架。

## 案例 (cases)

- 原文 handle_next_step 三分支：request_clarification / fetch_open_issues / create_issue 的 break 与 continue 控制。
- 头号功能请求引述：『interrupt a working agent and resume later, ESPECIALLY between the moment of tool selection and tool invocation』。
- 没有粒度时的三选一困境：① while...sleep 内存等待 ② 只做研究/汇总类低风险调用 ③ yolo 放手。
- 可融入的自定义实现清单：summarization/caching、LLM-as-judge、context compaction、logging/tracing/metrics、rate limiting、durable sleep。
- 模板 agent.ts 的 agentLoop（while true + switch intent + tool_response 回写）。
- workshop Chapter 3 的 agentLoop 初版：done_for_now 返回、add 执行并 continue、default 抛 Unknown intent。
- deploybot 场景：确定性代码在 Agent 每次部署请求之间请求人类批准，Agent 只输出 JSON 意图。

## 反模式/易错点

- 在内存里 while...sleep 等待长任务，进程一断必须从头重启，可恢复性为零，是典型的反模式。
- 把 Agent 限制为只做低风险、低价值调用（研究/汇总），白白浪费 Agent 的决策能力，价值缩水。
- 给 Agent 高价值工具却不设审批点，纯靠赌（yolo）它不会搞砸，风险不可控，必须加复核。，属于该因子的基础原则，应在设计中显式落实。
- 把控制流交给框架黑盒，无法在工具选择与执行之间插入任何逻辑，丧失所有干预能力，危险且不可调。，属于该因子的基础原则，应在设计中显式落实。
- 所有工具都同步执行返回，没有任何 async break 的等待路径，无法处理长任务与人工介入。，属于该因子的基础原则，应在设计中显式落实。
- 没有 while True 主循环，Agent 退化为单步函数调用，无法完成多步任务，循环骨架是底线。

## 源码索引（实践参考）

- `08-source/agent-content/factor-08-own-your-control-flow.md` — 原文完整内容：自建控制结构、handle_next_step 三分支、头号需求
- `08-source/agent-packages/create-12-factor-agent/template/src/agent.ts` — 模板 agentLoop/handleNextStep：while+switch 控制流骨架
- `08-source/agent-workshops/2025-05/walkthrough.md` — workshop Chapter 3 工具循环、Chapter 8/9 服务端控制流

## 相关关系

| 方向 | 类型 | 关系 |
|---|---|---|
| ag-nl2tool → ag-control | 前置依赖 | 工具调用需要确定性控制流 |
| ag-tools → ag-control | 前置依赖 | 工具组合受控制流编排 |
| ag-control → ag-reducer | 前置依赖 | 确定性控制流保障 reducer 语义 |
| t-control → ag-control | 前置依赖 | 控制流治理落到 Agent 编排 |
| app-build-run → ag-control | 变体 | 阶段分离 ↔ 控制流所有权 |
